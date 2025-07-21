#!/usr/bin/env python3
"""
Launcher script for the Draftworx Translation Streamlit Application
"""

import subprocess
import sys
import os

def main():
    """Launch the Streamlit application"""
    
    # Check if we're in the correct directory
    if not os.path.exists("streamlit_app.py"):
        print("Error: streamlit_app.py not found in current directory")
        print("Please run this script from the project root directory")
        sys.exit(1)
    
    # Check if virtual environment is activated
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("Warning: Virtual environment not detected")
        print("It's recommended to activate your virtual environment first:")
        print("  source venv/bin/activate  # On macOS/Linux")
        print("  venv\\Scripts\\activate     # On Windows")
    
    print("🚀 Launching Draftworx Translation Dashboard...")
    print("📊 The application will open in your default web browser")
    print("🌐 If it doesn't open automatically, go to: http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop the application")
    print("-" * 60)
    
    try:
        # Launch Streamlit with custom configuration
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error launching application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 