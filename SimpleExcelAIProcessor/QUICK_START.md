# Quick Start Guide

Get up and running in 3 minutes!

## 🚀 Step 1: Setup (1 minute)

**Windows:**
```cmd
run_processor.bat
```

**Mac/Linux:**
```bash
./run_processor.sh
```

**Manual Setup:**
```bash
python setup.py
```

## 🔑 Step 2: Add API Key (30 seconds)

1. Get your API key from [OpenAI](https://platform.openai.com/api-keys)
2. Edit the `.env` file and replace `your-api-key-here` with your actual key

## 📊 Step 3: Create Test Data (30 seconds)

```bash
python create_test_file.py
```

This creates `test_data.xlsx` with sample data.

## 🎯 Step 4: Run the Processor (1 minute)

```bash
python simple_excel_ai_processor.py
```

**Follow the prompts:**
- File: `test_data.xlsx`
- Sheet: `TestData`
- Range: `A1:A10`
- Prompt: `"Translate this text to Spanish"`

## ✅ Done!

Check your results in `test_data_AI_Results.xlsx`

---

## 🎯 Common Use Cases

**Translation:**
- Range: `A1:A20`
- Prompt: `"Translate to French"`

**Analysis:**
- Range: `B1:B50`
- Prompt: `"Analyze this financial data and provide insights"`

**Summarization:**
- Range: `C1:C10`
- Prompt: `"Summarize this text in 2 sentences"`

## 🆘 Need Help?

- See `README.md` for detailed documentation
- Run `python example_usage.py` for code examples
- Check the output Excel file for any error messages 