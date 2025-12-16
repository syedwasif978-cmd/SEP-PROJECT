@echo off
cd /d "%~dp0backend"
echo Starting Procurement Management System...
echo.
echo Browser will open at: http://127.0.0.1:5000
echo.
pip install -q -r requirements.txt
python app.py
