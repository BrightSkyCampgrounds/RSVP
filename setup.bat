@echo off
REM Setup script for Campspots application (Windows)

echo Setting up Campspots reservation system...

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Create .env if it doesn't exist
if not exist .env (
    echo Creating .env file...
    copy .env.example .env
    echo.
    echo WARNING: Edit .env file and add your Stripe API keys!
    echo Get them from: https://dashboard.stripe.com/test/apikeys
    echo.
)

REM Initialize database
echo Initializing database...
python init_db.py

echo.
echo Setup complete!
echo.
echo Next steps:
echo 1. Edit .env file and add your Stripe keys
echo 2. Activate virtual environment: venv\Scripts\activate
echo 3. Run the app: python app.py
echo 4. Visit: http://localhost:5000
echo.
pause
