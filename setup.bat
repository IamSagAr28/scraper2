@echo off
echo Setting up Court Cause List Fetcher...
echo.

echo Installing backend dependencies...
cd backend
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Failed to install backend dependencies
    pause
    exit /b 1
)
cd ..

echo.
echo Installing frontend dependencies...
cd frontend
npm install
if %errorlevel% neq 0 (
    echo Failed to install frontend dependencies
    pause
    exit /b 1
)
cd ..

echo.
echo Setup completed successfully!
echo.
echo To run the application:
echo 1. Backend: cd backend && python main.py
echo 2. Frontend: cd frontend && npm start
echo.
pause
