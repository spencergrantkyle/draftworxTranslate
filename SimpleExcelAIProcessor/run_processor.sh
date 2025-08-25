#!/bin/bash

echo "Simple Excel AI Processor"
echo "========================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.7+ and try again"
    exit 1
fi

# Check if requirements are installed
echo "Checking dependencies..."
if ! python3 -c "import pandas" &> /dev/null; then
    echo "Installing dependencies..."
    pip3 install -r simple_requirements.txt
    if [ $? -ne 0 ]; then
        echo "Error: Failed to install dependencies"
        exit 1
    fi
fi

# Check if OpenAI API key is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "Warning: OPENAI_API_KEY environment variable not set"
    echo "Please set your OpenAI API key before running the processor"
    echo
    read -p "Enter your OpenAI API key (or press Enter to skip): " api_key
    if [ ! -z "$api_key" ]; then
        export OPENAI_API_KEY="$api_key"
    fi
fi

echo
echo "Starting Excel AI Processor..."
echo
python3 simple_excel_ai_processor.py

echo
echo "Processing complete!" 