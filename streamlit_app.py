#!/usr/bin/env python3
"""
Streamlit Application for Draftworx Translation Visualization
Provides a beautiful UI for monitoring and controlling the translation process
"""

import streamlit as st
import pandas as pd
import time
import os
import json
from datetime import datetime
from typing import Optional, Dict, Any
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Import our existing modules
from csv_reader import CSVReader
from test_prompts import translate_english_value, translate_formula
from configurable_translator import ConfigurableTranslator
from prompt_config import PromptConfigManager, PromptConfiguration, TranslationPrompt, FormulaPrompt
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Draftworx Translation Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling with improved contrast
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .progress-section {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 1rem 0;
    }
    
    .translation-card {
        background: white;
        border: 2px solid #e9ecef;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .english-text {
        background: #e3f2fd;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #2196f3;
        margin: 0.5rem 0;
        color: #0d47a1;
        font-weight: 500;
    }
    
    .afrikaans-text {
        background: #f3e5f5;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #9c27b0;
        margin: 0.5rem 0;
        color: #4a148c;
        font-weight: 500;
    }
    
    .formula-text {
        background: #fff3e0;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #ff9800;
        margin: 0.5rem 0;
        font-family: 'Courier New', monospace;
        color: #e65100;
        font-weight: 500;
        font-size: 0.9rem;
    }
    
    .status-success {
        color: #4caf50;
        font-weight: bold;
    }
    
    .status-error {
        color: #f44336;
        font-weight: bold;
    }
    
    .status-warning {
        color: #ff9800;
        font-weight: bold;
    }
    
    .step-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: bold;
        margin: 0.5rem 0.25rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .step-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    .step-button:disabled {
        background: #cccccc;
        cursor: not-allowed;
        transform: none;
        box-shadow: none;
    }
    
    .processing-container {
        background: #f8f9fa;
        border: 2px solid #dee2e6;
        border-radius: 12px;
        padding: 2rem;
        margin: 1rem 0;
    }
    
    .record-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        text-align: center;
        font-weight: bold;
        font-size: 1.2rem;
    }
