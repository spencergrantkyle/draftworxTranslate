#!/usr/bin/env python3
"""
Configurable Translation Module for Draftworx
Uses dynamic prompt configuration instead of hardcoded prompts
"""

from openai import OpenAI
from prompt_config import PromptConfigManager, PromptConfiguration
from typing import Optional

class ConfigurableTranslator:
    """Translation class that uses configurable prompts"""
    
    def __init__(self, config_manager: Optional[PromptConfigManager] = None):
        self.client = OpenAI()
        self.config_manager = config_manager or PromptConfigManager()
        self.current_config = self.config_manager.load_configuration()
    
    def reload_configuration(self):
        """Reload the current configuration from storage"""
        self.current_config = self.config_manager.load_configuration()
    
    def update_configuration(self, config: PromptConfiguration):
        """Update the current configuration"""
        self.current_config = config
        self.config_manager.save_configuration(config)
    
    def translate_english_value(self, english_value: str, target_language: str) -> str:
        """
        Translate English text using the configured translation prompt
        
        Args:
            english_value: The English text to translate
            target_language: Target language for translation
            
        Returns:
            Translated text
        """
        try:
            # Build the system prompt using the configuration
            system_content = f"""
# Identity
{self.current_config.translation_prompt.identity}

# Instructions
{self.current_config.translation_prompt.instructions.format(target_language=target_language)}"""

            # Add examples if provided
            if self.current_config.translation_prompt.examples:
                system_content += f"""

# Examples
{self.current_config.translation_prompt.examples.format(target_language=target_language)}"""

            # Add critical rules if provided
            if self.current_config.translation_prompt.critical_rules:
                system_content += f"""

# Critical Rules
{self.current_config.translation_prompt.critical_rules.format(target_language=target_language)}"""

            # Add additional notes if provided
            if self.current_config.translation_prompt.additional_notes:
                system_content += f"""

# Additional Notes
{self.current_config.translation_prompt.additional_notes.format(target_language=target_language)}"""

            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": system_content
                    },
                    {
                        "role": "user",
                        "content": f"""Translate the following English sentence into {target_language}:

{english_value}"""
                    }
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error in translate_english_value: {e}")
            return f"Translation error: {str(e)}"

    def translate_formula(self, english_value: str, translated_value: str, english_formula: str, target_language: str) -> str:
        """
        Translate Excel formula using the configured formula prompt
        
        Args:
            english_value: Original English text value
            translated_value: Translated version of the English value
            english_formula: Original Excel formula
            target_language: Target language for translation
            
        Returns:
            Translated Excel formula
        """
        try:
            # Build the system prompt using the configuration
            system_content = f"""
# Identity
{self.current_config.formula_prompt.identity}

# CRITICAL RULES - DO NOT VIOLATE:
{self.current_config.formula_prompt.critical_rules.format(target_language=target_language)}

# Examples of CORRECT translations:
{self.current_config.formula_prompt.examples.format(target_language=target_language)}

# Instructions
{self.current_config.formula_prompt.instructions.format(target_language=target_language)}"""

            # Add additional notes if provided
            if self.current_config.formula_prompt.additional_notes:
                system_content += f"""

# Additional Notes
{self.current_config.formula_prompt.additional_notes.format(target_language=target_language)}"""

            user_content = f"""
Original English value: "{english_value}"
Translated {target_language} value: "{translated_value}"
Original Excel formula: {english_formula}

Instructions:
Update the Excel formula to reflect the {target_language} value where applicable.
ONLY translate hardcoded English words or phrases in quotation marks.
DO NOT change Excel functions (IF, UPPER, LEN, etc.) or named ranges (CompanyName, etc.).
DO NOT change any Excel syntax, operators, or structure.

Return ONLY the final Excel formula with a single apostrophe prefix."""

            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": system_content
                    },
                    {
                        "role": "user",
                        "content": user_content
                    }
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error in translate_formula: {e}")
            return f"Formula translation error: {str(e)}"

    def test_translation(self, test_english_value: str, target_language: str) -> dict:
        """
        Test the current configuration with a sample translation
        
        Args:
            test_english_value: English text to test with
            target_language: Target language for testing
            
        Returns:
            Dictionary with test results
        """
        try:
            # Test value translation
            translated_value = self.translate_english_value(test_english_value, target_language)
            
            # Create a sample formula for testing
            test_formula = f'="{test_english_value}"&SomeNamedRange'
            translated_formula = self.translate_formula(
                test_english_value, 
                translated_value, 
                test_formula, 
                target_language
            )
            
            return {
                "success": True,
                "original_value": test_english_value,
                "translated_value": translated_value,
                "original_formula": test_formula,
                "translated_formula": translated_formula,
                "configuration_name": self.current_config.name
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "configuration_name": self.current_config.name
            }

# Legacy compatibility functions for existing code
_default_translator = None

def get_default_translator():
    """Get or create the default translator instance"""
    global _default_translator
    if _default_translator is None:
        _default_translator = ConfigurableTranslator()
    return _default_translator

def translate_english_value(english_value: str, target_language: str) -> str:
    """Legacy compatibility function"""
    translator = get_default_translator()
    return translator.translate_english_value(english_value, target_language)

def translate_formula(english_value: str, translated_value: str, english_formula: str, target_language: str) -> str:
    """Legacy compatibility function"""
    translator = get_default_translator()
    return translator.translate_formula(english_value, translated_value, english_formula, target_language)

def reload_configuration():
    """Reload the configuration for the default translator"""
    global _default_translator
    if _default_translator:
        _default_translator.reload_configuration()