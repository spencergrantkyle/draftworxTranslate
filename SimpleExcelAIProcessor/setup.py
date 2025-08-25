#!/usr/bin/env python3
"""
Setup script for Simple Excel AI Processor
"""

import os
import sys
import subprocess

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("Error: Python 3.7 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✓ Python version: {sys.version.split()[0]}")
    return True

def install_requirements():
    """Install required packages"""
    try:
        print("Installing required packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "simple_requirements.txt"])
        print("✓ All packages installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing packages: {e}")
        return False

def create_env_file():
    """Create .env file template"""
    env_content = """# OpenAI API Configuration
# Get your API key from: https://platform.openai.com/api-keys
OPENAI_API_KEY=your-api-key-here

# Optional: Set default model (default: gpt-4o)
OPENAI_MODEL=gpt-4o
"""
    
    if not os.path.exists(".env"):
        with open(".env", "w") as f:
            f.write(env_content)
        print("✓ Created .env file template")
        print("  Please edit .env and add your OpenAI API key")
    else:
        print("✓ .env file already exists")

def test_installation():
    """Test if everything is working"""
    try:
        import pandas
        import openpyxl
        from openai import OpenAI
        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def main():
    """Main setup function"""
    print("=== Simple Excel AI Processor Setup ===\n")
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install requirements
    if not install_requirements():
        return False
    
    # Create environment file
    create_env_file()
    
    # Test installation
    if not test_installation():
        return False
    
    print("\n=== Setup Complete! ===")
    print("\nNext steps:")
    print("1. Edit .env file and add your OpenAI API key")
    print("2. Run: python simple_excel_ai_processor.py")
    print("3. Or use the batch/shell scripts for easy execution")
    print("\nFor help, see README.md")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1) 