</style>
""", unsafe_allow_html=True)

class StreamlitTranslator:
    """
    Streamlit-based translator with real-time visualization
    """
    
    def __init__(self, target_language: str = "Afrikaans"):
        """Initialize the Streamlit translator"""
        self.csv_reader = CSVReader()
        self.session_state = st.session_state
        self.target_language = target_language.capitalize()
        
        # Initialize configurable translator and config manager
        self.config_manager = PromptConfigManager()
        self.configurable_translator = ConfigurableTranslator(self.config_manager)
        
        # Initialize session state variables
        if 'current_df' not in self.session_state:
            self.session_state.current_df = None
        if 'processed_count' not in self.session_state:
            self.session_state.processed_count = 0
        if 'successful_count' not in self.session_state:
            self.session_state.successful_count = 0
        if 'current_index' not in self.session_state:
            self.session_state.current_index = 0
        if 'translation_history' not in self.session_state:
            self.session_state.translation_history = []
        if 'processing_active' not in self.session_state:
            self.session_state.processing_active = False
        if 'start_time' not in self.session_state:
            self.session_state.start_time = None
        if 'backup_files' not in self.session_state:
            self.session_state.backup_files = []
        if 'current_step' not in self.session_state:
            self.session_state.current_step = 0  # 0: not started, 1: translate value, 2: generate formula, 3: complete
        if 'current_translated_value' not in self.session_state:
            self.session_state.current_translated_value = ""
        if 'current_translated_formula' not in self.session_state:
            self.session_state.current_translated_formula = ""
        if 'prompt_config' not in self.session_state:
            self.session_state.prompt_config = self.config_manager.load_configuration()
    
    def load_named_ranges_doc(self) -> str:
        """Load the DraftworxNamedRanges.md file"""
        try:
            if os.path.exists("Knowledge/DraftworxNamedRanges.md"):
                with open("Knowledge/DraftworxNamedRanges.md", "r", encoding="utf-8") as f:
                    return f.read()
            return ""
        except Exception as e:
            st.error(f"Error loading named ranges documentation: {e}")
            return ""
    
    def get_backup_files(self) -> list:
        """Get list of available backup files"""
        backup_dir = "Backup_OutputResults"
        if not os.path.exists(backup_dir):
            return []
        
        backup_files = []
        for file in os.listdir(backup_dir):
            if file.endswith('.csv'):
                file_path = os.path.join(backup_dir, file)
                file_stats = os.stat(file_path)
                backup_files.append({
                    'name': file,
                    'path': file_path,
                    'size': file_stats.st_size,
                    'modified': datetime.fromtimestamp(file_stats.st_mtime)
                })
        
        return sorted(backup_files, key=lambda x: x['modified'], reverse=True)
    
    def load_data(self, file_path: str) -> pd.DataFrame:
        """Load CSV data with proper initialization"""
        try:
            df = self.csv_reader.read_csv(file_path)
            
            # Initialize language columns if they don't exist
            value_col = f'CellValue_{self.target_language}'
            formula_col = f'CellFormula_{self.target_language}'
            if value_col not in df.columns:
                df[value_col] = ''
            if formula_col not in df.columns:
                df[formula_col] = ''
            
            return df
        except Exception as e:
            st.error(f"Error loading data: {e}")
            return None
    
    def translate_text(self, english_text: str) -> str:
        """Translate English text to target language"""
        if not english_text or english_text.strip() == "":
            return ""
        
        try:
            with st.spinner("🔄 Translating text..."):
                # Reload configuration to ensure we're using the latest
                self.configurable_translator.reload_configuration()
                translation = self.configurable_translator.translate_english_value(english_text, self.target_language)
                return translation.strip()
        except Exception as e:
            st.error(f"Error translating text: {e}")
            return english_text
    
    def generate_formula(self, english_value: str, translated_value: str, english_formula: str) -> str:
        """Generate formula in target language"""
        if not english_formula or english_formula.strip() == "":
            return ""
        
        try:
            with st.spinner("🔄 Generating formula..."):
                # Reload configuration to ensure we're using the latest
                self.configurable_translator.reload_configuration()
                formula = self.configurable_translator.translate_formula(english_value, translated_value, english_formula, self.target_language)
                
                # Ensure formula starts with apostrophe
                if not formula.startswith("'"):
                    formula = "'" + formula
                
                return formula.strip()
        except Exception as e:
            st.error(f"Error generating formula: {e}")
            return f"'{english_formula}"
    
    def process_single_record_step_by_step(self, df: pd.DataFrame, index: int):
        """Process a single record step by step with user control"""
        try:
            english_value = str(df.at[index, 'CellValue_English']).strip()
            english_formula = str(df.at[index, 'CellFormula_English']).strip()
            value_col = f'CellValue_{self.target_language}'
            formula_col = f'CellFormula_{self.target_language}'
            
            # Skip if already processed or empty
            if (df.at[index, value_col] and df.at[index, formula_col]) or \
               (not english_value and not english_formula):
                st.success("✅ This record is already processed or empty")
                return True
            
            # Create processing container
            with st.container():
                st.markdown(f'<div class="record-header">📝 Processing Record {index + 1} of {len(df)}</div>', unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Original English:**")
                    st.markdown(f'<div class="english-text">{english_value}</div>', unsafe_allow_html=True)
                
                with col2:
                    st.markdown("**Original Formula:**")
                    st.markdown(f'<div class="formula-text">{english_formula}</div>', unsafe_allow_html=True)
                
                # Step-by-step processing with buttons
                st.markdown("### 🔄 Processing Steps")
                
                # Step 1: Translate value
                if self.session_state.current_step == 0:
                    st.markdown("**Step 1: Translate Value**")
                    st.info(f"Click the button below to translate the English value to {self.target_language}")
                    
                    if st.button("🔄 Translate Value", key=f"translate_{index}", type="primary"):
                        if english_value:
                            self.session_state.current_translated_value = self.translate_text(english_value)
                            self.session_state.current_step = 1
                            st.rerun()
                        else:
                            st.warning("No English value to translate")
                            self.session_state.current_step = 1
                            st.rerun()
                
                # Show translated value if available
                if self.session_state.current_step >= 1 and self.session_state.current_translated_value:
                    st.markdown(f"**Translated Value ({self.target_language}):**")
                    st.markdown(f'<div class="afrikaans-text">{self.session_state.current_translated_value}</div>', unsafe_allow_html=True)
                
                # Step 2: Generate formula
                if self.session_state.current_step == 1:
                    st.markdown("**Step 2: Generate Formula**")
                    st.info(f"Click the button below to generate the {self.target_language} formula")
                    
                    if st.button("🔧 Generate Formula", key=f"formula_{index}", type="primary"):
                        if english_formula:
                            self.session_state.current_translated_formula = self.generate_formula(
                                english_value, self.session_state.current_translated_value, english_formula
                            )
                            self.session_state.current_step = 2
                            st.rerun()
                        else:
                            st.warning("No English formula to generate")
                            self.session_state.current_step = 2
                            st.rerun()
                
                # Show generated formula if available
                if self.session_state.current_step >= 2 and self.session_state.current_translated_formula:
                    st.markdown(f"**Generated Formula ({self.target_language}):**")
                    st.markdown(f'<div class="formula-text">{self.session_state.current_translated_formula}</div>', unsafe_allow_html=True)
                
                # Step 3: Complete and move to next record
                if self.session_state.current_step == 2:
                    st.markdown("**Step 3: Complete Processing**")
                    st.success(f"✅ Translation and formula generation completed for {self.target_language}!")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.button("💾 Save & Complete", key=f"save_{index}", type="primary"):
                            # Save the results to the dataframe
                            df.at[index, value_col] = self.session_state.current_translated_value
                            df.at[index, formula_col] = self.session_state.current_translated_formula
                            
                            # Add to history
                            self.session_state.translation_history.append({
                                'index': index,
                                'english_value': english_value,
                                'translated_value': self.session_state.current_translated_value,
                                'english_formula': english_formula,
                                'translated_formula': self.session_state.current_translated_formula,
                                'timestamp': datetime.now(),
                                'language': self.target_language
                            })
                            
                            # Update counts
                            self.session_state.processed_count += 1
                            self.session_state.successful_count += 1
                            
                            # Reset for next record
                            self.session_state.current_step = 0
                            self.session_state.current_translated_value = ""
                            self.session_state.current_translated_formula = ""
                            self.session_state.current_index = index + 1
                            
                            st.success("✅ Record completed and saved!")
                            st.rerun()
                    
                    with col2:
                        if st.button("⏭️ Skip to Next", key=f"skip_{index}"):
                            # Reset for next record without saving
                            self.session_state.current_step = 0
                            self.session_state.current_translated_value = ""
                            self.session_state.current_translated_formula = ""
                            self.session_state.current_index = index + 1
                            st.rerun()
                
                # Navigation buttons
                st.markdown("### 🧭 Navigation")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("⬅️ Previous Record", key=f"prev_{index}", disabled=index == 0):
                        if index > 0:
                            self.session_state.current_index = index - 1
                            self.session_state.current_step = 0
                            self.session_state.current_translated_value = ""
                            self.session_state.current_translated_formula = ""
                            st.rerun()
                
                with col2:
                    if st.button("🔄 Reset Current", key=f"reset_{index}"):
                        self.session_state.current_step = 0
                        self.session_state.current_translated_value = ""
                        self.session_state.current_translated_formula = ""
                        st.rerun()
                
                with col3:
                    if st.button("➡️ Next Record", key=f"next_{index}", disabled=index >= len(df) - 1):
                        if index < len(df) - 1:
                            self.session_state.current_index = index + 1
                            self.session_state.current_step = 0
                            self.session_state.current_translated_value = ""
                            self.session_state.current_translated_formula = ""
                            st.rerun()
                
                return True
                
        except Exception as e:
            st.error(f"Error processing record {index}: {e}")
            return False
    
    def save_progress(self, df: pd.DataFrame, is_final: bool = False):
        """Save progress to backup file"""
        try:
            backup_dir = "Backup_OutputResults"
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            lang_suffix = self.target_language.lower()
            
            if is_final:
                backup_filename = f"{backup_dir}/final_backup_{lang_suffix}_{self.session_state.successful_count}_{timestamp}.csv"
            else:
                backup_filename = f"{backup_dir}/backup_{lang_suffix}_{self.session_state.successful_count}_{timestamp}.csv"
            
            df.to_csv(backup_filename, index=False, encoding='utf-8')
            
            # Update backup files list
            self.session_state.backup_files = self.get_backup_files()
            
            return backup_filename
            
        except Exception as e:
            st.error(f"Error saving progress: {e}")
            return None
    
    def create_progress_charts(self):
        """Create progress visualization charts"""
        if self.session_state.current_df is None:
            return None
        
        df = self.session_state.current_df
        
        # Calculate statistics
        value_col = f'CellValue_{self.target_language}'
        formula_col = f'CellFormula_{self.target_language}'
        total_records = len(df)
        translated_values = df[value_col].notna().sum()
        translated_formulas = df[formula_col].notna().sum()
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Translation Progress', 'Processing Rate', 'Success Rate', 'Time Elapsed'),
            specs=[[{"type": "pie"}, {"type": "bar"}],
                   [{"type": "indicator"}, {"type": "indicator"}]]
        )
        
        # Pie chart for translation progress
        fig.add_trace(
            go.Pie(
                labels=['Translated', 'Remaining'],
                values=[translated_values, total_records - translated_values],
                hole=0.4,
                marker_colors=['#4caf50', '#ff9800']
            ),
            row=1, col=1
        )
        
        # Bar chart for processing rate
        if self.session_state.translation_history:
            recent_history = self.session_state.translation_history[-10:]  # Last 10 records
            timestamps = [h['timestamp'] for h in recent_history]
            fig.add_trace(
                go.Bar(
                    x=timestamps,
                    y=list(range(1, len(recent_history) + 1)),
                    name='Records Processed'
                ),
                row=1, col=2
            )
        
        # Success rate indicator
        success_rate = (self.session_state.successful_count / max(self.session_state.processed_count, 1)) * 100
        fig.add_trace(
            go.Indicator(
                mode="gauge+number+delta",
                value=success_rate,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Success Rate (%)"},
                gauge={'axis': {'range': [None, 100]},
                       'bar': {'color': "darkblue"},
                       'steps': [{'range': [0, 50], 'color': "lightgray"},
                                {'range': [50, 80], 'color': "yellow"},
                                {'range': [80, 100], 'color': "green"}]}
            ),
            row=2, col=1
        )
        
        # Time elapsed indicator
        if self.session_state.start_time:
            elapsed_time = (datetime.now() - self.session_state.start_time).total_seconds()
            fig.add_trace(
                go.Indicator(
                    mode="number+delta",
                    value=elapsed_time,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Time Elapsed (seconds)"},
                    delta={'reference': 0}
                ),
                row=2, col=2
            )
        
        fig.update_layout(height=600, showlegend=False)
        return fig

def main():
    """Main Streamlit application"""
    
    # Header
    st.markdown('<h1 class="main-header">🌍 Draftworx Translation Dashboard</h1>', unsafe_allow_html=True)
    
    # Sidebar configuration
    st.sidebar.markdown("## ⚙️ Configuration")
    
    # Language selection
    language_options = ["Afrikaans", "French", "German", "Spanish", "Portuguese", "Dutch", "Italian", "Swahili", "Zulu", "Xhosa", "Chinese", "Japanese", "Russian", "Arabic"]
    selected_language = st.sidebar.selectbox("Select target language:", language_options, index=0)
    
    # Initialize translator
    translator = StreamlitTranslator(target_language=selected_language)
    
    # File selection
    st.sidebar.markdown("### 📁 Input File")
    input_file = st.sidebar.selectbox(
        "Select input file:",
        ["SheetFlatFiles/sample_directors.csv", "SheetFlatFiles/directors.csv", "SheetFlatFiles/directors_inafrikaans.csv"],
        index=0
    )
    
    # Backup file selection
    st.sidebar.markdown("### 💾 Resume from Backup")
    backup_files = translator.get_backup_files()
    if backup_files:
        backup_options = ["None"] + [f"{f['name']} ({f['modified'].strftime('%Y-%m-%d %H:%M')})" for f in backup_files]
        selected_backup = st.sidebar.selectbox("Resume from backup:", backup_options, index=0)
        
        if selected_backup != "None":
            backup_index = backup_options.index(selected_backup) - 1
            backup_path = backup_files[backup_index]['path']
        else:
            backup_path = None
    else:
        backup_path = None
        st.sidebar.info("No backup files found")
    
    # Processing settings
    st.sidebar.markdown("### ⚡ Processing Settings")
    auto_save = st.sidebar.checkbox("Auto-save progress", value=True)
    
    # Main content area
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Dashboard", "🔄 Processing", "📈 Analytics", "📋 History", "⚙️ Configuration"])
    
    with tab1:
        st.markdown("## 📊 Translation Dashboard")
        
        # Load data button
        if st.button("🔄 Load Data", type="primary"):
            try:
                if backup_path:
                    st.info(f"Loading from backup: {os.path.basename(backup_path)}")
                    translator.session_state.current_df = translator.load_data(backup_path)
                else:
                    st.info(f"Loading from: {input_file}")
                    translator.session_state.current_df = translator.load_data(input_file)
                
                if translator.session_state.current_df is not None:
                    st.success("✅ Data loaded successfully!")
                    translator.session_state.processed_count = 0
                    translator.session_state.successful_count = 0
                    translator.session_state.current_index = 0
                    translator.session_state.translation_history = []
                    translator.session_state.current_step = 0
                    translator.session_state.start_time = datetime.now()
                else:
                    st.error("❌ Failed to load data")
            except Exception as e:
                st.error(f"Error loading data: {e}")
        
        # Display current data info
        if translator.session_state.current_df is not None:
            df = translator.session_state.current_df
            
            # Metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Records", len(df))
            
            with col2:
                value_col = f'CellValue_{translator.target_language}'
                translated_values = df[value_col].notna().sum()
                st.metric(f"Translated {translator.target_language} Values", translated_values)
            
            with col3:
                formula_col = f'CellFormula_{translator.target_language}'
                translated_formulas = df[formula_col].notna().sum()
                st.metric(f"Translated {translator.target_language} Formulas", translated_formulas)
            
            with col4:
                progress_pct = (translated_values / len(df)) * 100 if len(df) > 0 else 0
                st.metric("Progress", f"{progress_pct:.1f}%")
            
            # Progress chart
            st.markdown("### 📈 Progress Visualization")
            progress_chart = translator.create_progress_charts()
            if progress_chart:
                st.plotly_chart(progress_chart, use_container_width=True)
            
            # Data preview
            st.markdown("### 📋 Data Preview")
            st.dataframe(df.head(10), use_container_width=True)
    
    with tab2:
        st.markdown("## 🔄 Translation Processing")
        
        if translator.session_state.current_df is None:
            st.warning("⚠️ Please load data first in the Dashboard tab")
        else:
            df = translator.session_state.current_df
            
            # Processing controls
            st.markdown("### 🎮 Processing Controls")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if st.button("💾 Save Progress"):
                    backup_file = translator.save_progress(df)
                    if backup_file:
                        st.success(f"Progress saved to: {os.path.basename(backup_file)}")
            
            with col2:
                if st.button("🔄 Reset All"):
                    translator.session_state.current_step = 0
                    translator.session_state.current_translated_value = ""
                    translator.session_state.current_translated_formula = ""
                    st.rerun()
            
            with col3:
                if st.button("📊 View Statistics"):
                    st.info(f"Processed: {translator.session_state.processed_count}")
                    st.info(f"Successful: {translator.session_state.successful_count}")
                    if translator.session_state.processed_count > 0:
                        success_rate = (translator.session_state.successful_count / translator.session_state.processed_count) * 100
                        st.info(f"Success Rate: {success_rate:.1f}%")
            
            with col4:
                if st.button("🏁 Complete All"):
                    st.info(f"This will process all remaining records automatically in {translator.target_language}")
                    # Auto-process remaining records
                    for i in range(translator.session_state.current_index, len(df)):
                        english_value = str(df.at[i, 'CellValue_English']).strip()
                        english_formula = str(df.at[i, 'CellFormula_English']).strip()
                        
                        if not (df.at[i, f'CellValue_{translator.target_language}'] and df.at[i, f'CellFormula_{translator.target_language}']):
                            if english_value:
                                translated_value = translator.translate_text(english_value)
                                df.at[i, f'CellValue_{translator.target_language}'] = translated_value
                            
                            if english_formula:
                                translated_formula = translator.generate_formula(
                                    english_value, translated_value if english_value else "", english_formula
                                )
                                df.at[i, f'CellFormula_{translator.target_language}'] = translated_formula
                            
                            translator.session_state.processed_count += 1
                            translator.session_state.successful_count += 1
                    
                    translator.session_state.current_index = len(df)
                    st.success(f"✅ All records processed in {translator.target_language}!")
                    st.rerun()
            
            # Current record processing
            st.markdown("### 📝 Current Record Processing")
            
            if translator.session_state.current_index < len(df):
                translator.process_single_record_step_by_step(df, translator.session_state.current_index)
            else:
                st.success("🎉 All records have been processed!")
                
                # Final save option
                if st.button("💾 Save Final Results", type="primary"):
                    backup_file = translator.save_progress(df, is_final=True)
                    if backup_file:
                        st.success(f"Final results saved to: {os.path.basename(backup_file)}")
    
    with tab3:
        st.markdown("## 📈 Analytics")
        
        if translator.session_state.current_df is not None and translator.session_state.translation_history:
            # Processing statistics
            st.markdown("### 📊 Processing Statistics")
            
            # Time analysis
            if len(translator.session_state.translation_history) > 1:
                timestamps = [h['timestamp'] for h in translator.session_state.translation_history]
                processing_times = []
                
                for i in range(1, len(timestamps)):
                    time_diff = (timestamps[i] - timestamps[i-1]).total_seconds()
                    processing_times.append(time_diff)
                
                avg_time = sum(processing_times) / len(processing_times)
                st.metric("Average Processing Time", f"{avg_time:.2f} seconds per record")
            
            # Success rate
            success_rate = (translator.session_state.successful_count / max(translator.session_state.processed_count, 1)) * 100
            st.metric("Success Rate", f"{success_rate:.1f}%")
            
            # Translation history chart
            if translator.session_state.translation_history:
                st.markdown("### 📈 Translation History")
                
                history_df = pd.DataFrame(translator.session_state.translation_history)
                history_df['timestamp'] = pd.to_datetime(history_df['timestamp'])
                
                fig = px.line(history_df, x='timestamp', y='index', 
                            title='Translation Progress Over Time')
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("📊 Analytics will be available after processing some records")
    
    with tab4:
        st.markdown("## 📋 Translation History")
        
        if translator.session_state.translation_history:
            # Recent translations
            st.markdown("### 🔄 Recent Translations")
            
            for i, record in enumerate(reversed(translator.session_state.translation_history[-10:])):
                with st.expander(f"Record {record['index'] + 1} - {record['timestamp'].strftime('%H:%M:%S')}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**English Value:**")
                        st.markdown(f'<div class="english-text">{record["english_value"]}</div>', unsafe_allow_html=True)
                        
                        st.markdown("**English Formula:**")
                        st.markdown(f'<div class="formula-text">{record["english_formula"]}</div>', unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown(f"**{translator.target_language} Value:**")
                        st.markdown(f'<div class="afrikaans-text">{record["translated_value"]}</div>', unsafe_allow_html=True)
                        
                        st.markdown(f"**{translator.target_language} Formula:**")
                        st.markdown(f'<div class="formula-text">{record["translated_formula"]}</div>', unsafe_allow_html=True)
        else:
            st.info("📋 Translation history will appear here after processing records")
        
        # Backup files
        st.markdown("### 💾 Backup Files")
        backup_files = translator.get_backup_files()
        
        if backup_files:
            for backup in backup_files:
                with st.expander(f"{backup['name']} - {backup['modified'].strftime('%Y-%m-%d %H:%M:%S')}"):
                    st.write(f"**Size:** {backup['size'] / 1024:.1f} KB")
                    st.write(f"**Modified:** {backup['modified'].strftime('%Y-%m-%d %H:%M:%S')}")
                    
                    if st.button(f"Load {backup['name']}", key=f"load_{backup['name']}"):
                        translator.session_state.current_df = translator.load_data(backup['path'])
                        st.success(f"Loaded backup: {backup['name']}")
                        st.rerun()
        else:
            st.info("No backup files found")
    
    with tab5:
        st.markdown("## ⚙️ Prompt Configuration")
        st.markdown("Configure the AI prompts used for translation and formula generation.")
        
        # Load current configuration
        config = translator.config_manager.load_configuration()
        
        # Configuration management
        st.markdown("### 📁 Configuration Management")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Preset management
            st.markdown("#### 📋 Presets")
            available_presets = translator.config_manager.get_available_presets()
            
            if available_presets:
                selected_preset = st.selectbox("Load Preset:", ["Current"] + available_presets)
                
                if selected_preset != "Current" and st.button("Load Preset"):
                    config = translator.config_manager.load_preset(selected_preset)
                    translator.config_manager.save_configuration(config)
                    st.success(f"Loaded preset: {selected_preset}")
                    st.rerun()
            else:
                st.info("No presets saved yet")
        
        with col2:
            # Save preset
            st.markdown("#### 💾 Save as Preset")
            preset_name = st.text_input("Preset Name:")
            if preset_name and st.button("Save Preset"):
                if translator.config_manager.save_preset(config, preset_name):
                    st.success(f"Saved preset: {preset_name}")
                else:
                    st.error("Failed to save preset")
        
        with col3:
            # Import/Export
            st.markdown("#### 📤 Import/Export")
            if st.button("Export Configuration"):
                export_path = f"prompt_configs/export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                if translator.config_manager.export_configuration(config, export_path):
                    st.success(f"Configuration exported to: {export_path}")
                else:
                    st.error("Failed to export configuration")
        
        # Configuration Info
        st.markdown("### ℹ️ Current Configuration")
        col1, col2 = st.columns(2)
        
        with col1:
            st.info(f"**Name:** {config.name}")
            st.info(f"**Created:** {config.created_at}")
        
        with col2:
            st.info(f"**Modified:** {config.modified_at}")
            if config.description:
                st.info(f"**Description:** {config.description}")
        
        # Configuration Editor
        st.markdown("### ✏️ Edit Configuration")
        
        # Basic configuration details
        with st.expander("📝 Basic Configuration Details", expanded=True):
            new_name = st.text_input("Configuration Name:", value=config.name)
            new_description = st.text_area("Description:", value=config.description, height=100)
        
        # Translation prompt configuration
        with st.expander("🌍 Translation Prompt Configuration", expanded=False):
            st.markdown("#### AI Identity for Text Translation")
            translation_identity = st.text_area(
                "Identity:", 
                value=config.translation_prompt.identity,
                height=100,
                help="Define who the AI is for translation tasks"
            )
            
            st.markdown("#### Translation Instructions")
            translation_instructions = st.text_area(
                "Instructions:", 
                value=config.translation_prompt.instructions,
                height=200,
                help="Detailed instructions for text translation. Use {target_language} placeholder for dynamic language insertion."
            )
            
            st.markdown("#### Translation Examples (Optional)")
            translation_examples = st.text_area(
                "Examples:", 
                value=config.translation_prompt.examples,
                height=150,
                help="Provide examples of good translations"
            )
            
            st.markdown("#### Critical Rules for Translation (Optional)")
            translation_rules = st.text_area(
                "Critical Rules:", 
                value=config.translation_prompt.critical_rules,
                height=100,
                help="Important rules that must be followed"
            )
            
            st.markdown("#### Additional Notes (Optional)")
            translation_notes = st.text_area(
                "Additional Notes:", 
                value=config.translation_prompt.additional_notes,
                height=100,
                help="Any additional guidance for the AI"
            )
        
        # Formula prompt configuration
        with st.expander("📊 Formula Translation Prompt Configuration", expanded=False):
            st.markdown("#### AI Identity for Formula Translation")
            formula_identity = st.text_area(
                "Identity:", 
                value=config.formula_prompt.identity,
                height=100,
                help="Define who the AI is for formula translation tasks",
                key="formula_identity"
            )
            
            st.markdown("#### Critical Rules for Formula Translation")
            formula_rules = st.text_area(
                "Critical Rules:", 
                value=config.formula_prompt.critical_rules,
                height=200,
                help="Essential rules for formula translation - what NOT to translate",
                key="formula_rules"
            )
            
            st.markdown("#### Formula Translation Examples")
            formula_examples = st.text_area(
                "Examples:", 
                value=config.formula_prompt.examples,
                height=300,
                help="Concrete examples of correct formula translations. Use {target_language} placeholder.",
                key="formula_examples"
            )
            
            st.markdown("#### Formula Translation Instructions")
            formula_instructions = st.text_area(
                "Instructions:", 
                value=config.formula_prompt.instructions,
                height=200,
                help="Step-by-step instructions for formula translation",
                key="formula_instructions"
            )
            
            st.markdown("#### Additional Notes for Formulas (Optional)")
            formula_notes = st.text_area(
                "Additional Notes:", 
                value=config.formula_prompt.additional_notes,
                height=100,
                help="Any additional guidance for formula translation",
                key="formula_notes"
            )
        
        # Test Configuration
        with st.expander("🧪 Test Configuration", expanded=False):
            st.markdown("#### Test Your Configuration")
            test_text = st.text_input(
                "Test English Text:", 
                value="The operating results and statement of financial position of the company are fully set out in the attached financial statements.",
                help="Enter text to test translation with current configuration"
            )
            
            test_language = st.selectbox(
                "Test Language:", 
                ["Afrikaans", "French", "German", "Spanish", "Portuguese", "Dutch", "Italian"],
                help="Select language for testing"
            )
            
            if st.button("🧪 Test Configuration"):
                if test_text:
                    # Create temporary configuration for testing
                    temp_config = PromptConfiguration(
                        translation_prompt=TranslationPrompt(
                            identity=translation_identity,
                            instructions=translation_instructions,
                            examples=translation_examples,
                            critical_rules=translation_rules,
                            additional_notes=translation_notes
                        ),
                        formula_prompt=FormulaPrompt(
                            identity=formula_identity,
                            critical_rules=formula_rules,
                            examples=formula_examples,
                            instructions=formula_instructions,
                            additional_notes=formula_notes
                        ),
                        name=new_name,
                        description=new_description
                    )
                    
                    # Test with temporary configuration
                    temp_translator = ConfigurableTranslator()
                    temp_translator.current_config = temp_config
                    
                    test_results = temp_translator.test_translation(test_text, test_language)
                    
                    if test_results["success"]:
                        st.success("✅ Test completed successfully!")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown("**Original:**")
                            st.markdown(f'<div style="background-color: #f0f0f0; padding: 10px; border-radius: 5px;">{test_results["original_value"]}</div>', unsafe_allow_html=True)
                            
                            st.markdown("**Original Formula:**")
                            st.markdown(f'<div style="background-color: #f0f0f0; padding: 10px; border-radius: 5px; font-family: monospace;">{test_results["original_formula"]}</div>', unsafe_allow_html=True)
                        
                        with col2:
                            st.markdown(f"**{test_language} Translation:**")
                            st.markdown(f'<div style="background-color: #e8f5e8; padding: 10px; border-radius: 5px;">{test_results["translated_value"]}</div>', unsafe_allow_html=True)
                            
                            st.markdown(f"**{test_language} Formula:**")
                            st.markdown(f'<div style="background-color: #e8f5e8; padding: 10px; border-radius: 5px; font-family: monospace;">{test_results["translated_formula"]}</div>', unsafe_allow_html=True)
                    else:
                        st.error(f"❌ Test failed: {test_results['error']}")
                else:
                    st.warning("Please enter test text")
        
        # Save configuration
        st.markdown("### 💾 Save Configuration")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("💾 Save Configuration", type="primary"):
                # Create new configuration object
                new_config = PromptConfiguration(
                    translation_prompt=TranslationPrompt(
                        identity=translation_identity,
                        instructions=translation_instructions,
                        examples=translation_examples,
                        critical_rules=translation_rules,
                        additional_notes=translation_notes
                    ),
                    formula_prompt=FormulaPrompt(
                        identity=formula_identity,
                        critical_rules=formula_rules,
                        examples=formula_examples,
                        instructions=formula_instructions,
                        additional_notes=formula_notes
                    ),
                    name=new_name,
                    description=new_description,
                    created_at=config.created_at,
                    modified_at=datetime.now().isoformat()
                )
                
                if translator.config_manager.save_configuration(new_config):
                    st.success("✅ Configuration saved successfully!")
                    st.info("The new configuration will be used for all future translations.")
                    # Update session state
                    translator.session_state.prompt_config = new_config
                else:
                    st.error("❌ Failed to save configuration")
        
        with col2:
            if st.button("🔄 Reset to Default"):
                default_config = translator.config_manager.get_default_configuration()
                if translator.config_manager.save_configuration(default_config):
                    st.success("✅ Reset to default configuration!")
                    st.rerun()
                else:
                    st.error("❌ Failed to reset configuration")
        
        with col3:
            if st.button("↩️ Reload Configuration"):
                config = translator.config_manager.load_configuration()
                st.success("✅ Configuration reloaded!")
                st.rerun()

if __name__ == "__main__":
    main() 