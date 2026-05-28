@echo off
echo ========================================================
echo   Double-Marking AI Agent Automation
echo   Keele University Computer Science Department
echo ========================================================
echo.
echo Choose deployment mode:
echo   [1] Local Access Only (recommended for individual use)
echo   [2] Network Access (for department-wide deployment)
echo.
set /p mode="Enter your choice (1-2): "

cd /d "C:\MSc Project\agent"

if "%mode%"=="1" (
    echo.
    echo Starting Double-Marking AI Agent - Local Mode...
    echo Access at: http://localhost:8501
    echo ========================================================
    python -m streamlit run app/main.py --server.port 8501
) else if "%mode%"=="2" (
    echo.
    echo Starting Double-Marking AI Agent - Network Mode...
    echo Local Access: http://localhost:8501
    echo Network Access: http://10.167.71.152:8501
    echo ========================================================
    python -m streamlit run app/main.py --server.address 0.0.0.0 --server.port 8501
) else (
    echo Invalid choice. Starting Double-Marking AI Agent - Local Mode...
    echo Access at: http://localhost:8501
    echo ========================================================
    python -m streamlit run app/main.py --server.port 8501
)

echo.
echo Agent stopped. Press any key to close...
pause