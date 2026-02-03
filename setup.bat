@echo off
echo ============================================
echo Chemical Equipment Visualizer - Setup
echo ============================================
echo.

echo Step 1: Setting up Backend...
cd backend
echo Creating virtual environment...
python -m venv venv
call venv\Scripts\activate
echo Installing dependencies...
pip install -r requirements.txt
echo Running migrations...
python manage.py makemigrations
python manage.py migrate
echo.
echo Backend setup complete!
echo.
echo Step 2: Setting up Web Frontend...
cd ..\frontend-web
echo Installing npm dependencies...
call npm install
echo.
echo Web frontend setup complete!
echo.
echo Step 3: Setting up Desktop Frontend...
cd ..\frontend-desktop
echo Creating virtual environment...
python -m venv venv
call venv\Scripts\activate
echo Installing dependencies...
pip install -r requirements.txt
cd ..
echo.
echo Desktop frontend setup complete!
echo.
echo ============================================
echo Setup Complete!
echo ============================================
echo.
echo To start the application:
echo.
echo 1. Backend (Terminal 1):
echo    cd backend
echo    venv\Scripts\activate
echo    python manage.py runserver
echo.
echo 2. Web Frontend (Terminal 2):
echo    cd frontend-web
echo    npm start
echo.
echo 3. Desktop Application (Terminal 3):
echo    cd frontend-desktop
echo    venv\Scripts\activate
echo    python main.py
echo.
echo See README.md for more details.
echo.
pause
