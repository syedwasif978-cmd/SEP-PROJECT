@echo off
REM Quick start script for SEP-PROJECT
REM This script initializes the database and starts both backend and frontend servers

setlocal enabledelayedexpansion

echo.
echo ====================================================
echo   SEP-PROJECT: Quick Start
echo ====================================================
echo.

REM Set Python path
set PYTHON=C:/Users/DELL/AppData/Local/Python/pythoncore-3.14-64/python.exe
set PROJECT_PATH=%~dp0

echo [1/3] Checking Python installation...
%PYTHON% --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found at %PYTHON%
    pause
    exit /b 1
)
echo ✓ Python found

echo.
echo [2/3] Initializing database...
cd /d "%PROJECT_PATH%"
%PYTHON% init_db.py
if %errorlevel% neq 0 (
    echo ERROR: Database initialization failed
    pause
    exit /b 1
)
echo ✓ Database ready

echo.
echo [3/3] Starting services...
echo.
echo IMPORTANT: 
echo - Backend will serve the frontend at http://127.0.0.1:5000/
echo - When you run the backend it will attempt to open your default browser.
echo - If you prefer a separate static server, you can still run:
echo   cd "%PROJECT_PATH%Frontend"
echo   %PYTHON% -m http.server 5500
echo.
echo - Then open in browser: http://127.0.0.1:5000/
echo.
echo Press any key to start backend...
pause >nul

cd /d "%PROJECT_PATH%backend"
%PYTHON% app.py
