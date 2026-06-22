@echo off
setlocal
title SmartGov Startup Manager
color 0A

echo ======================================================
echo           SMARTGOV PROJECT - STARTUP MANAGER
echo ======================================================
echo.

echo [1/4] Navigating to project directory...
D:
cd "C:\Users\niran\Documents\MY PROJECTS\smart_gov"
if %errorlevel% neq 0 (
    color 0C
    echo [ERROR] Could not find D:\FINAL_CODE
    pause
    exit /b
)
echo [DONE] Switched to D:\FINAL_CODE
echo.

echo [2/4] Activating virtual environment ('career')...
if not exist "career\Scripts\activate.bat" (
    color 0C
    echo [ERROR] Virtual environment 'career' not found!
    pause
    exit /b
)
call "career\Scripts\activate"
echo [DONE] Virtual environment activated.
echo.

echo [3/4] Preparing to launch application...
echo.
echo ======================================================
echo   🚀 APP IS STARTING! 
echo.
echo   🔗 URL: http://127.0.0.1:5000
echo   👤 Admin Username: admin
echo   🔑 Admin Password: admin123
echo.
echo   (Press Ctrl+C to stop the server)
echo ======================================================
echo.

echo [4/4] Running python app.py...
python app.py

if %errorlevel% neq 0 (
    color 0C
    echo.
    echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    echo   [CRITICAL ERROR] Application stopped unexpectedly.
    echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    pause
)

endlocal
