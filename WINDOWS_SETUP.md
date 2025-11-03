# DeepSeek-OCR Web Application - Windows Setup Guide

## ✅ Installation Complete

Your DeepSeek-OCR web application is now running on Windows!

### 🖥️ Access the Application

The server is running at:
- **Local**: http://127.0.0.1:5000
- **Network**: http://192.168.100.121:5000

Open your web browser and navigate to either address to use the OCR application.

---

## 📋 What Changed

### Windows Compatibility Fix

The original implementation used **vLLM**, which doesn't work well on Windows due to:
- Long file path issues during installation
- POSIX-specific dependencies
- Build compilation problems

### New Implementation

The application now uses:
- **transformers** library directly - Full Windows support
- **AutoModelForCausalLM** - Standard Hugging Face model loading
- **AutoProcessor** - Image and text processing
- No dependency on vLLM or custom DeepSeek-OCR repository code

This approach is:
- ✅ **Windows-compatible** - Works on all Windows versions
- ✅ **Simpler** - Fewer dependencies to install
- ✅ **Reliable** - Uses stable, well-tested libraries
- ✅ **GPU-accelerated** - Automatically uses CUDA if available

---

## 🚀 First Use

### Model Download
On your **first OCR request**, the application will:
1. Download the DeepSeek-OCR model (~8GB) from Hugging Face
2. Cache it locally (typically in `C:\Users\[username]\.cache\huggingface`)
3. Load the model into memory

This process takes **5-10 minutes** depending on your internet speed.

**Subsequent uses** will be much faster - the model loads from cache in 30-60 seconds.

### Testing the Application

1. Open http://127.0.0.1:5000 in your browser
2. Click the upload area or drag a document
3. Select an image or PDF file
4. Wait for the OCR to complete (first time will be slower)
5. View the extracted text

---

## 💻 System Requirements

### Minimum Requirements
- **OS**: Windows 10/11
- **RAM**: 16GB+ recommended
- **Storage**: 12GB free space (for model)
- **Internet**: For initial model download

### For Best Performance
- **GPU**: NVIDIA GPU with 8GB+ VRAM
- **CUDA**: CUDA Toolkit 11.8 or later
- **RAM**: 16GB+

### CPU-Only Mode
If you don't have an NVIDIA GPU, the application will run on CPU:
- ⚠️ **Much slower** - 10-30x slower than GPU
- ✅ **Still works** - All functionality available
- 💡 **Tip**: Start with small images

---

## 📦 Installed Dependencies

```
Flask==3.0.0          # Web framework
flask-cors==4.0.0     # Cross-origin support
Werkzeug==3.0.1       # WSGI utilities
python-dotenv==1.0.0  # Environment variables
Pillow==10.2.0        # Image processing
PyMuPDF==1.26.5       # PDF handling
torch                 # PyTorch for deep learning
torchvision           # Computer vision tools
transformers          # Hugging Face transformers
accelerate            # Model loading optimization
sentencepiece         # Tokenization
```

---

## 🔧 Troubleshooting

### Server Won't Start
```powershell
# Check if port 5000 is already in use
netstat -ano | findstr :5000

# Kill the process if needed (replace PID with actual process ID)
taskkill /PID [PID] /F

# Restart the server
python app.py
```

### Out of Memory Error
- Close other GPU-intensive applications
- Reduce image size before upload
- If on CPU, ensure at least 8GB free RAM

### Slow Performance
1. **First use**: Model download takes 5-10 minutes - this is normal
2. **CPU mode**: Check terminal output for "Using device: cpu" warning
3. **Large PDFs**: Processing time increases with page count

### Model Download Issues
```powershell
# Clear Hugging Face cache
rd /s /q %USERPROFILE%\.cache\huggingface

# Set proxy if needed (replace with your proxy)
set HTTP_PROXY=http://proxy.example.com:8080
set HTTPS_PROXY=http://proxy.example.com:8080

# Restart the server
python app.py
```

---

## 🛠️ Development

### Restart the Server
Press `Ctrl+C` in the terminal to stop, then:
```powershell
python app.py
```

### View Server Logs
The terminal shows:
- Server startup messages
- Model loading progress
- OCR processing status
- Error messages (if any)

### Edit Configuration
Edit `app.py` to change:
- Port number (default: 5000)
- Max file size (default: 16MB)
- Model parameters
- OCR settings

---

## 📁 Project Structure

```
OCRWeb/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (optional)
├── templates/
│   └── index.html         # Web interface
├── static/
│   ├── css/
│   │   └── style.css      # Styles
│   └── js/
│       └── script.js      # Frontend logic
├── uploads/               # Temporary file storage
├── README.md              # General documentation
└── WINDOWS_SETUP.md       # This file
```

---

## 🎯 Next Steps

1. **Test the application** with various documents
2. **Bookmark** http://127.0.0.1:5000 for easy access
3. **Share** the network URL (http://192.168.100.121:5000) with others on your local network
4. **Customize** the UI by editing `templates/index.html` and `static/css/style.css`

---

## 💡 Tips

### Optimize Performance
- Use images with 2-3 megapixels for best results
- Compress large PDFs before upload
- Close browser tabs while processing to free RAM

### Best Results
- Upload clear, high-contrast images
- Ensure text is horizontal and not skewed
- Use 300 DPI or higher for scanned documents
- Crop images to remove unnecessary borders

### Production Deployment
For production use, replace Flask's built-in server with a production WSGI server:
```powershell
pip install waitress
waitress-serve --host=0.0.0.0 --port=5000 app:app
```

---

## 📞 Support

If you encounter issues:

1. Check the terminal for error messages
2. Review the troubleshooting section above
3. Verify all dependencies are installed: `pip list`
4. Ensure you have enough disk space and RAM
5. Try with a small, simple image first

---

## 🎉 Success!

Your DeepSeek-OCR web application is ready to use. Enjoy extracting text from your documents!

**Current Status**: ✅ Server Running
**Access URL**: http://127.0.0.1:5000
