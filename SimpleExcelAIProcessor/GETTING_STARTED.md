# Getting Started with Simple Excel AI Processor

## 🎯 What You'll Learn

This guide will walk you through the complete process of setting up and using the Simple Excel AI Processor to process Excel cells through OpenAI's API.

## 📋 Prerequisites

Before you begin, make sure you have:

- **Python 3.7 or higher** installed on your system
- **An OpenAI API key** (get one from [OpenAI Platform](https://platform.openai.com/api-keys))
- **An Excel file** with data you want to process

## 🚀 Step-by-Step Setup

### Step 1: Extract and Navigate
1. Extract the `SimpleExcelAIProcessor` folder to your desired location
2. Open a terminal/command prompt
3. Navigate to the `SimpleExcelAIProcessor` folder:
   ```bash
   cd path/to/SimpleExcelAIProcessor
   ```

### Step 2: Run Setup
Choose one of these methods:

**Option A: Automated Setup (Recommended)**
```bash
python setup.py
```

**Option B: Platform-Specific Launcher**
- **Windows:** Double-click `run_processor.bat`
- **Mac/Linux:** Run `./run_processor.sh`

**Option C: Manual Setup**
```bash
pip install -r simple_requirements.txt
```

### Step 3: Configure API Key
1. Copy `env_example.txt` to `.env`:
   ```bash
   cp env_example.txt .env
   ```
2. Edit the `.env` file and replace `your-api-key-here` with your actual OpenAI API key

### Step 4: Test the Setup
1. Create test data:
   ```bash
   python create_test_file.py
   ```
2. Run the processor:
   ```bash
   python simple_excel_ai_processor.py
   ```
3. Follow the prompts:
   - File: `test_data.xlsx`
   - Sheet: `TestData`
   - Range: `A1:A10`
   - Prompt: `"Translate this text to Spanish"`

## 📊 Understanding the Output

After processing, you'll get a new Excel file named `[original_filename]_AI_Results.xlsx` with these columns:

| Column | Example |
|--------|---------|
| Sheet Name | `TestData` |
| Cell Reference | `A1` |
| Cell Value | `Hello World` |
| Cell Formula | `=A1` (if applicable) |
| API Response | `Hola Mundo` |

## 🎯 Common Workflows

### Translation Workflow
1. **Input:** Excel file with text in column A
2. **Range:** `A1:A50`
3. **Prompt:** `"Translate this text to French"`
4. **Output:** Translated text in the API Response column

### Analysis Workflow
1. **Input:** Excel file with financial data
2. **Range:** `B1:B100`
3. **Prompt:** `"Analyze this financial value and provide insights"`
4. **Output:** Analysis and insights for each value

### Formula Analysis Workflow
1. **Input:** Excel file with formulas
2. **Range:** `C1:C20`
3. **Prompt:** `"Explain what this Excel formula calculates"`
4. **Output:** Formula explanations and potential improvements

## 🔧 Customization Options

### Change the AI Model
Edit the `model` parameter in the script:
```python
results = processor.process_cell_range(
    workbook_path, sheet_name, cell_range, custom_prompt, 
    model="gpt-3.5-turbo"  # Change this line
)
```

### Adjust Processing Speed
Modify the delay between API calls in the script:
```python
time.sleep(0.1)  # Change this value (in seconds)
```

### Custom System Prompt
Modify the system message in the script:
```python
{
    "role": "system",
    "content": "Your custom system prompt here"
}
```

## 🛠️ Troubleshooting

### Common Issues

**"Module not found" errors:**
```bash
pip install -r simple_requirements.txt
```

**"API key not found" errors:**
- Check that your `.env` file exists and contains the correct API key
- Make sure the API key is valid and has sufficient credits

**"File not found" errors:**
- Verify the Excel file path is correct
- Make sure the file exists and is not corrupted

**"Sheet not found" errors:**
- Check the sheet name spelling (case-sensitive)
- Use the exact sheet name from your Excel file

### Getting Help

1. **Check the logs:** Look for error messages in the terminal output
2. **Test with sample data:** Use `create_test_file.py` to generate test data
3. **Verify API key:** Test your API key on the OpenAI platform
4. **Check file permissions:** Ensure you can read the input file and write to the output directory

## 📈 Best Practices

1. **Start Small:** Test with a small range (e.g., A1:A5) before processing large datasets
2. **Use Specific Prompts:** Be clear and specific in your prompts for better results
3. **Monitor API Usage:** Keep track of your OpenAI API usage and costs
4. **Backup Data:** Always keep a backup of your original Excel files
5. **Rate Limiting:** The script includes built-in delays, but be mindful of API rate limits

## 🎉 Next Steps

Once you're comfortable with the basic usage:

1. **Explore Examples:** Run `python example_usage.py` for more examples
2. **Customize Prompts:** Experiment with different prompts for various use cases
3. **Batch Processing:** Process multiple files or ranges
4. **Integration:** Integrate the processor into your existing workflows

---

**Need more help?** Check the `README.md` file for detailed documentation or run the example scripts to see different use cases in action. 