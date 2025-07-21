#!/usr/bin/env python3
"""
Debug Test Script for Draftworx Translation
Allows interactive testing of translation functions with custom input
"""

import sys
import os
from translate import DraftworxTranslator

def interactive_debug():
    """Interactive debug mode for testing translations"""
    
    print("=" * 80)
    print("Draftworx Translation Debug Tool")
    print("=" * 80)
    print("This tool allows you to test translations interactively.")
    print("You can test individual text translations and formula generations.")
    print("Type 'quit' to exit.")
    print()
    
    try:
        # Initialize translator in debug mode
        translator = DraftworxTranslator(debug_mode=True)
        
        while True:
            print("\n" + "=" * 60)
            print("Choose an option:")
            print("1. Test text translation")
            print("2. Test formula generation")
            print("3. Test both (text + formula)")
            print("4. View named ranges documentation")
            print("5. Quit")
            print("=" * 60)
            
            choice = input("Enter your choice (1-5): ").strip()
            
            if choice == "1":
                test_text_translation(translator)
            elif choice == "2":
                test_formula_generation(translator)
            elif choice == "3":
                test_both(translator)
            elif choice == "4":
                view_named_ranges(translator)
            elif choice == "5" or choice.lower() == "quit":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please enter 1-5.")
                
    except Exception as e:
        print(f"Error initializing translator: {e}")
        print("Please ensure your .env file contains OPENAI_API_KEY")

def test_text_translation(translator):
    """Test text translation with user input"""
    print("\n" + "-" * 40)
    print("TEXT TRANSLATION TEST")
    print("-" * 40)
    
    english_text = input("Enter English text to translate: ").strip()
    if not english_text:
        print("No text entered. Skipping.")
        return
    
    print(f"\nTranslating: '{english_text}'")
    print("Press Enter to continue...")
    input()
    
    try:
        afrikaans_text = translator.translate_text_to_afrikaans(english_text)
        print(f"\nTranslation result: '{afrikaans_text}'")
    except Exception as e:
        print(f"Translation failed: {e}")

def test_formula_generation(translator):
    """Test formula generation with user input"""
    print("\n" + "-" * 40)
    print("FORMULA GENERATION TEST")
    print("-" * 40)
    
    english_value = input("Enter English value: ").strip()
    afrikaans_value = input("Enter Afrikaans value: ").strip()
    english_formula = input("Enter English formula: ").strip()
    
    if not english_formula:
        print("No formula entered. Skipping.")
        return
    
    print(f"\nGenerating formula for:")
    print(f"  English value: '{english_value}'")
    print(f"  Afrikaans value: '{afrikaans_value}'")
    print(f"  English formula: '{english_formula}'")
    print("Press Enter to continue...")
    input()
    
    try:
        afrikaans_formula = translator.generate_afrikaans_formula(
            english_value, afrikaans_value, english_formula
        )
        print(f"\nFormula generation result: '{afrikaans_formula}'")
    except Exception as e:
        print(f"Formula generation failed: {e}")

def test_both(translator):
    """Test both translation and formula generation"""
    print("\n" + "-" * 40)
    print("COMPLETE TEST (Translation + Formula)")
    print("-" * 40)
    
    english_value = input("Enter English value: ").strip()
    english_formula = input("Enter English formula (optional): ").strip()
    
    if not english_value:
        print("No English value entered. Skipping.")
        return
    
    print(f"\nTesting complete workflow:")
    print(f"  English value: '{english_value}'")
    print(f"  English formula: '{english_formula}'")
    print("Press Enter to continue...")
    input()
    
    try:
        # Step 1: Translate text
        print("\nStep 1: Translating text...")
        afrikaans_value = translator.translate_text_to_afrikaans(english_value)
        print(f"Translation result: '{afrikaans_value}'")
        
        # Step 2: Generate formula (if provided)
        if english_formula:
            print("\nStep 2: Generating formula...")
            afrikaans_formula = translator.generate_afrikaans_formula(
                english_value, afrikaans_value, english_formula
            )
            print(f"Formula result: '{afrikaans_formula}'")
        
        print("\nComplete test finished!")
        
    except Exception as e:
        print(f"Test failed: {e}")

def view_named_ranges(translator):
    """View the named ranges documentation"""
    print("\n" + "-" * 40)
    print("NAMED RANGES DOCUMENTATION")
    print("-" * 40)
    
    if translator.named_ranges_doc:
        print("Named ranges documentation loaded:")
        print("-" * 20)
        print(translator.named_ranges_doc[:2000])  # Show first 2000 chars
        if len(translator.named_ranges_doc) > 2000:
            print("... (truncated)")
    else:
        print("No named ranges documentation found.")
        print("Expected file: Knowledge/DraftworxNamedRanges.md")

if __name__ == "__main__":
    interactive_debug() 