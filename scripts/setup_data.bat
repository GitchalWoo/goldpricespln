@echo off
REM Quick setup script for fetching NBP gold prices (Windows)
REM Usage: setup_data.bat

echo.
echo 🏦 NBP Gold Price Setup
echo =============================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Python found
    echo.
    echo Installing Python dependencies...
    pip install -r scripts\requirements.txt
    echo.
    echo Fetching gold price data...
    python scripts\fetch_nbp_gold_prices.py -v
    echo.
    echo ✅ Data updated successfully!
    echo 📁 Output file: data\nbp-gold-prices.json
    goto done
)

REM Python not found
echo ❌ Python not found
echo.
echo Please install Python 3:
echo   https://www.python.org/downloads/
echo.
exit /b 1

:done
echo.
echo 🚀 Next steps:
echo   1. Start local server: npx http-server -p 8000
echo   2. Open browser: http://localhost:8000
echo.
