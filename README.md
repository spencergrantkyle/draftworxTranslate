# Draftworx Translation Script

This script translates English financial statement formulas and values to Afrikaans using OpenAI's GPT-4 API. It processes the `IFRSEnglishFormulasValues.csv` file and generates Afrikaans translations while preserving Excel named ranges.

## Features

- Translates English text values to Afrikaans using OpenAI API
- Generates Afrikaans Excel formulas that maintain named ranges
- Preserves professional financial statement terminology
- Includes progress tracking and backup functionality
- Comprehensive logging for debugging

## Prerequisites

- Python 3.7 or higher
- OpenAI API key
- `IFRSEnglishFormulasValues.csv` file in the project directory
- Optional: `DraftworxNamedRanges.md` file for named ranges context

## Installation

1. Clone or download this repository
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project directory with your OpenAI API key:
   ```
   OPENAI_API_KEY=your-api-key-here
   ```

## Usage

### Basic Usage

Run the script with default settings:
```bash
python translate
```

### Custom Input/Output Files

You can specify custom input and output files by modifying the script or calling the methods directly:

```python
from translate import DraftworxTranslator

translator = DraftworxTranslator()  # Will automatically load API key from .env
translator.run_translation(
    input_file="your_input.csv",
    output_file="your_output.csv"
)
```

## Input File Format

The script expects a CSV file with the following columns:
- `CellValue_English`: The English text to translate
- `CellFormula_English`: The English Excel formula to convert
- `CellValue_Afrikaans`: (Optional) Will be populated with Afrikaans translations
- `CellFormula_Afrikaans`: (Optional) Will be populated with Afrikaans formulas

## Output

The script generates:
- `IFRSEnglishFormulasValues_translated.csv`: Final output with Afrikaans translations
- `translation.log`: Detailed log file with translation progress
- Backup files: `IFRSEnglishFormulasValues_backup_X.csv` (every 10 records)

## Named Ranges

If you have a `DraftworxNamedRanges.md` file, the script will use it as context to understand the named ranges used in your Excel formulas. This helps ensure accurate formula generation.

## Rate Limiting

The script includes a 1-second delay between API calls to respect OpenAI's rate limits. For large datasets, consider:
- Using a higher-tier OpenAI plan
- Processing in smaller batches
- Running during off-peak hours

## Error Handling

- Failed translations will retain the original English text
- Failed formula generations will retain the original formula with an apostrophe prefix
- All errors are logged to `translation.log`
- Progress is saved every 10 records to prevent data loss

## Example Output

**Input:**
```
CellValue_English: "Registration Number"
CellFormula_English: "=""(""&IF(EntityType=""Sole Proprietor"",""Identification"",""Registration"")&"" Number ""&RegistrationNumber&"")"""
```

**Output:**
```
CellValue_Afrikaans: "Registrasienommer"
CellFormula_Afrikaans: "'=""(""&IF(EntityType=""Sole Proprietor"",""Identifikasie"",""Registrasie"")&"" Nommer ""&RegistrationNumber&"")"""
```

## Troubleshooting

1. **API Key Issues**: Ensure your `.env` file contains the correct OpenAI API key
2. **File Not Found**: Check that `IFRSEnglishFormulasValues.csv` exists in the project directory
3. **Rate Limits**: If you hit rate limits, the script will pause and retry
4. **Memory Issues**: For very large files, consider processing in smaller chunks

## Logging

The script creates detailed logs in `translation.log` including:
- Translation progress
- API responses
- Errors and warnings
- Processing statistics

## License

This script is provided as-is for use with Draftworx financial statement translation. 