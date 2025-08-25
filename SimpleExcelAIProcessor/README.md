# Simple Excel AI Processor

A clean and simple script that processes Excel cell ranges through the OpenAI API and outputs results to a new Excel file.

## Features

- Process any cell range in an Excel workbook
- Extract both cell values and formulas
- Send custom prompts to OpenAI API for each cell
- Output results to a new Excel file with organized columns
- Easy to use and share

## Setup

1. **Install Python dependencies:**
   ```bash
   pip install -r simple_requirements.txt
   ```

2. **Set up OpenAI API key:**
   - Get an API key from [OpenAI](https://platform.openai.com/api-keys)
   - Set it as an environment variable:
     ```bash
     export OPENAI_API_KEY="your-api-key-here"
     ```
   - Or on Windows:
     ```cmd
     set OPENAI_API_KEY=your-api-key-here
     ```

## Usage

1. **Run the script:**
   ```bash
   python simple_excel_ai_processor.py
   ```

2. **Follow the prompts:**
   - Enter the path to your Excel file
   - Choose the sheet name
   - Specify the cell range (e.g., `A1:B10`)
   - Enter your custom prompt

3. **Get results:**
   - The script will process each cell in the range
   - Results are saved to a new Excel file: `[original_filename]_AI_Results.xlsx`

## Output Format

The output Excel file contains these columns:
- **Sheet Name**: The sheet where the cell was located
- **Cell Reference**: The cell address (e.g., A1, B2)
- **Cell Value**: The actual value in the cell
- **Cell Formula**: The formula if the cell contains one
- **API Response**: The response from OpenAI API

## Example

**Input Excel file:**
- Sheet: "Data"
- Range: A1:A5
- Custom prompt: "Translate this text to Spanish"

**Output Excel file:**
| Sheet Name | Cell Reference | Cell Value | Cell Formula | API Response |
|------------|----------------|------------|--------------|--------------|
| Data       | A1            | Hello      |              | Hola         |
| Data       | A2            | World      |              | Mundo        |
| Data       | A3            | Goodbye    |              | Adiós        |

## Tips

- Use cell ranges like `A1:B10` for rectangular ranges
- Use single cells like `A1` for individual cells
- The script only processes non-empty cells
- Include a small delay between API calls to avoid rate limiting
- Results are automatically formatted with adjusted column widths

## Troubleshooting

- **File not found**: Make sure the Excel file path is correct
- **API errors**: Check your OpenAI API key and internet connection
- **Permission errors**: Ensure you have write permissions in the output directory

## Requirements

- Python 3.7+
- OpenAI API key
- Internet connection for API calls 