@echo off
echo ========================================
echo Techlynx Pro Django Setup Script
echo ========================================
echo.

echo [1/6] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)
echo Virtual environment created successfully!
echo.

echo [2/6] Activating virtual environment...
call venv\Scripts\activate.bat
echo.

echo [3/6] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo Dependencies installed successfully!
echo.

echo [4/6] Creating migrations...
python manage.py makemigrations
python manage.py makemigrations website
echo.

echo [5/6] Running migrations...
python manage.py migrate
if errorlevel 1 (
    echo ERROR: Failed to run migrations
    pause
    exit /b 1
)
echo Database migrations completed!
echo.

echo [6/6] Creating superuser...
echo Please enter your admin credentials:
python manage.py createsuperuser
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To start the development server, run:
echo   python manage.py runserver
echo.
echo Then visit: http://127.0.0.1:8000
echo Admin panel: http://127.0.0.1:8000/admin
echo.
pause
