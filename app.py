from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from PIL import Image
import fitz  # PyMuPDF
import torch

# CRITICAL FIX: Prevent flash attention imports before transformers loads
# This must happen BEFORE importing transformers
os.environ["TRANSFORMERS_NO_ADVISORY_WARNINGS"] = "1"
os.environ["DISABLE_FLASH_ATTENTION"] = "1"

# Force CPU mode if no CUDA available
# This prevents the model from trying to use .cuda()
if not torch.cuda.is_available():
    os.environ["CUDA_VISIBLE_DEVICES"] = ""  # Hide CUDA devices
    print("⚠️  No CUDA detected - forcing CPU-only mode")
    
    # Disable bfloat16 on CPU (not fully supported)
    torch.backends.cpu.allow_tf32 = False
    
    # Monkey-patch torch.cuda.is_available() to always return False
    original_is_available = torch.cuda.is_available
    torch.cuda.is_available = lambda: False
    
    # Monkey-patch all .cuda() methods to redirect to CPU
    _original_tensor_cuda = torch.Tensor.cuda
    _original_module_cuda = torch.nn.Module.cuda
    
    def _fake_tensor_cuda(self, *args, **kwargs):
        # Force float32 on CPU
        return self.float().to(torch.device('cpu'))
    
    def _fake_module_cuda(self, *args, **kwargs):
        # Force float32 on CPU
        return self.float().to(torch.device('cpu'))
    
    torch.Tensor.cuda = _fake_tensor_cuda
    torch.nn.Module.cuda = _fake_module_cuda
    
    # Also patch bfloat16 conversion to redirect to float32 on CPU
    _original_tensor_bfloat16 = torch.Tensor.bfloat16
    def _fake_bfloat16(self):
        print("⚠️  bfloat16 requested on CPU, using float32 instead")
        return self.float()
    torch.Tensor.bfloat16 = _fake_bfloat16
    
    # Patch embedding layers to handle float indices (convert to long)
    _original_embedding_forward = torch.nn.Embedding.forward
    def _patched_embedding_forward(self, input):
        # If input is float, convert to long for embedding lookup
        if input.dtype in [torch.float32, torch.float16, torch.bfloat16]:
            input = input.long()
        return _original_embedding_forward(self, input)
    torch.nn.Embedding.forward = _patched_embedding_forward
    
    # Patch masked_scatter_ to handle float masks (convert to bool)
    _original_masked_scatter_ = torch.Tensor.masked_scatter_
    def _patched_masked_scatter_(self, mask, source):
        # If mask is float, convert to bool (assumes > 0.5 = True)
        if mask.dtype in [torch.float32, torch.float16, torch.bfloat16]:
            mask = mask.bool()
        return _original_masked_scatter_(self, mask, source)
    torch.Tensor.masked_scatter_ = _patched_masked_scatter_
    
    print("✓ CPU-only patches installed (all .cuda() and .bfloat16() calls redirected)")
    print("✓ All operations will use float32 for CPU compatibility")
    print("✓ Embedding layer patched to handle float→long conversion")
    print("✓ masked_scatter_ patched to handle float→bool masks")

# Use AutoModel for DeepSeek-OCR (it's a VLM, not pure causal LM)
from transformers import AutoProcessor, AutoModel, AutoTokenizer

