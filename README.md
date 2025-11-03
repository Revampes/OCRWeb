# DeepSeek OCR Web Application# DeepSeek OCR Web Application



A modern web application that uses **DeepSeek-OCR** AI model locally to extract text from images and PDF documents.A modern, user-friendly web application that uses DeepSeek's AI-powered OCR model to extract text from images and documents.



![DeepSeek OCR](https://img.shields.io/badge/AI-DeepSeek%20OCR-blue)![DeepSeek OCR](https://img.shields.io/badge/AI-DeepSeek%20OCR-blue)

![Python](https://img.shields.io/badge/Python-3.8+-green)![Python](https://img.shields.io/badge/Python-3.8+-green)

![Flask](https://img.shields.io/badge/Flask-3.0.0-lightgrey)![Flask](https://img.shields.io/badge/Flask-3.0.0-lightgrey)

![Windows](https://img.shields.io/badge/Platform-Windows-blue)

# DeepSeek OCR Web Application

## ✨ Features

A modern web application that uses **DeepSeek-OCR** AI model locally to extract text from images and PDF documents.

- 🖼️ **Multi-format Support** - PNG, JPG, JPEG, GIF, BMP, TIFF, WEBP, PDF

- 🤖 **DeepSeek-OCR Model** - Uses the official DeepSeek-OCR model locally![DeepSeek OCR](https://img.shields.io/badge/AI-DeepSeek%20OCR-blue)

- 🎨 **Modern UI** - Beautiful, responsive interface with drag-and-drop support![Python](https://img.shields.io/badge/Python-3.8+-green)

- 📋 **Easy Export** - Copy to clipboard or download as text file![Flask](https://img.shields.io/badge/Flask-3.0.0-lightgrey)

- 🔒 **Privacy First** - Everything runs locally, no data sent to external servers

- ⚡ **High Accuracy** - DeepSeek-OCR provides state-of-the-art OCR results## ✨ Features

- 🆓 **No API Key Required** - Runs completely offline after initial model download

- 💻 **Windows Compatible** - Optimized for Windows 10/11- 🖼️ **Multi-format Support** - PNG, JPG, JPEG, GIF, BMP, TIFF, WEBP, PDF

- 🤖 **DeepSeek-OCR Model** - Uses the actual DeepSeek-OCR local model with vLLM

## 🚀 Quick Start- 🎨 **Modern UI** - Beautiful, responsive interface with drag-and-drop support

- 📋 **Easy Export** - Copy to clipboard or download as text file

### Prerequisites- 🔒 **Privacy First** - Everything runs locally, no data sent to external APIs

- ⚡ **High Accuracy** - DeepSeek-OCR provides state-of-the-art OCR results

- **Python 3.8 or higher** (tested with Python 3.13)- 🆓 **No API Key Required** - Runs completely offline

- **16GB RAM** recommended

- **NVIDIA GPU** with 8GB+ VRAM (optional but highly recommended)## 🚀 Quick Start

- **12GB free disk space** (for model cache)

- **Internet connection** (for initial model download)### Prerequisites



### Installation- Python 3.8 or higher

- CUDA-capable GPU (recommended for faster processing)

1. **Navigate to project directory**- At least 8GB GPU memory

   ```powershell- DeepSeek-OCR repository files (provided in `c:\Users\user\Desktop\DeepSeek-OCR-main`)

   cd c:\Users\user\Downloads\OCRWeb

   ```### Installation



2. **Install dependencies**1. **Navigate to project directory**

   ```powershell   ```powershell

   pip install -r requirements.txt   cd c:\Users\user\Downloads\OCRWeb

   ```   ```



   This will install:2. **Install dependencies**

   - Flask (web framework)   ```powershell

   - PyTorch (deep learning)   pip install -r requirements.txt

   - Transformers (model loading)   ```

   - PyMuPDF (PDF handling)

   - And other required libraries3. **Install vLLM requirements** (from DeepSeek-OCR repository)

   ```powershell

### Running the Application   cd c:\Users\user\Desktop\DeepSeek-OCR-main\DeepSeek-OCR-master\DeepSeek-OCR-vllm

   pip install -r requirements.txt

1. **Start the Flask server**   ```

   ```powershell

   python app.py### Running the Application

   ```

1. **Start the Flask server**

2. **Open your browser**   ```powershell

      cd c:\Users\user\Downloads\OCRWeb

   Navigate to: **http://localhost:5000**   python app.py

   ```

3. **Start scanning!**

   - Upload or drag-and-drop an image/PDF2. **Open your browser**

   - Click "Scan Document"   

   - Wait for processing (first time takes 5-10 minutes to download model)   Navigate to: `http://localhost:5000`

   - View, copy, or download the extracted text

3. **Start scanning!**

## 📖 Documentation   - Upload or drag-and-drop an image/PDF

   - Click "Scan Document"

- **QUICK_START.md** - Get started in 5 minutes   - View, copy, or download the extracted text

- **WINDOWS_SETUP.md** - Detailed Windows setup and troubleshooting guide

- **This README** - General overview and features## ⚠️ Important Note About DeepSeek-OCR



## ⚙️ How It Works- 🖼️ **Multi-format Support** - PNG, JPG, JPEG, GIF, BMP, TIFF, WEBP, PDF

- 🤖 **AI-Powered OCR** - Leverages DeepSeek's advanced OCR model

### Local Model Processing- 🎨 **Modern UI** - Beautiful, responsive interface with drag-and-drop support

- 📋 **Easy Export** - Copy to clipboard or download as text file

1. **First Use**- 🔒 **Privacy First** - API keys are not stored, files are deleted after processing

   - Downloads DeepSeek-OCR model (~8GB) from Hugging Face- ⚡ **Fast Processing** - Instant results with real-time feedback

   - Caches model to `C:\Users\[username]\.cache\huggingface`

   - Takes 5-10 minutes depending on internet speed## 🚀 Quick Start



2. **Subsequent Uses**### Prerequisites

   - Loads model from local cache

   - No internet required- Python 3.8 or higher

   - Takes 30-60 seconds to load into memory- DeepSeek API key (get one at [platform.deepseek.com](https://platform.deepseek.com))



3. **Processing**### Installation

   - Converts images/PDFs to compatible format

   - Runs DeepSeek-OCR inference1. **Clone or download this repository**

   - Returns extracted text   ```powershell

   cd c:\Users\user\Downloads\OCRWeb

### GPU vs CPU   ```



The application automatically detects your hardware:2. **Create a virtual environment (recommended)**

   ```powershell

- **NVIDIA GPU** (CUDA available):   python -m venv venv

  - ✅ Fast processing (seconds per page)   .\venv\Scripts\Activate.ps1

  - ✅ Handles large documents   ```

  - ✅ Recommended configuration

3. **Install dependencies**

- **CPU only** (no CUDA):   ```powershell

  - ⚠️ Slower processing (minutes per page)   pip install -r requirements.txt

  - ⚠️ Higher memory usage   ```

  - ✅ Still functional

4. **Configure API Key (Optional)**

## 📁 Project Structure   

   You can either:

```   - Enter your API key in the web interface each time, or

OCRWeb/   - Create a `.env` file for persistent configuration:

│   

├── app.py                    # Flask backend with DeepSeek-OCR integration   ```powershell

├── requirements.txt          # Python dependencies   copy .env.example .env

├── README.md                 # This file   ```

├── QUICK_START.md            # Quick start guide   

├── WINDOWS_SETUP.md          # Detailed Windows guide   Then edit `.env` and add your DeepSeek API key:

│   ```

├── templates/   DEEPSEEK_API_KEY=your_actual_api_key_here

│   └── index.html            # Web interface   ```

│

├── static/### Running the Application

│   ├── css/

│   │   └── style.css         # Stylesheet1. **Start the Flask server**

│   └── js/   ```powershell

│       └── script.js         # Frontend JavaScript   python app.py

│   ```

└── uploads/                  # Temporary upload directory (auto-created)

```2. **Open your browser**

   

## 🎯 Usage Tips   Navigate to: `http://localhost:5000`



### For Best Results3. **Start scanning!**

   - Enter your DeepSeek API key (if not in .env)

1. **Image Quality**   - Upload or drag-and-drop an image/PDF

   - Use 300 DPI or higher for scanned documents   - Click "Scan Document"

   - Ensure good lighting and contrast   - View, copy, or download the extracted text

   - Keep text horizontal (not rotated)

## 📁 Project Structure

2. **File Size**

   - Compress large PDFs before upload```

   - Use 2-3 megapixel images for optimal speedOCRWeb/

   - Maximum file size: 16MB│

├── app.py                 # Flask backend application

3. **Document Types**├── requirements.txt       # Python dependencies

   - Printed text works best├── .env.example          # Environment variable template

   - Handwriting may have lower accuracy├── .gitignore           # Git ignore rules

   - Tables and structured data are supported├── README.md            # This file

│

### Performance Optimization├── templates/

│   └── index.html       # Main HTML template

- **Close other applications** when processing large documents│

- **Use GPU** whenever possible for 10-30x speedup├── static/

- **Process one document at a time** for best results│   ├── css/

│   │   └── style.css    # Stylesheet

## 🔧 Configuration│   └── js/

│       └── script.js    # Frontend JavaScript

### Supported File Formats│

└── uploads/             # Temporary upload directory (auto-created)

- **Images**: PNG, JPG, JPEG, GIF, BMP, TIFF, WEBP```

- **Documents**: PDF (multi-page support)

- **Maximum file size**: 16MB## 🔧 Configuration



### Changing Settings### Environment Variables



Edit `app.py` to modify:Create a `.env` file with:



```python```env

# Port number (default: 5000)DEEPSEEK_API_KEY=your_api_key_here

app.run(debug=True, host='0.0.0.0', port=5000)```



# Maximum file size (default: 16MB)### Supported File Formats

MAX_FILE_SIZE = 16 * 1024 * 1024

- **Images**: PNG, JPG, JPEG, GIF, BMP, TIFF, WEBP

# Allowed file extensions- **Documents**: PDF

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'webp', 'pdf'}- **Maximum file size**: 16MB

```

## 🌐 API Endpoints

## 🌐 API Endpoints

### Health Check

### Health Check```

```GET /api/health

GET /api/health```

Returns server status.

Response:

{### OCR Processing

  "status": "ok",```

  "message": "Server is running"POST /api/ocr

}Content-Type: multipart/form-data

```

Parameters:

### OCR Processing- file: Image or PDF file (required)

```- api_key: DeepSeek API key (optional if set in .env)

POST /api/ocr```

Content-Type: multipart/form-data

## 🎯 Usage Tips

Parameters:

- file: Image or PDF file (required)1. **Best Results**: Use clear, well-lit images with readable text

2. **Multiple Documents**: Process documents one at a time for best accuracy

Response (Success):3. **Tables**: The OCR model preserves table structure when possible

{4. **Languages**: Supports multiple languages depending on DeepSeek's model capabilities

  "success": true,

  "text": "Extracted text content...",## 🛠️ Troubleshooting

  "filename": "document.pdf"

}### Port Already in Use

If port 5000 is busy, modify `app.py`:

Response (Error):```python

{app.run(debug=True, host='0.0.0.0', port=5001)  # Change port number

  "error": "Error message here"```

}

```### API Key Issues

- Ensure your DeepSeek API key is valid

## 🛠️ Troubleshooting- Check you have sufficient credits at [platform.deepseek.com](https://platform.deepseek.com)

- Verify the key is correctly entered (no extra spaces)

### Common Issues

### Upload Errors

1. **"No module named 'torch'"**- Check file size is under 16MB

   ```powershell- Ensure file format is supported

   pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118- Try a different image if processing fails

   ```

## 🔒 Security Notes

2. **"Model download failed"**

   - Check internet connection- API keys entered in the web interface are not stored on the server

   - Ensure 12GB free disk space- Uploaded files are automatically deleted after processing

   - Try clearing cache: `rd /s /q %USERPROFILE%\.cache\huggingface`- Use HTTPS in production environments

- Never commit `.env` files to version control

3. **"Out of memory"**

   - Close other applications## 📝 Development

   - Use smaller images

   - Consider upgrading to GPU with more VRAMTo run in development mode with auto-reload:



4. **"Port 5000 already in use"**```powershell

   ```powershell# Activate virtual environment

   # Find and kill the process.\venv\Scripts\Activate.ps1

   netstat -ano | findstr :5000

   taskkill /PID [PID] /F# Set Flask environment (optional)

   ```$env:FLASK_ENV="development"



See **WINDOWS_SETUP.md** for detailed troubleshooting.# Run the app

python app.py

## 🚀 Deployment```



### Development## 🤝 Contributing

```powershell

python app.pyContributions are welcome! Feel free to:

```- Report bugs

Access at: http://localhost:5000- Suggest new features

- Submit pull requests

### Production

## 📄 License

For production deployment, use a WSGI server:

This project is open source and available under the MIT License.

```powershell

pip install waitress## 🙏 Acknowledgments

waitress-serve --host=0.0.0.0 --port=5000 app:app

```- [DeepSeek AI](https://www.deepseek.com/) for the OCR model

- [Flask](https://flask.palletsprojects.com/) for the web framework

## 🔒 Security & Privacy- [Font Awesome](https://fontawesome.com/) for icons



- ✅ **No API keys required** - Runs completely offline## 📞 Support

- ✅ **Local processing** - No data sent to external servers

- ✅ **Auto-cleanup** - Uploaded files deleted after processing- **DeepSeek API**: [platform.deepseek.com](https://platform.deepseek.com)

- ✅ **No tracking** - No usage data collected- **Documentation**: [DeepSeek API Docs](https://platform.deepseek.com/docs)



## 📝 Development---



### Technology StackMade with ❤️ using DeepSeek AI


- **Backend**: Flask 3.0.0
- **AI Model**: DeepSeek-OCR (via Hugging Face Transformers)
- **Deep Learning**: PyTorch
- **PDF Processing**: PyMuPDF
- **Image Processing**: Pillow
- **Frontend**: HTML5, CSS3, JavaScript

### Contributing

Contributions are welcome! Areas for improvement:
- Multi-language support
- Batch processing
- OCR confidence scores
- Advanced PDF features
- UI enhancements

## 🔄 Recent Changes

### Version 2.0 (Current)

- ✅ **Windows compatibility** - Fixed vLLM installation issues
- ✅ **Simplified installation** - Uses transformers library directly
- ✅ **Better error handling** - Clearer error messages
- ✅ **Improved documentation** - Comprehensive guides added

### Version 1.0 (Original)

- ❌ Used vLLM (Linux-only)
- ❌ Complex setup process
- ❌ Windows installation failures

## 🙏 Acknowledgments

- [DeepSeek AI](https://www.deepseek.com/) - For the excellent OCR model
- [Hugging Face](https://huggingface.co/) - For model hosting and transformers library
- [Flask](https://flask.palletsprojects.com/) - For the web framework
- [PyTorch](https://pytorch.org/) - For deep learning framework

## 📞 Resources

- **DeepSeek-OCR Model**: [huggingface.co/deepseek-ai/DeepSeek-OCR](https://huggingface.co/deepseek-ai/DeepSeek-OCR)
- **Project Repository**: Located at `c:\Users\user\Downloads\OCRWeb`
- **Model Cache**: `C:\Users\[username]\.cache\huggingface`

## 📄 License

This project is open source and available under the MIT License.

---

Made with ❤️ using DeepSeek AI

**Status**: ✅ Ready to Use  
**Version**: 2.0 (Windows Compatible)  
**Last Updated**: November 2025
