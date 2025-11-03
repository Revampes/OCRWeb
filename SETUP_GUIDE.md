# DeepSeek-OCR Web App Setup Guide

## Complete Setup Instructions

### Step 1: Install Python Packages

```powershell
# Navigate to project directory
cd c:\Users\user\Downloads\OCRWeb

# Install main requirements
pip install Flask flask-cors Werkzeug python-dotenv Pillow PyMuPDF transformers torch torchvision

# Install vLLM (this may take a while)
pip install vllm
```

### Step 2: Install DeepSeek-OCR Dependencies

```powershell
cd c:\Users\user\Desktop\DeepSeek-OCR-main
pip install -r requirements.txt
```

### Step 3: Download DeepSeek-OCR Model

The model will be automatically downloaded from Hugging Face when you first run the app.
Model: `deepseek-ai/DeepSeek-OCR`

This is a large model (~7-8GB), so the first run will take time to download.

### Step 4: Run the Application

```powershell
cd c:\Users\user\Downloads\OCRWeb
python app.py
```

The first startup will:
1. Download the DeepSeek-OCR model (if not already downloaded)
2. Load the model into GPU memory
3. Start the Flask web server

This may take 5-10 minutes on first run.

### Step 5: Access the Web Interface

Open your browser and go to: `http://localhost:5000`

## System Requirements

- **GPU**: CUDA-capable NVIDIA GPU with 8GB+ VRAM (required)
- **RAM**: 16GB+ system RAM recommended
- **Storage**: 10GB+ free space for model files
- **OS**: Windows 10/11
- **Python**: 3.8, 3.9, 3.10, or 3.11

## Troubleshooting

### CUDA Not Available
If you get CUDA errors, install CUDA toolkit from NVIDIA.

### Out of Memory
Reduce `gpu_memory_utilization` in `app.py` from 0.75 to 0.5 or lower.

### Model Download Fails
Manually download the model:
```python
from transformers import AutoModel
model = AutoModel.from_pretrained("deepseek-ai/DeepSeek-OCR", trust_remote_code=True)
```

## Performance

- **First Run**: 5-10 minutes (model download + initialization)
- **Subsequent Runs**: 30-60 seconds (model loading)
- **OCR Processing**: 2-10 seconds per image (depending on complexity)

Enjoy using DeepSeek-OCR! 🚀
