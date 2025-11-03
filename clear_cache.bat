@echo off
echo ================================================
echo DeepSeek-OCR Cache Cleaner
echo ================================================
echo.
echo This will clear the HuggingFace cache for DeepSeek-OCR
echo The model will need to re-download (~8GB) on next use
echo.
pause
echo.

python clear_model_cache.py

echo.
echo ================================================
pause
