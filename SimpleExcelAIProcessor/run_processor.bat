@echo off
echo Simple Excel AI Processor
echo ========================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.7+ and try again
    pause
    exit /b 1
)

REM Check if requirements are installed
echo Checking dependencies...
pip show pandas >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r simple_requirements.txt
    if errorlevel 1 (
        echo Error: Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Check if OpenAI API key is set
if "%OPENAI_API_KEY%"=="" (
    echo Warning: OPENAI_API_KEY environment variable not set
    echo Please set your OpenAI API key before running the processor
    echo.
    set /p api_key="Enter your OpenAI API key (or press Enter to skip): "
    if not "%api_key%"=="" (
        set OPENAI_API_KEY=%api_key%
    )
)

echo.
echo Starting Excel AI Processor...
echo.
python simple_excel_ai_processor.py

echo.
echo Processing complete!
pause 