# Draftworx Translation Script

This script translates English financial statement formulas and values to multiple languages (primarily Afrikaans and Spanish) using OpenAI's GPT-4 API. It processes CSV files containing financial statement data and generates translations while preserving Excel named ranges and formula logic.

## Features

- **Multi-language Support**: Translate to Afrikaans, Spanish, and other languages
- **Intelligent Formula Translation**: Preserves Excel named ranges and functions while translating text content
- **Professional Financial Terminology**: Maintains IFRS-compliant financial disclosure standards
- **Progress Tracking & Backup**: Automatic backup every 5 records with detailed progress logging
- **Resume Capability**: Can resume from backup files if processing is interrupted
- **Debug Mode**: Step-by-step processing with user interaction for troubleshooting
- **Comprehensive Logging**: Detailed logs for debugging and monitoring
- **UTF-8 BOM Support**: Excel-compatible output encoding

## Prerequisites

- Python 3.7 or higher
- OpenAI API key
- CSV files in the `SheetFlatFiles/` directory
- Optional: `Knowledge/DraftworxNamedRanges.md` for named ranges context

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

## Project Structure

```
draftworx_translate/
├── translate.py              # Main translation script
├── csv_reader.py            # CSV file handling utilities
├── test_prompts.py          # OpenAI API prompt functions
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── .env                    # Environment variables (create this)
├── SheetFlatFiles/         # Input CSV files
│   ├── directors.csv
│   ├── accountingpolicies.csv
│   └── [other CSV files]
├── Knowledge/              # Reference materials
│   ├── DraftworxNamedRanges.md
│   ├── Example_EnglishAfrikaans.md
│   └── IFRS+ Financials.xlsx
└── Backup_OutputResults/   # Automatic backup files
```

## Usage

### Basic Usage

Run the script with default settings (translates directors.csv to Afrikaans):
```bash
python translate.py
```

### Command Line Options

```bash
python translate.py [OPTIONS]

Options:
  --debug, -d              Enable debug mode with step-by-step processing
  --save-interval, -s      Number of records before saving progress (default: 5)
  --resume-from, -r        Path to backup file to resume from
  --input-file, -i         Input CSV file path (default: SheetFlatFiles/directors.csv)
  --output-file, -o        Output CSV file path (auto-generated if not specified)
  --language, -l           Target language (default: Afrikaans)
```

### Examples

**Translate directors.csv to Afrikaans:**
```bash
python translate.py
```

**Translate accounting policies to Spanish with debug mode:**
```bash
python translate.py --input-file SheetFlatFiles/accountingpolicies.csv --language Spanish --debug
```

**Resume from a backup file:**
```bash
python translate.py --resume-from Backup_OutputResults/backup_afrikaans_50_20250721_100022.csv
```

**Custom save interval and output file:**
```bash
python translate.py --save-interval 10 --output-file my_translated_file.csv
```

### Programmatic Usage

```python
from translate import DraftworxTranslator

# Initialize translator
translator = DraftworxTranslator(debug_mode=False, target_language="Spanish")

# Run translation
translator.run_translation(
    input_file="SheetFlatFiles/accountingpolicies.csv",
    output_file="accountingpolicies_inspanish.csv",
    save_interval=5
)
```

## Input File Format

The script expects CSV files with the following columns:
- `CellValue_English`: The English text to translate
- `CellFormula_English`: The English Excel formula to convert
- `CellValue_[Language]`: (Optional) Will be populated with translations
- `CellFormula_[Language]`: (Optional) Will be populated with translated formulas

## Output

The script generates:
- `[filename]_in[language].csv`: Final output with translations
- `translation.log`: Detailed log file with translation progress
- Backup files: `Backup_OutputResults/backup_[language]_[count]_[timestamp].csv`

## Named Ranges Support

The script automatically loads `Knowledge/DraftworxNamedRanges.md` to understand Excel named ranges used in formulas. This ensures accurate formula generation by preserving:
- Named ranges (e.g., `CompanyName`, `Director_is_are`, `AFS_Name`)
- Excel functions (e.g., `IF`, `UPPER`, `LEN`, `OR`, `AND`)
- Cell references and operators
- Only translates hardcoded text in quotation marks

## Rate Limiting & Performance

- Built-in 0.5-second delay between API calls to respect OpenAI rate limits
- Progress saved every 5 records by default (configurable)
- Processing rate: ~2 records/second (varies with API response time)
- For large datasets, consider:
  - Using a higher-tier OpenAI plan
  - Processing during off-peak hours
  - Using debug mode for small batches

## Error Handling

- Failed translations retain original English text
- Failed formula generations retain original formula with apostrophe prefix
- All errors logged to `translation.log`
- Automatic backup prevents data loss
- Resume capability from any backup file

## Example Output

**Input:**
```
CellValue_English: "The director is required by the Companies Act of South Africa to maintain adequate accounting records"
CellFormula_English: "=""The "&Director_board&" is required by the "&ApplicableAct&" to maintain adequate accounting records"""
```

**Output:**
```
CellValue_Afrikaans: "Die direkteur word ingevolge die Maatskappyewet van Suid-Afrika vereis om toepaslike rekeningkundige rekords te onderhou"
CellFormula_Afrikaans: "'=""Die "&Director_board&" word ingevolge die "&ApplicableAct&" vereis om toepaslike rekeningkundige rekords te onderhou"""
```

## Debug Mode

Enable debug mode for step-by-step processing:
```bash
python translate.py --debug
```

Debug mode features:
- User interaction after each API call
- Detailed logging of input/output
- Ability to inspect translations before proceeding
- Useful for troubleshooting and small batches

## Troubleshooting

1. **API Key Issues**: Ensure your `.env` file contains the correct OpenAI API key
2. **File Not Found**: Check that input CSV files exist in the `SheetFlatFiles/` directory
3. **Rate Limits**: Script automatically handles rate limiting with delays
4. **Memory Issues**: For very large files, consider processing in smaller chunks
5. **Encoding Issues**: All files use UTF-8 encoding for compatibility

## Logging

The script creates detailed logs in `translation.log` including:
- Translation progress and statistics
- API responses and errors
- Processing rates and time estimates
- Backup file locations
- Debug information (when enabled)

## Dependencies

- `pandas>=1.5.0`: Data manipulation
- `openai>=0.28.0`: OpenAI API client
- `python-dotenv>=0.19.0`: Environment variable management
- `openpyxl>=3.0.0`: Excel file support
- `streamlit>=1.28.0`: Web interface (if needed)
- `plotly>=5.15.0`: Data visualization (if needed)

## License

This script is provided as-is for use with Draftworx financial statement translation. 