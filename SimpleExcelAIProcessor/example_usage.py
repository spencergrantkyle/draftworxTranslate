#!/usr/bin/env python3
"""
Example usage of the Simple Excel AI Processor
Demonstrates how to use the processor programmatically
"""

from simple_excel_ai_processor import SimpleExcelAIProcessor
import os

def example_translation():
    """Example: Translate text in Excel cells"""
    
    # Initialize the processor
    processor = SimpleExcelAIProcessor()
    
    # Example parameters
    workbook_path = "example_data.xlsx"  # Replace with your file path
    sheet_name = "Sheet1"
    cell_range = "A1:A5"
    custom_prompt = "Translate the following text to Spanish. If it's already in Spanish, translate it to English:"
    
    print("Processing translation example...")
    
    # Process the cells
    results = processor.process_cell_range(workbook_path, sheet_name, cell_range, custom_prompt)
    
    # Save results
    if results:
        output_path = "translation_results.xlsx"
        processor.save_results_to_excel(results, output_path)
        print(f"Translation results saved to: {output_path}")

def example_analysis():
    """Example: Analyze financial data"""
    
    processor = SimpleExcelAIProcessor()
    
    workbook_path = "financial_data.xlsx"  # Replace with your file path
    sheet_name = "Data"
    cell_range = "B2:B20"
    custom_prompt = "Analyze this financial value and provide insights about whether it's positive, negative, or neutral, and suggest any potential concerns or positive indicators:"
    
    print("Processing financial analysis...")
    
    results = processor.process_cell_range(workbook_path, sheet_name, cell_range, custom_prompt)
    
    if results:
        output_path = "financial_analysis_results.xlsx"
        processor.save_results_to_excel(results, output_path)
        print(f"Financial analysis results saved to: {output_path}")

def example_formula_analysis():
    """Example: Analyze Excel formulas"""
    
    processor = SimpleExcelAIProcessor()
    
    workbook_path = "formulas.xlsx"  # Replace with your file path
    sheet_name = "Calculations"
    cell_range = "C1:C10"
    custom_prompt = "Analyze this Excel formula and explain what it calculates in simple terms. If there are any potential issues or improvements, mention them:"
    
    print("Processing formula analysis...")
    
    results = processor.process_cell_range(workbook_path, sheet_name, cell_range, custom_prompt)
    
    if results:
        output_path = "formula_analysis_results.xlsx"
        processor.save_results_to_excel(results, output_path)
        print(f"Formula analysis results saved to: {output_path}")

if __name__ == "__main__":
    print("=== Example Usage of Simple Excel AI Processor ===\n")
    
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("Warning: OPENAI_API_KEY environment variable not set!")
        print("Please set your OpenAI API key before running examples.\n")
    
    print("Available examples:")
    print("1. Translation example")
    print("2. Financial analysis example") 
    print("3. Formula analysis example")
    
    choice = input("\nEnter your choice (1-3) or press Enter to exit: ").strip()
    
    if choice == "1":
        example_translation()
    elif choice == "2":
        example_analysis()
    elif choice == "3":
        example_formula_analysis()
    else:
        print("Exiting...") 