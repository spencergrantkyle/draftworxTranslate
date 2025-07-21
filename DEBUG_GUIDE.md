# Draftworx Translation Debug Guide

This guide explains how to use the debugging features added to the translation script for step-by-step testing and monitoring.

## Debug Features Overview

The translation script now includes comprehensive debugging capabilities that allow you to:

1. **Step through each cell processing** with detailed logging
2. **Monitor API calls and responses** in real-time
3. **Test individual translations** without processing the full dataset
4. **Interactive debugging** with custom input
5. **Detailed error reporting** with full stack traces
6. **Optimized throttling** for faster processing while respecting API limits
7. **Enhanced progress monitoring** with detailed statistics
8. **Resume functionality** to continue from backup files

## Performance Optimization

### Throttling Strategy

The script now uses optimized throttling for faster processing:

- **Batch processing**: Process 25 records before a longer pause (0.5 seconds)
- **Individual records**: Minimal pause (0.1 seconds) between records
- **Debug mode**: No rate limiting for faster testing
- **Configurable**: Adjust batch size and save intervals via command line

### Progress Monitoring

Enhanced progress tracking includes:

- **Real-time statistics**: Records processed, translation counts, processing rate
- **Time estimates**: Estimated time remaining based on current processing rate
- **Progress percentage**: Visual progress indicators
- **Automatic backups**: Timestamped backup files with detailed statistics

## Command Line Options

### Basic Usage

```bash
# Standard translation
python translate.py

# Debug mode
python translate.py --debug

# Interactive testing
python debug_test.py
```

### Advanced Options

```bash
# Configure batch size and save interval
python translate.py --batch-size 50 --save-interval 100

# Resume from backup file
python translate.py --resume-from "Backup_OutputResults/backup_100_20241201_143022.csv"

# Custom input/output files
python translate.py --input-file "my_data.csv" --output-file "my_translated_data.csv"

# Combine options
python translate.py --debug --batch-size 30 --save-interval 75 --resume-from "backup.csv"
```

### Command Line Arguments

| Argument | Short | Description | Default |
|----------|-------|-------------|---------|
| `--debug` | `-d` | Enable debug mode | False |
| `--batch-size` | `-b` | Records before rate limiting pause | 25 |
| `--save-interval` | `-s` | Records before saving progress | 50 |
| `--resume-from` | `-r` | Path to backup file to resume from | None |
| `--input-file` | `-i` | Input CSV file path | `SheetFlatFiles/directors.csv` |
| `--output-file` | `-o` | Output CSV file path | `SheetFlatFiles/directors_inafrikaans.csv` |

## Progress Monitoring

### Real-time Statistics

During processing, you'll see detailed progress information:

```
Processing record 45/200 (22.5%): Directors' Report...
Progress saved to: Backup_OutputResults/backup_50_20241201_143022.csv
Records processed: 50/200 (25.0%)
Translated values: 45
Translated formulas: 42
Elapsed time: 67.34 seconds
Processing rate: 0.74 records/second
Estimated time remaining: 202.5 seconds (3.4 minutes)
```

### Backup Files

Backup files are automatically created with:

- **Timestamped names**: `backup_50_20241201_143022.csv`
- **Progress indicators**: Number in filename shows records processed
- **Final backups**: `final_backup_200_20241201_150045.csv` for completed runs
- **Detailed statistics**: Each save includes processing rate and time estimates

## Resume Functionality

### Listing Backup Files

Use the backup lister to see available backup files:

```bash
python list_backups.py
```

Example output:
```
================================================================================
AVAILABLE BACKUP FILES
================================================================================
File                                              Records   Values    Formulas  Type      
--------------------------------------------------------------------------------
backup_50_20241201_143022.csv                    200       45        42        PROGRESS  
backup_100_20241201_144515.csv                   200       89        87        PROGRESS  
final_backup_200_20241201_150045.csv             200       200       198       FINAL     
--------------------------------------------------------------------------------

SUMMARY:
Total backup files: 3
Most recent backup: final_backup_200_20241201_150045.csv
  Modified: 2024-12-01 15:00:45
  Progress: 200/200 values (100.0%)

To resume from the most recent backup, run:
python translate.py --resume-from "Backup_OutputResults/final_backup_200_20241201_150045.csv"
```

### Resuming from Backup

```bash
# Resume from specific backup file
python translate.py --resume-from "Backup_OutputResults/backup_50_20241201_143022.csv"

# Resume with custom parameters
python translate.py --resume-from "backup.csv" --batch-size 30 --save-interval 60
```

### Backup File Details

View detailed information about a specific backup:

```bash
python list_backups.py "Backup_OutputResults/backup_50_20241201_143022.csv"
```

## Debug Modes

### 1. Full Dataset Debug Mode

Run the main translation script with debug mode enabled:

```bash
# Enable debug mode with command line flag
python translate.py --debug

# Or use the short form
python translate.py -d
```

**What this does:**
- Processes the full dataset step-by-step
- Shows detailed information for each record
- Prompts you to continue after each cell processing
- Displays API call context and responses
- Skips rate limiting for faster testing

