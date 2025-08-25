#!/usr/bin/env python3
"""
Prompt Configuration Management for Draftworx Translation
Handles storage and retrieval of translation prompt templates
"""

import json
import os
from typing import Dict, Any
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class TranslationPrompt:
    """Data class for translation prompt configuration"""
    identity: str
    instructions: str
    examples: str = ""
    critical_rules: str = ""
    additional_notes: str = ""

@dataclass
class FormulaPrompt:
    """Data class for formula translation prompt configuration"""
    identity: str
    critical_rules: str
    examples: str
    instructions: str
    additional_notes: str = ""

@dataclass
class PromptConfiguration:
    """Complete prompt configuration for translation"""
    translation_prompt: TranslationPrompt
    formula_prompt: FormulaPrompt
    name: str = "Default Configuration"
    description: str = ""
    created_at: str = ""
    modified_at: str = ""

class PromptConfigManager:
    """Manages prompt configurations with persistence"""
    
    def __init__(self, config_dir: str = "prompt_configs"):
        self.config_dir = config_dir
        self.config_file = os.path.join(config_dir, "active_config.json")
        self.presets_dir = os.path.join(config_dir, "presets")
        
        # Create directories if they don't exist
        os.makedirs(self.config_dir, exist_ok=True)
        os.makedirs(self.presets_dir, exist_ok=True)
        
        # Initialize with default configuration if none exists
        if not os.path.exists(self.config_file):
            self.save_configuration(self.get_default_configuration())
    
    def get_default_configuration(self) -> PromptConfiguration:
        """Returns the default prompt configuration based on test_prompts.py"""
        
        translation_prompt = TranslationPrompt(
            identity="You are a professional translator specializing in IFRS-compliant financial disclosures.",
            instructions="""- Translate the provided English text into formal, professional {target_language} for use in financial statements.
- Maintain tone, meaning, and structure.
- Use proper grammar and consider singular/plural and gender forms.
- Do not translate variable names or placeholders if present.
- Return only the final translation—no headings, no commentary, no formatting."""
        )
        
        formula_prompt = FormulaPrompt(
            identity="You are an expert Excel formula translator focused on localizing financial statement text without breaking Excel logic.",
            critical_rules="""- DO NOT translate Excel functions like IF, UPPER, LEN, OR, AND, etc.
- DO NOT translate named ranges like CompanyName, Capitalisation, Director_is_are, etc.
- DO NOT translate cell references like A1, B2, etc.
- DO NOT translate operators like =, +, -, *, /, etc.
- DO NOT translate parentheses, commas, or other Excel syntax
- ONLY translate hardcoded English text in quotation marks""",
            examples="""Example 1:
English value: "The company"
{target_language} value: "<translated>"
English formula: ="The company "&CompanyName
{target_language} formula: ="<translated>"&CompanyName

Example 2:
English value: "Total revenue"
{target_language} value: "<translated>"
English formula: =IF(TotalIncome>1000,"Total revenue exceeded","Within budget")
{target_language} formula: =IF(TotalIncome>1000,"<translated exceeded>","<translated within budget>")""",
            instructions="""- You will receive a formula in Excel that contains dynamic named ranges and static text.
- Your task is to translate ONLY the hardcoded English text inside quotation marks to formal {target_language}.
- DO NOT modify Excel logic (e.g., IF, OR, LOWER) or named ranges (e.g., Director_is_are, AFS_Name). 
- The translated formula MUST evaluate to the provided {target_language} sentence.
- Your response must be a valid Excel formula prefixed with a single apostrophe (') to prevent auto-evaluation.
- No additional text, no explanations—just return the formula as a single line."""
        )
        
        return PromptConfiguration(
            translation_prompt=translation_prompt,
            formula_prompt=formula_prompt,
            name="Default IFRS Configuration",
            description="Standard prompt configuration for IFRS financial statement translations",
            created_at=datetime.now().isoformat(),
            modified_at=datetime.now().isoformat()
        )
    
    def load_configuration(self) -> PromptConfiguration:
        """Load the active prompt configuration"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Convert dict back to dataclass
            translation_prompt = TranslationPrompt(**data['translation_prompt'])
            formula_prompt = FormulaPrompt(**data['formula_prompt'])
            
            return PromptConfiguration(
                translation_prompt=translation_prompt,
                formula_prompt=formula_prompt,
                name=data.get('name', 'Unnamed Configuration'),
                description=data.get('description', ''),
                created_at=data.get('created_at', ''),
                modified_at=data.get('modified_at', '')
            )
        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            print(f"Error loading configuration: {e}")
            return self.get_default_configuration()
    
    def save_configuration(self, config: PromptConfiguration) -> bool:
        """Save the prompt configuration"""
        try:
            # Update modification time
            config.modified_at = datetime.now().isoformat()
            
            # Convert to dict for JSON serialization
            config_dict = asdict(config)
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_dict, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Error saving configuration: {e}")
            return False
    
    def save_preset(self, config: PromptConfiguration, preset_name: str) -> bool:
        """Save a configuration as a preset"""
        try:
            # Clean preset name for filename
            safe_name = "".join(c for c in preset_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            preset_file = os.path.join(self.presets_dir, f"{safe_name}.json")
            
            # Update configuration name
            config.name = preset_name
            config.modified_at = datetime.now().isoformat()
            
            config_dict = asdict(config)
            
            with open(preset_file, 'w', encoding='utf-8') as f:
                json.dump(config_dict, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Error saving preset: {e}")
            return False
    
    def load_preset(self, preset_name: str) -> PromptConfiguration:
        """Load a preset configuration"""
        try:
            safe_name = "".join(c for c in preset_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            preset_file = os.path.join(self.presets_dir, f"{safe_name}.json")
            
            with open(preset_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            translation_prompt = TranslationPrompt(**data['translation_prompt'])
            formula_prompt = FormulaPrompt(**data['formula_prompt'])
            
            return PromptConfiguration(
                translation_prompt=translation_prompt,
                formula_prompt=formula_prompt,
                name=data.get('name', preset_name),
                description=data.get('description', ''),
                created_at=data.get('created_at', ''),
                modified_at=data.get('modified_at', '')
            )
        except Exception as e:
            print(f"Error loading preset: {e}")
            return self.get_default_configuration()
    
    def get_available_presets(self) -> list:
        """Get list of available preset configurations"""
        try:
            presets = []
            for filename in os.listdir(self.presets_dir):
                if filename.endswith('.json'):
                    preset_name = filename[:-5]  # Remove .json extension
                    presets.append(preset_name)
            return sorted(presets)
        except Exception:
            return []
    
    def delete_preset(self, preset_name: str) -> bool:
        """Delete a preset configuration"""
        try:
            safe_name = "".join(c for c in preset_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            preset_file = os.path.join(self.presets_dir, f"{safe_name}.json")
            
            if os.path.exists(preset_file):
                os.remove(preset_file)
                return True
            return False
        except Exception as e:
            print(f"Error deleting preset: {e}")
            return False
    
    def export_configuration(self, config: PromptConfiguration, export_path: str) -> bool:
        """Export configuration to a specific file"""
        try:
            config_dict = asdict(config)
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(config_dict, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error exporting configuration: {e}")
            return False
    
    def import_configuration(self, import_path: str) -> PromptConfiguration:
        """Import configuration from a file"""
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            translation_prompt = TranslationPrompt(**data['translation_prompt'])
            formula_prompt = FormulaPrompt(**data['formula_prompt'])
            
            return PromptConfiguration(
                translation_prompt=translation_prompt,
                formula_prompt=formula_prompt,
                name=data.get('name', 'Imported Configuration'),
                description=data.get('description', ''),
                created_at=data.get('created_at', ''),
                modified_at=datetime.now().isoformat()
            )
        except Exception as e:
            print(f"Error importing configuration: {e}")
            return self.get_default_configuration()