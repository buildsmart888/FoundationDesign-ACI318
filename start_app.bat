@echo off
echo Stopping any existing Python processes...
taskkill /f /im python.exe >nul 2>&1

echo Waiting for cleanup...
timeout /t 2 >nul

echo Starting Foundation Design App...
py -m streamlit run "streamlit_app.py" --server.port 8501 --server.address localhost --server.headless true

pause
