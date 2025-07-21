#!/usr/bin/env python3
"""
Translation Script for Draftworx Financial Statements
Translates English formulas and values to Afrikaans using OpenAI API
"""

import os
import pandas as pd
import time
import logging
from typing import Optional, Dict, Any
from csv_reader import CSVReader
from dotenv import load_dotenv
from test_prompts import translate_english_value, translate_formula

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('translation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DraftworxTranslator:
    """
    Handles translation of Draftworx financial statement formulas from English to a target language
    """
    
    def __init__(self, debug_mode: bool = False, target_language: str = "Afrikaans"):
        """
        Initialize the translator
        
        Args:
            debug_mode (bool): Enable step-by-step debugging mode
            target_language (str): The language to translate to
        """
        self.debug_mode = debug_mode
        self.target_language = target_language.capitalize()
        
        # Load the CSV reader
        self.csv_reader = CSVReader()
        
        # Load named ranges documentation DraftworxNamedRanges.md
        self.named_ranges_doc = self._load_named_ranges_doc()
        
        logger.info("DraftworxTranslator initialized successfully")
        if debug_mode:
            logger.info("DEBUG MODE ENABLED - Step-by-step processing with user interaction")
        logger.info(f"Target language: {self.target_language}")
        
    def _load_named_ranges_doc(self) -> str:
        """
        Load the DraftworxNamedRanges.md file if it exists
        
        Returns:
            str: Content of the named ranges documentation or empty string
        """
        try:
            if os.path.exists("Knowledge/DraftworxNamedRanges.md"):
                with open("Knowledge/DraftworxNamedRanges.md", "r", encoding="utf-8") as f:
                    content = f.read()
                    logger.info("Named ranges documentation loaded successfully")
                    return content
            else:
                logger.warning("Knowledge/DraftworxNamedRanges.md not found. Named ranges context will not be available.")
                return ""
        except Exception as e:
            logger.error(f"Error loading named ranges documentation: {e}")
            return ""
    
    def translate_text(self, english_text: str) -> str:
        """
        Translate English text to the target language using the function from test_prompts.py
        
        Args:
            english_text (str): English text to translate
            
        Returns:
            str: Translated text in the target language
        """
        if not english_text or english_text.strip() == "":
            return ""
            
        try:
            if self.debug_mode:
                logger.info("=" * 80)
                logger.info(f"DEBUG: translate_text_to_{self.target_language.lower()}")
                logger.info("=" * 80)
                logger.info(f"Input English text: '{english_text}'")
                logger.info("Making API call to translate_english_value...")
            
            # Use the function from test_prompts.py
            translation = translate_english_value(english_text, self.target_language)
            
            if self.debug_mode:
                logger.info("API Response received:")
                logger.info(f"Translation result: '{translation}'")
                logger.info("=" * 80)
            
            logger.info(f"Translated: '{english_text}' -> '{translation}' [{self.target_language}]")
            return translation.strip()
            
        except Exception as e:
            if self.debug_mode:
                logger.error(f"DEBUG: Error in translate_text_to_{self.target_language.lower()}: {e}")
                logger.error(f"Full error details: {type(e).__name__}: {str(e)}")
            logger.error(f"Error translating text '{english_text}': {e}")
            return english_text  # Return original if translation fails
    
    def generate_formula(self, english_value: str, translated_value: str, english_formula: str) -> str:
        """
        Generate formula in the target language using the function from test_prompts.py
        
        Args:
            english_value (str): Original English value
            translated_value (str): Translated value in the target language
            english_formula (str): Original English Excel formula
            
        Returns:
            str: Target language Excel formula with apostrophe prefix
        """
        if not english_formula or english_formula.strip() == "":
            return ""
            
        try:
            if self.debug_mode:
                logger.info("=" * 80)
                logger.info(f"DEBUG: generate_{self.target_language.lower()}_formula")
                logger.info("=" * 80)
                logger.info(f"Input English value: '{english_value}'")
                logger.info(f"Input {self.target_language} value: '{translated_value}'")
                logger.info(f"Input English formula: '{english_formula}'")
                logger.info("Making API call to translate_formula...")
            
            # Use the function from test_prompts.py
            formula = translate_formula(english_value, translated_value, english_formula, self.target_language)
            
            if self.debug_mode:
                logger.info("API Response received:")
                logger.info(f"Output formula: '{formula}'")
            
            # Ensure formula starts with apostrophe
            if not formula.startswith("'"):
                formula = "'" + formula
                
            if self.debug_mode:
                logger.info(f"Final formula with apostrophe: '{formula}'")
                logger.info("=" * 80)
                
            logger.info(f"Generated {self.target_language} formula: {formula}")
            return formula.strip()
            
        except Exception as e:
            if self.debug_mode:
                logger.error(f"DEBUG: Error in generate_{self.target_language.lower()}_formula: {e}")
                logger.error(f"Full error details: {type(e).__name__}: {str(e)}")
            logger.error(f"Error generating {self.target_language} formula for '{english_formula}': {e}")
            return f"'{english_formula}"  # Return original with apostrophe if generation fails
    
    def process_single_record(self, df: pd.DataFrame, index: int) -> bool:
        """
        Process a single record with proper API call sequencing
        
        Args:
            df (pd.DataFrame): The dataframe to update
            index (int): Index of the record to process
            
        Returns:
            bool: True if processing was successful, False otherwise
        """
        try:
            english_value = str(df.at[index, 'CellValue_English']).strip()
            english_formula = str(df.at[index, 'CellFormula_English']).strip()
            value_col = f'CellValue_{self.target_language}'
            formula_col = f'CellFormula_{self.target_language}'
            
            # Skip if already processed or empty
            if (df.at[index, value_col] and df.at[index, formula_col]) or \
               (not english_value and not english_formula):
                if self.debug_mode:
                    logger.info(f"Skipping record {index + 1}: Already processed or empty")
                return True
            
            logger.info(f"Processing record {index + 1}: {english_value[:50]}...")
            
            if self.debug_mode:
                logger.info("=" * 80)
                logger.info(f"DEBUG: Processing Record {index + 1}")
                logger.info("=" * 80)
                logger.info(f"Row index: {index}")
                logger.info(f"English value: '{english_value}'")
                logger.info(f"English formula: '{english_formula}'")
                logger.info("Press Enter to continue with translation...")
                input()
            
            # Step 1: Translate the English value to target language
            translated_value = ""
            if english_value:
                if self.debug_mode:
                    logger.info(f"Step 1: Calling translate_text_to_{self.target_language.lower()}...")
                    logger.info("Press Enter to make API call...")
                    input()
                
                translated_value = self.translate_text(english_value)
                df.at[index, value_col] = translated_value
                
                if self.debug_mode:
                    logger.info(f"Translation completed and saved: '{translated_value}'")
                    logger.info("Press Enter to continue to formula generation...")
                    input()
            else:
                if self.debug_mode:
                    logger.info("No English value to translate")
            
            # Step 2: Generate formula
            if english_formula:
                if self.debug_mode:
                    logger.info(f"Step 2: Calling generate_{self.target_language.lower()}_formula...")
                    logger.info("Press Enter to make API call...")
                    input()
                
                formula = self.generate_formula(
                    english_value, translated_value, english_formula
                )
                df.at[index, formula_col] = formula
                
                if self.debug_mode:
                    logger.info(f"Formula generation completed and saved: '{formula}'")
                    logger.info("Press Enter to continue to next record...")
                    input()
            else:
                if self.debug_mode:
                    logger.info("No English formula to generate")
            
            if self.debug_mode:
                logger.info(f"Record {index + 1} processing completed.")
                logger.info("Current results:")
                logger.info(f"  {value_col}: '{df.at[index, value_col]}'")
                logger.info(f"  {formula_col}: '{df.at[index, formula_col]}'")
                logger.info("Press Enter to continue to next record...")
                input()
            
            return True
            
        except Exception as e:
            logger.error(f"Error processing record {index}: {e}")
            if self.debug_mode:
                logger.error(f"DEBUG: Full error details: {type(e).__name__}: {str(e)}")
                logger.info("Press Enter to continue to next record...")
                input()
            return False
    
    def process_dataframe(self, df: pd.DataFrame, save_interval: int = 5) -> pd.DataFrame:
        """
        Process the dataframe to translate values and generate formulas
        
        Args:
            df (pd.DataFrame): Input dataframe with English values and formulas
            save_interval (int): Number of records to process before saving progress
            
        Returns:
            pd.DataFrame: Updated dataframe with target language translations
        """
        logger.info(f"Starting translation process for {len(df)} records")
        logger.info(f"Save interval: {save_interval}")
        
        if self.debug_mode:
            logger.info("DEBUG MODE ENABLED - Step-by-step processing with user interaction")
            logger.info("You will be prompted to continue after each API call")
        
        value_col = f'CellValue_{self.target_language}'
        formula_col = f'CellFormula_{self.target_language}'
        if value_col not in df.columns:
            df[value_col] = ''
        if formula_col not in df.columns:
            df[formula_col] = ''
        
        processed_count = 0
        successful_count = 0
        start_time = time.time()
        last_save_time = start_time
        
        for index in range(len(df)):
            try:
                # Calculate progress percentage
                progress_pct = ((index + 1) / len(df)) * 100
                elapsed_time = time.time() - start_time
                
                logger.info(f"Processing record {index + 1}/{len(df)} ({progress_pct:.1f}%)")
                
                # Process single record with proper sequencing
                success = self.process_single_record(df, index)
                
                if success:
                    successful_count += 1
                
                processed_count += 1
                
                # Save progress based on interval
                if processed_count % save_interval == 0:
                    self.save_progress(df, processed_count, successful_count, elapsed_time)
                    last_save_time = time.time()
                
                # Rate limiting - be respectful to the API
                if not self.debug_mode:
                    # Small pause between records to be respectful
                    time.sleep(0.5)
                
            except KeyboardInterrupt:
                logger.info("Translation interrupted by user")
                self.save_progress(df, processed_count, successful_count, time.time() - start_time, is_final=True)
                break
            except Exception as e:
                logger.error(f"Unexpected error processing record {index}: {e}")
                if self.debug_mode:
                    logger.info("Press Enter to continue to next record...")
                    input()
                continue
        
        # Final save
        if processed_count > 0:
            final_elapsed = time.time() - start_time
            self.save_progress(df, processed_count, successful_count, final_elapsed, is_final=True)
        
        logger.info(f"Translation process completed. {successful_count}/{processed_count} records processed successfully in {time.time() - start_time:.2f} seconds.")
        return df
    
    def save_progress(self, df: pd.DataFrame, processed_count: int, successful_count: int, elapsed_time: float, is_final: bool = False):
        """
        Save the current progress to a backup file with enhanced tracking
        
        Args:
            df (pd.DataFrame): Current dataframe
            processed_count (int): Number of records processed
            successful_count (int): Number of records processed successfully
            elapsed_time (float): Total elapsed time in seconds
            is_final (bool): True if this is the final save, False otherwise
        """
        try:
            # Ensure backup directory exists
            backup_dir = "Backup_OutputResults"
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
                logger.info(f"Created backup directory: {backup_dir}")
            
            # Create timestamp for unique filenames
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            lang_suffix = self.target_language.lower()
            
            if is_final:
                backup_filename = f"{backup_dir}/final_backup_{lang_suffix}_{successful_count}_{timestamp}.csv"
                logger.info("=" * 60)
                logger.info("FINAL PROGRESS SAVE")
                logger.info("=" * 60)
            else:
                backup_filename = f"{backup_dir}/backup_{lang_suffix}_{successful_count}_{timestamp}.csv"
                logger.info("-" * 40)
                logger.info("PROGRESS SAVE")
                logger.info("-" * 40)
            
            # Save the dataframe with UTF-8 BOM for Excel compatibility
            df.to_csv(backup_filename, index=False, encoding='utf-8-sig')
            
            # Calculate statistics
            total_records = len(df)
            value_col = f'CellValue_{self.target_language}'
            formula_col = f'CellFormula_{self.target_language}'
            translated_values = df[value_col].notna().sum()
            translated_formulas = df[formula_col].notna().sum()
            
            # Calculate processing rate
            if elapsed_time > 0:
                records_per_second = successful_count / elapsed_time
                estimated_remaining = (total_records - processed_count) / records_per_second if records_per_second > 0 else 0
            else:
                records_per_second = 0
                estimated_remaining = 0
            
            # Log progress statistics
            logger.info(f"Progress saved to: {backup_filename}")
            logger.info(f"Records processed: {processed_count}/{total_records} ({processed_count/total_records*100:.1f}%)")
            logger.info(f"Successful translations: {successful_count}")
            logger.info(f"Translated values: {translated_values}")
            logger.info(f"Translated formulas: {translated_formulas}")
            logger.info(f"Elapsed time: {elapsed_time:.2f} seconds")
            logger.info(f"Processing rate: {records_per_second:.2f} records/second")
            
            if not is_final and estimated_remaining > 0:
                logger.info(f"Estimated time remaining: {estimated_remaining:.1f} seconds ({estimated_remaining/60:.1f} minutes)")
            
            if is_final:
                logger.info("=" * 60)
            else:
                logger.info("-" * 40)
                
        except Exception as e:
            logger.error(f"Error saving progress: {e}")
            logger.error(f"Full error details: {type(e).__name__}: {str(e)}")
    
    def resume_from_backup(self, backup_file: str) -> pd.DataFrame:
        """
        Resume processing from a backup file
        
        Args:
            backup_file (str): Path to the backup file to resume from
            
        Returns:
            pd.DataFrame: Loaded dataframe with existing progress
        """
        try:
            logger.info(f"Resuming from backup file: {backup_file}")
            
            if not os.path.exists(backup_file):
                raise FileNotFoundError(f"Backup file not found: {backup_file}")
            
            # Load the backup dataframe
            df = pd.read_csv(backup_file, encoding='utf-8')
            
            value_col = f'CellValue_{self.target_language}'
            formula_col = f'CellFormula_{self.target_language}'
            existing_values = df[value_col].notna().sum() if value_col in df.columns else 0
            existing_formulas = df[formula_col].notna().sum() if formula_col in df.columns else 0
            
            logger.info(f"Loaded backup with {len(df)} records")
            logger.info(f"Existing translations: {existing_values} values, {existing_formulas} formulas")
            
            return df
            
        except Exception as e:
            logger.error(f"Error resuming from backup: {e}")
            raise
    
    def run_translation(self, input_file: str = "SheetFlatFiles/directors.csv", 
                       output_file: str = None,
                       save_interval: int = 5,
                       resume_from: str = None):
        """
        Main method to run the translation process
        
        Args:
            input_file (str): Input CSV file path
            output_file (str): Output CSV file path (if None, auto-generate based on language)
            save_interval (int): Number of records to process before saving progress
            resume_from (str): Path to backup file to resume from (optional)
        """
        try:
            if resume_from:
                logger.info(f"Resuming translation from backup: {resume_from}")
                df = self.resume_from_backup(resume_from)
            else:
                logger.info(f"Loading data from {input_file}")
                # Load the CSV file
                df = self.csv_reader.read_csv(input_file)
                logger.info(f"Loaded {len(df)} records from {input_file}")
            
            # Process the dataframe with configurable parameters
            df_translated = self.process_dataframe(df, save_interval=save_interval)
            
            # Save the final result with UTF-8 BOM for Excel compatibility
            value_col = f'CellValue_{self.target_language}'
            formula_col = f'CellFormula_{self.target_language}'
            if not output_file:
                base, ext = os.path.splitext(input_file)
                output_file = f"{base}_in{self.target_language.lower()}{ext}"
            logger.info(f"Saving translated data to {output_file}")
            df_translated.to_csv(output_file, index=False, encoding='utf-8-sig')
            
            # Print summary
            translated_values = df_translated[value_col].notna().sum()
            translated_formulas = df_translated[formula_col].notna().sum()
            
            logger.info(f"Translation Summary:")
            logger.info(f"  Total records: {len(df_translated)}")
            logger.info(f"  Translated values: {translated_values}")
            logger.info(f"  Translated formulas: {translated_formulas}")
            logger.info(f"  Output saved to: {output_file}")
            
        except Exception as e:
            logger.error(f"Error in translation process: {e}")
            raise


def main():
    """Main function to run the translation script"""
    
    try:
        import sys
        import argparse
        
        # Set up command line argument parsing
        parser = argparse.ArgumentParser(description='Draftworx Translation Script')
        parser.add_argument('--debug', '-d', action='store_true', 
                          help='Enable debug mode with step-by-step processing')
        parser.add_argument('--save-interval', '-s', type=int, default=5,
                          help='Number of records to process before saving progress (default: 5)')
        parser.add_argument('--resume-from', '-r', type=str,
                          help='Path to backup file to resume from')
        parser.add_argument('--input-file', '-i', type=str, default="SheetFlatFiles/directors.csv",
                          help='Input CSV file path (default: SheetFlatFiles/directors.csv)')
        parser.add_argument('--output-file', '-o', type=str, default=None,
                          help='Output CSV file path (default: auto-generated based on language)')
        parser.add_argument('--language', '-l', type=str, default="Afrikaans",
                          help='Target language for translation (default: Afrikaans)')
        
        args = parser.parse_args()
        
        # Check for debug mode
        debug_mode = args.debug
        target_language = args.language.capitalize()
        
        if debug_mode:
            logger.info("DEBUG MODE ENABLED")
            logger.info("This will run step-by-step with detailed logging and user interaction")
            logger.info("Use Ctrl+C to exit at any time")
        
        # Log configuration
        logger.info("Translation Configuration:")
        logger.info(f"  Debug mode: {debug_mode}")
        logger.info(f"  Save interval: {args.save_interval}")
        logger.info(f"  Input file: {args.input_file}")
        logger.info(f"  Output file: {args.output_file}")
        logger.info(f"  Target language: {target_language}")
        if args.resume_from:
            logger.info(f"  Resume from: {args.resume_from}")
        
        # Initialize translator
        translator = DraftworxTranslator(debug_mode=debug_mode, target_language=target_language)
        
        # Run translation with configurable parameters
        translator.run_translation(
            input_file=args.input_file,
            output_file=args.output_file,
            save_interval=args.save_interval,
            resume_from=args.resume_from
        )
        
        print("Translation completed successfully!")
        
    except Exception as e:
        logger.error(f"Translation failed: {e}")
        print(f"Translation failed: {e}")


if __name__ == "__main__":
    main()
    