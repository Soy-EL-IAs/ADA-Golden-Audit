@echo off
cd /d "%~dp0"
echo Starting ADA App v0.1...
echo Checking dependencies...
python -c "import fastapi, uvicorn" >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: FastAPI or Uvicorn not found.
    echo Please run: pip install fastapi uvicorn
    pause
    exit /b 1
)

echo Starting server...
start "ADA App Server" python ada.py serve --host 127.0.0.1 --port 8000 --reload

echo Waiting for server to start...
timeout /t 3 /nobreak >nul

echo Opening browser...
start http://127.0.0.1:8000

echo ADA App is running at http://127.0.0.1:8000
echo Close this window to stop the launcher (the server will keep running in its own window).
pause
