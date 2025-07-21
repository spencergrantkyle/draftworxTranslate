# 🌍 Draftworx Translation Dashboard

A beautiful Streamlit application for visualizing and controlling the Draftworx translation process in real-time.

## 🚀 Features

### 📊 Real-time Dashboard
- **Live Progress Tracking**: Visual progress bars and metrics
- **Interactive Charts**: Plotly-powered analytics and progress visualization
- **Beautiful UI**: Modern, responsive design with custom styling

### 🔄 Translation Processing
- **Step-by-step Visualization**: See each translation as it happens
- **Real-time Updates**: Watch translations appear instantly
- **Pause/Resume**: Control processing at any time
- **Auto-save**: Automatic progress saving at configurable intervals

### 📈 Analytics & History
- **Processing Statistics**: Success rates, timing, and performance metrics
- **Translation History**: Complete record of all translations
- **Backup Management**: Easy access to all backup files
- **Progress Charts**: Visual representation of translation progress

### 💾 Data Management
- **Multiple File Support**: Load from CSV files or backup files
- **Resume Capability**: Continue from any backup point
- **Export Options**: Save progress at any time
- **File Preview**: Preview data before processing

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- Virtual environment (recommended)
- OpenAI API key configured

### Setup Steps

1. **Clone or navigate to the project directory**
   ```bash
   cd draftworx_translate
   ```

2. **Activate virtual environment**
   ```bash
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate     # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   - Ensure your `.env` file contains your OpenAI API key
   - The application will automatically load environment variables

## 🚀 Running the Application

### Method 1: Using the Launcher Script (Recommended)
```bash
python run_streamlit.py
```

### Method 2: Direct Streamlit Command
```bash
streamlit run streamlit_app.py
```

### Method 3: With Custom Configuration
```bash
streamlit run streamlit_app.py --server.port 8501 --server.address localhost
```

## 📖 Usage Guide

### 1. Dashboard Tab 📊
- **Load Data**: Click "🔄 Load Data" to load your CSV file
- **View Metrics**: See total records, progress, and translation counts
- **Progress Charts**: Interactive visualizations of translation progress
- **Data Preview**: Preview the first 10 records of your data

### 2. Processing Tab 🔄
- **Start Processing**: Begin the translation process
- **Pause/Resume**: Control processing at any time
- **Real-time Updates**: Watch translations happen live
- **Save Progress**: Manually save progress at any point

### 3. Analytics Tab 📈
- **Processing Statistics**: View success rates and timing
- **Performance Metrics**: Average processing time per record
- **Progress Charts**: Historical view of translation progress
- **Time Analysis**: Processing patterns and trends

### 4. History Tab 📋
- **Recent Translations**: View the last 10 translations with details
- **Backup Files**: Access and load from any backup file
- **Translation Details**: See English/Afrikaans pairs and formulas
- **File Management**: Load, compare, and manage backup files

## ⚙️ Configuration Options

### Sidebar Settings
- **Input File**: Select from available CSV files
- **Backup Resume**: Choose a backup file to resume from
- **Save Interval**: Set how often to auto-save (1-20 records)
- **Auto-save**: Enable/disable automatic progress saving

### Processing Controls
- **Start/Pause**: Control processing flow
- **Manual Save**: Save progress at any time
- **Real-time Updates**: See translations as they happen

## 🎨 UI Features

### Custom Styling
- **Gradient Headers**: Beautiful gradient text effects
- **Metric Cards**: Colorful metric displays
- **Progress Sections**: Highlighted progress areas
- **Translation Cards**: Organized translation displays

### Color Coding
- **English Text**: Blue background with left border
- **Afrikaans Text**: Purple background with left border
- **Formulas**: Orange background with monospace font
- **Success/Error**: Green/red status indicators

### Responsive Design
- **Wide Layout**: Optimized for large screens
- **Tabbed Interface**: Organized into logical sections
- **Sidebar Configuration**: Easy access to settings
- **Mobile Friendly**: Works on various screen sizes

## 📊 Data Visualization

### Progress Charts
- **Pie Charts**: Translation progress overview
- **Bar Charts**: Processing rate over time
- **Gauge Charts**: Success rate indicators
- **Line Charts**: Historical progress tracking

### Real-time Metrics
- **Live Counters**: Updated in real-time
- **Progress Bars**: Visual progress indicators
- **Status Indicators**: Success/failure tracking
- **Time Tracking**: Elapsed time and estimates

## 🔧 Troubleshooting

### Common Issues

1. **"Module not found" errors**
   - Ensure virtual environment is activated
   - Run `pip install -r requirements.txt`

2. **OpenAI API errors**
   - Check your `.env` file has the correct API key
   - Verify API key has sufficient credits

3. **File not found errors**
   - Ensure CSV files are in the correct directories
   - Check file paths in the sidebar

4. **Streamlit not starting**
   - Check if port 8501 is available
   - Try a different port: `streamlit run streamlit_app.py --server.port 8502`

### Performance Tips

1. **Large Files**: For files with >1000 records, increase save interval
2. **Memory Usage**: Close other applications to free up memory
3. **Network**: Ensure stable internet connection for API calls
4. **Browser**: Use Chrome or Firefox for best performance

## 🔄 Integration with Existing Scripts

The Streamlit app uses the same core functions as your existing `translate.py` script:
- `translate_english_value()` from `test_prompts.py`
- `translate_formula()` from `test_prompts.py`
- `CSVReader` class from `csv_reader.py`

This ensures consistency between command-line and web interfaces.

## 📁 File Structure

```
draftworx_translate/
├── streamlit_app.py          # Main Streamlit application
├── run_streamlit.py          # Launcher script
├── requirements.txt          # Updated dependencies
├── translate.py              # Original command-line script
├── test_prompts.py           # Translation functions
├── csv_reader.py             # CSV handling
├── SheetFlatFiles/           # Input/output CSV files
├── Backup_OutputResults/     # Backup files
└── Knowledge/                # Documentation files
```

## 🎯 Best Practices

1. **Start Small**: Test with a small dataset first
2. **Monitor Progress**: Use the analytics tab to track performance
3. **Regular Saves**: Enable auto-save to prevent data loss
4. **Backup Management**: Use backup files to resume interrupted work
5. **API Limits**: Be mindful of OpenAI API rate limits

## 🆘 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review the console output for error messages
3. Ensure all dependencies are installed correctly
4. Verify your OpenAI API key is valid and has credits

## 🚀 Future Enhancements

Potential improvements for future versions:
- **Batch Processing**: Process multiple files simultaneously
- **Advanced Analytics**: More detailed performance metrics
- **Export Options**: Additional output formats
- **User Management**: Multi-user support
- **API Optimization**: Caching and rate limiting improvements 