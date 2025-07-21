#!/usr/bin/env python3
"""
Demo script for the Draftworx Translation Streamlit Application
Shows how to use the application with sample data
"""

import pandas as pd
import os

def create_sample_data():
    """Create sample data for demonstration"""
    
    # Sample data that mimics the structure of your translation files
    sample_data = {
        'CellValue_English': [
            "The directors are responsible for the preparation and fair presentation of the financial statements.",
            "These financial statements have been prepared in accordance with International Financial Reporting Standards.",
            "The company's principal activities are the provision of financial services.",
            "Revenue is recognised when the performance obligation is satisfied.",
            "The carrying amount of property, plant and equipment is reviewed annually."
        ],
        'CellFormula_English': [
            '="The directors are responsible for the preparation and fair presentation of the "&LOWER(GroupAFSPrefix)&"financial statements."',
            '="These "&LOWER(GroupAFSPrefix)&"financial statements have been prepared in accordance with International Financial Reporting Standards."',
            '="The "&GroupEntityCase&" principal activities are the provision of financial services."',
            '="Revenue is recognised when the performance obligation is satisfied."',
            '="The carrying amount of property, plant and equipment is reviewed annually."'
        ],
        'CellValue_Afrikaans': [''] * 5,  # Empty for demonstration
        'CellFormula_Afrikaans': [''] * 5  # Empty for demonstration
    }
    
    return pd.DataFrame(sample_data)

def main():
    """Main demo function"""
    
    print("🌍 Draftworx Translation Streamlit Demo")
    print("=" * 50)
    
    # Create sample data
    print("📝 Creating sample data...")
    sample_df = create_sample_data()
    
    # Save sample data
    sample_file = "SheetFlatFiles/sample_directors.csv"
    os.makedirs("SheetFlatFiles", exist_ok=True)
    sample_df.to_csv(sample_file, index=False, encoding='utf-8')
    
    print(f"✅ Sample data saved to: {sample_file}")
    print(f"📊 Sample data contains {len(sample_df)} records")
    
    print("\n🚀 To run the Streamlit application:")
    print("1. Activate your virtual environment:")
    print("   source venv/bin/activate")
    print("\n2. Run the launcher script:")
    print("   python run_streamlit.py")
    print("\n3. Or run Streamlit directly:")
    print("   streamlit run streamlit_app.py")
    
    print("\n📖 Usage instructions:")
    print("1. Open the Dashboard tab")
    print("2. Click 'Load Data' to load the sample file")
    print("3. Go to the Processing tab")
    print("4. Click 'Start Processing' to begin translation")
    print("5. Watch the real-time translation process!")
    
    print("\n🎯 Features to try:")
    print("- Pause/Resume processing")
    print("- View real-time progress charts")
    print("- Check the Analytics tab for statistics")
    print("- Explore the History tab for translation details")
    print("- Save progress and resume from backups")
    
    print("\n💡 Tips:")
    print("- The app uses the same OpenAI API as your existing script")
    print("- Make sure your .env file has your OpenAI API key")
    print("- Processing can be paused and resumed at any time")
    print("- All progress is automatically saved to backup files")
    
    print("\n" + "=" * 50)
    print("🎉 Demo setup complete! Ready to launch Streamlit app.")

if __name__ == "__main__":
    main() 