**Example output:**
```
DEBUG MODE ENABLED - Step-by-step processing with user interaction
You will be prompted to continue after each cell processing

================================================================================
DEBUG: Processing Record 1
================================================================================
Row index: 0
English value: 'Directors' Report'
English formula: '=A1'
Press Enter to continue with translation...

Calling translate_text_to_afrikaans...
================================================================================
DEBUG: translate_text_to_afrikaans
================================================================================
Input English text: 'Directors' Report'
Using model: gpt-4o
Using prompt ID: pmpt_687bf16ca65c8194a1dc502981595803065506b4fb34a24c
Making API call...
API Response received:
Raw response: <Response object>
Output text: 'Direkteursverslag'
================================================================================
Translation result stored: 'Direkteursverslag'
```

### 2. Interactive Debug Tool

Use the interactive debug script for custom testing:

```bash
python debug_test.py
```

**What this provides:**
- Menu-driven interface for testing
- Custom input for text translation
- Custom input for formula generation
- View named ranges documentation
- Complete workflow testing

## Debug Output Details

### Translation Debug Output

When `translate_text_to_afrikaans()` is called in debug mode, you'll see:

```
================================================================================
DEBUG: translate_text_to_afrikaans
================================================================================
Input English text: 'Directors' Report'
Using model: gpt-4o
Using prompt ID: pmpt_687bf16ca65c8194a1dc502981595803065506b4fb34a24c
Making API call...
API Response received:
Raw response: <Response object>
Output text: 'Direkteursverslag'
================================================================================
```

### Formula Generation Debug Output

When `generate_afrikaans_formula()` is called in debug mode, you'll see:

```
================================================================================
DEBUG: generate_afrikaans_formula
================================================================================
Input English value: 'Directors' Report'
Input Afrikaans value: 'Direkteursverslag'
Input English formula: '=A1'
Using model: gpt-4o
Using prompt ID: pmpt_687bf4be40f88195ad8b29331fb5004701f521265648f64a
Formatted input text:
----------------------------------------
Original English Value: "Directors' Report"
Translated Afrikaans Value: "Direkteursverslag"
Original English Formula: =A1
Named Ranges Reference: [documentation content...]
----------------------------------------
Making API call...
API Response received:
Raw response: <Response object>
Output formula: '=A1'
Final formula with apostrophe: ''=A1'
================================================================================
```

## Interactive Debug Tool Options

When running `python debug_test.py`, you'll see these options:

1. **Test text translation** - Test only the text translation function
2. **Test formula generation** - Test only the formula generation function
3. **Test both (text + formula)** - Test the complete workflow
4. **View named ranges documentation** - Check if named ranges are loaded
5. **Quit** - Exit the debug tool

## Error Handling in Debug Mode

When errors occur in debug mode, you'll get detailed information:

```
DEBUG: Error in translate_text_to_afrikaans: API rate limit exceeded
Full error details: RateLimitError: Rate limit exceeded
Press Enter to continue to next record...
```

## Performance Tips

### Optimizing Processing Speed

1. **Adjust batch size**: Larger batch sizes (50-100) for faster processing
2. **Increase save interval**: Save less frequently (100-200) to reduce I/O overhead
3. **Monitor API limits**: Watch for rate limit errors and adjust accordingly

### Example Fast Processing

```bash
# Fast processing configuration
python translate.py --batch-size 100 --save-interval 200

# Balanced configuration (recommended)
python translate.py --batch-size 50 --save-interval 100

# Conservative configuration (for unstable connections)
python translate.py --batch-size 25 --save-interval 50
```

## Troubleshooting

### Common Issues

1. **API Key Not Found**
   ```
   Configuration error: OPENAI_API_KEY not found in .env file or environment variables
   ```
   - Ensure your `.env` file contains `OPENAI_API_KEY=your-key-here`

2. **Prompt Primitive Not Found**
   ```
   Error: Prompt primitive not found
   ```
   - Verify the prompt IDs in `secrets.md` are correct
   - Check that the prompt primitives exist in your OpenAI dashboard

3. **Named Ranges Documentation Missing**
   ```
   Knowledge/DraftworxNamedRanges.md not found. Named ranges context will not be available.
   ```
   - This is a warning, not an error
   - Formula generation will still work but without named ranges context

4. **Backup Directory Not Found**
   ```
   Backup directory 'Backup_OutputResults' not found.
   ```
   - The script will automatically create the directory when needed

### Debug Mode Best Practices

1. **Use for Development Only** - Debug mode is for testing, not production
2. **Monitor API Costs** - Debug mode can make many API calls quickly
3. **Check Logs** - Review `translation.log` for detailed error information
4. **Test Incrementally** - Start with single tests before running full dataset
5. **Use Resume Feature** - Resume from backups if processing is interrupted

## File Structure

```
draftworx_translate/
├── translate.py          # Main translation script with debug mode
├── debug_test.py         # Interactive debug tool
├── list_backups.py       # Backup file lister utility
├── DEBUG_GUIDE.md        # This guide
├── secrets.md            # Prompt primitive IDs
├── Knowledge/
│   └── DraftworxNamedRanges.md  # Named ranges documentation
├── Backup_OutputResults/ # Backup files directory
│   ├── backup_50_*.csv   # Progress backup files
│   └── final_backup_*.csv # Final backup files
└── translation.log       # Detailed logging output
```

## Next Steps

1. **Test API Connectivity**: Run `python debug_test.py` to verify basic functionality
2. **Test Full Workflow**: Run `python translate.py --debug` for step-by-step processing
3. **Optimize Performance**: Adjust batch size and save interval for your needs
4. **Monitor Progress**: Use `python list_backups.py` to track progress
5. **Resume if Needed**: Use resume functionality if processing is interrupted 