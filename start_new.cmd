@echo off
REM Procurement Management System - Quick Start
REM Navigate to backend directory and start Flask server

echo.
echo ========================================
echo Procurement Management System
echo Use Case-Driven Workflow (UC-01 to UC-08)
echo ========================================
echo.

cd /d "%~dp0backend"

echo Installing dependencies...
pip install -q -r requirements.txt

echo.
echo Starting Flask server...
echo Server will be available at: http://127.0.0.1:5000
echo.
echo Workflow Pages:
echo - Place Order:            http://127.0.0.1:5000/order.html
echo - Quotation Management:   http://127.0.0.1:5000/quotation.html
echo - Invoice Management:     http://127.0.0.1:5000/invoice.html
echo - Dashboard:              http://127.0.0.1:5000/
echo.
echo ========================================
echo.

python app.py

pause