# Fix DynamicCache compatibility issue with transformers 4.57.1+
try:
    from transformers.cache_utils import DynamicCache
    print("⚙️  Patching DynamicCache for transformers 4.57.1+ compatibility...")
    
    # Patch __init__ to add _seen_tokens tracking
    original_init = DynamicCache.__init__
    def patched_init(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
        self._seen_tokens = 0
        self._max_length = None
    
    # Add seen_tokens property
    def get_seen_tokens(self):
        if hasattr(self, '_seen_tokens'):
            return self._seen_tokens
        # Fallback: calculate from cache
        if hasattr(self, 'key_cache') and len(self.key_cache) > 0:
            return self.key_cache[0].shape[-2] if self.key_cache[0] is not None else 0
        return 0
    
    def set_seen_tokens(self, value):
        self._seen_tokens = value
    
    # Add get_max_length method
    def get_max_length(self):
        if hasattr(self, '_max_length'):
            return self._max_length
        return None
    
    # Add get_seq_length method (sometimes also needed)
    def get_seq_length(self, layer_idx=None):
        if layer_idx is not None and hasattr(self, 'key_cache') and len(self.key_cache) > layer_idx:
            if self.key_cache[layer_idx] is not None:
                return self.key_cache[layer_idx].shape[-2]
        elif hasattr(self, 'key_cache') and len(self.key_cache) > 0:
            if self.key_cache[0] is not None:
                return self.key_cache[0].shape[-2]
        return 0
    
    # Apply patches
    DynamicCache.__init__ = patched_init
    if not hasattr(DynamicCache, 'seen_tokens'):
        DynamicCache.seen_tokens = property(get_seen_tokens, set_seen_tokens)
    if not hasattr(DynamicCache, 'get_max_length'):
        DynamicCache.get_max_length = get_max_length
    if not hasattr(DynamicCache, 'get_seq_length'):
        DynamicCache.get_seq_length = get_seq_length
    
    print("✓ DynamicCache compatibility patches applied")
    print("  - seen_tokens property")
    print("  - get_max_length() method")
    print("  - get_seq_length() method")
except Exception as e:
    print(f"⚠️  Could not patch DynamicCache: {e}")

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'webp', 'pdf'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Create uploads folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Global model instances (lazy loaded)
_model = None
_tokenizer = None

def get_deepseek_model():
    """Lazy load DeepSeek-OCR model"""
    global _model, _tokenizer
    
    if _model is None:
        print("=" * 60)
        print("Loading DeepSeek-OCR model...")
        print("First time: ~8GB download + initialization (5-10 min)")
        print("=" * 60)
        print("\n⚠️  IMPORTANT: This model requires significant resources:")
        print("   - GPU: ~8GB VRAM, fast inference (~5-10 sec/image)")
        print("   - CPU: ~16GB RAM, VERY slow inference (~2-5 min/image)")
        print("=" * 60)
        
        model_name = "deepseek-ai/DeepSeek-OCR"
        
        # Check if CUDA is available and actually works
        device = "cpu"
        try:
            if torch.cuda.is_available():
                # Test if CUDA actually works
                torch.zeros(1).cuda()
                device = "cuda"
                print(f"🔧 Using device: {device}")
            else:
                print(f"🔧 Using device: {device}")
                print("⚠️  WARNING: Running on CPU will be VERY slow!")
                print("   Recommended: Use NVIDIA GPU for practical performance.")
        except Exception as cuda_error:
            print(f"🔧 Using device: cpu (CUDA check failed: {cuda_error})")
            print("⚠️  WARNING: Running on CPU will be VERY slow!")
            print("   Recommended: Use NVIDIA GPU for practical performance.")
        
        try:
            print("\n📥 Loading tokenizer...")
            import time
            start_time = time.time()
            
            _tokenizer = AutoTokenizer.from_pretrained(
                model_name,
                trust_remote_code=True
            )
            tok_time = time.time() - start_time
            print(f"✓ Tokenizer loaded ({tok_time:.1f}s)")
            
            print("\n📥 Loading DeepSeek-OCR model (this takes a few minutes)...")
            print("⏳ First time: Downloading ~8GB (5-10 min)")
            print("⏳ Subsequent: Loading from cache (30-60s GPU, 2-3min CPU)")
            print("⚙️  Applying compatibility patches for transformers 4.57.1+...")
            model_start = time.time()
            
            # Monkey-patch to handle missing LlamaFlashAttention2
            import sys
            import transformers.models.llama.modeling_llama as llama_module
            
            # If LlamaFlashAttention2 doesn't exist, create a dummy class
            if not hasattr(llama_module, 'LlamaFlashAttention2'):
                print("⚠️  LlamaFlashAttention2 not found, creating compatibility shim...")
                # Create a dummy class that points to the standard attention
                llama_module.LlamaFlashAttention2 = llama_module.LlamaAttention
                print("✓ Compatibility shim installed")
            
            # First try: Load with eager attention (safest, most compatible)
            try:
                print("📦 Starting model download/load... (this is the slow part)")
                _model = AutoModel.from_pretrained(
                    model_name,
                    trust_remote_code=True,
                    torch_dtype=torch.float16 if device == "cuda" else torch.float32,
                    low_cpu_mem_usage=True,
                    device_map="auto" if device == "cuda" else None,
                    attn_implementation="eager",  # Avoid flash attention issues
                    force_download=False,
                    resume_download=True,
                )
                model_time = time.time() - model_start
                print(f"✓ Model loaded with eager attention ({model_time:.1f}s)")
            except Exception as e:
                error_msg = str(e)
                print(f"⚠️  Eager attention failed: {error_msg[:200]}")
                print("Trying alternative loading method...")
                
                # Second try: Load with sdpa attention (scaled dot product attention)
                try:
                    _model = AutoModel.from_pretrained(
                        model_name,
                        trust_remote_code=True,
                        torch_dtype=torch.float16 if device == "cuda" else torch.float32,
                        low_cpu_mem_usage=True,
                        device_map="auto" if device == "cuda" else None,
                        attn_implementation="sdpa",
                        force_download=False,
                        resume_download=True,
                    )
                    print("✓ Model loaded with SDPA attention")
                except Exception as e2:
                    error_msg2 = str(e2)
                    print(f"⚠️  SDPA attention failed: {error_msg2[:200]}")
                    print("Trying without attention specification...")
                    
                    # Third try: Load without specifying attention (let model decide)
                    _model = AutoModel.from_pretrained(
                        model_name,
                        trust_remote_code=True,
                        torch_dtype=torch.float16 if device == "cuda" else torch.float32,
                        low_cpu_mem_usage=True,
                        device_map="auto" if device == "cuda" else None,
                        force_download=False,
                        resume_download=True,
                    )
                    print("✓ Model loaded with default attention")
            
            # Move model to correct device with proper dtype
            if device == "cpu":
                print("⚙️  Converting model to CPU with float32 (bfloat16 not fully supported on CPU)...")
                # Force convert ALL parameters and buffers to float32
                _model = _model.float()  # Convert to float32
                _model = _model.to(torch.device('cpu'))
                
                # Additional: Convert any remaining bfloat16 parameters
                for name, param in _model.named_parameters():
                    if param.dtype == torch.bfloat16:
                        param.data = param.data.float()
                
                for name, buffer in _model.named_buffers():
                    if buffer.dtype == torch.bfloat16:
                        buffer.data = buffer.data.float()
                
                print("⚠️  Model set to CPU mode (will be slow)")
            else:
                # Only try .cuda() if we confirmed CUDA works
                try:
                    _model = _model.cuda()
                    print("✓ Model moved to GPU")
                except Exception as e:
                    print(f"⚠️  GPU move failed: {e}, falling back to CPU")
                    _model = _model.float().to(torch.device('cpu'))
            
            _model.eval()
            
            print("\n" + "=" * 60)
            print("✅ DeepSeek-OCR model loaded successfully!")
            print(f"   Device: {device}")
            print(f"   Dtype: {next(_model.parameters()).dtype}")
            print("=" * 60)
            
        except Exception as e:
            print(f"\n❌ Error loading model: {str(e)}")
            raise
    
    return _model, _tokenizer

def extract_text_from_image(image: Image.Image) -> str:
    """Extract text from an image using DeepSeek-OCR"""
    try:
        print("\n🔄 Starting OCR extraction...")
        model, tokenizer = get_deepseek_model()
        
        # Save image temporarily (model expects file path)
        import tempfile
        temp_dir = tempfile.mkdtemp()
        temp_image_path = os.path.join(temp_dir, 'input_image.png')
        image.save(temp_image_path, 'PNG')
        
        try:
            # Prepare the prompt (using DeepSeek-OCR's format)
            prompt = "<image>\nExtract all text from this image."
            
            print("📝 Processing image with DeepSeek-OCR...")
            print("⚙️  Using: base_size=1024, image_size=640, crop_mode=True")
            
            # Use DeepSeek-OCR's custom infer method
            # output_path is required (even though we won't save results)
            result = model.infer(
                tokenizer=tokenizer,
                prompt=prompt,
                image_file=temp_image_path,
                output_path=temp_dir,  # Required, but save_results=False means no files saved
                base_size=1024,        # Base resolution
                image_size=640,        # Crop resolution
                crop_mode=True,        # Enable cropping for better accuracy
                save_results=False,    # Don't actually save files
                test_compress=False
            )
            
            # Clean up result
            if result:
                text = result.strip()
                # Remove the prompt from the result if present
                if text.startswith("Extract all text from this image."):
                    text = text.replace("Extract all text from this image.", "").strip()
            else:
                text = "No text detected in the image."
            
            print(f"✅ OCR complete! Extracted {len(text)} characters\n")
            return text
            
        finally:
            # Clean up temporary files and directory
            import shutil
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir, ignore_errors=True)
        
    except Exception as e:
        print(f"❌ OCR Error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise Exception(f"OCR processing failed: {str(e)}")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/ocr', methods=['POST'])
def ocr_scan():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed. Please upload an image or PDF file.'}), 400
        
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        print(f"\n📁 Processing file: {filename}")
        
        try:
            if filepath.lower().endswith('.pdf'):
                pdf_document = fitz.open(filepath)
                all_text = []
                
                print(f"📄 PDF with {len(pdf_document)} page(s)")
                
                for page_num in range(len(pdf_document)):
                    print(f"\n--- Page {page_num + 1}/{len(pdf_document)} ---")
                    
                    page = pdf_document[page_num]
                    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                    img_data = pix.tobytes("png")
                    
                    from io import BytesIO
                    image = Image.open(BytesIO(img_data)).convert('RGB')
                    
                    page_text = extract_text_from_image(image)
                    all_text.append(f"--- Page {page_num + 1} ---\n{page_text}")
                
                pdf_document.close()
                extracted_text = "\n\n".join(all_text)
            else:
                image = Image.open(filepath).convert('RGB')
                extracted_text = extract_text_from_image(image)
            
            if not extracted_text or not extracted_text.strip():
                extracted_text = "No text could be extracted from the file."
                
        except Exception as ocr_error:
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'error': f'OCR extraction failed: {str(ocr_error)}'}), 500
        
        os.remove(filepath)
        
        return jsonify({
            'success': True,
            'text': extracted_text,
            'filename': filename
        })
    
    except Exception as e:
        if 'filepath' in locals() and os.path.exists(filepath):
            os.remove(filepath)
        
        return jsonify({
            'error': f'OCR processing failed: {str(e)}'
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'message': 'Server is running'})

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 DeepSeek-OCR Web Application")
    print("=" * 60)
    print("Starting Flask server...")
    print("\n📌 Note: DeepSeek-OCR model will load on first request")
    print("   First time: ~8GB download (5-10 minutes)")
    print("   Subsequent: ~30-60 seconds model loading")
    print("=" * 60)
    print("\n🌐 Access at: http://localhost:5000")
    print("=" * 60 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
