@echo off
echo Installing DeepSeek OCR Web Application...
echo.

REM Install Python packages
echo Installing required Python packages...
pip install Flask==3.0.0
pip install flask-cors==4.0.0
pip install openai==1.12.0
pip install Werkzeug==3.0.1
pip install python-dotenv==1.0.0

echo.
echo Installation complete!
echo.
echo To run the application, execute: python app.py
echo Then open your browser to: http://localhost:5000
pause
