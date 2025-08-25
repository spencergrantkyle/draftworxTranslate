# CrewAI Integration Guide: LLM Translation Tools

## Overview

This guide shows how to extract the LLM functions from the Draftworx Translation project and integrate them as CrewAI tools, rather than using the translator as a single tool. This approach gives you more granular control and allows CrewAI agents to use individual translation capabilities.

---

## 1. **Extracted LLM Functions**

### Core Translation Functions

The project contains two main LLM functions that can be extracted as CrewAI tools:

1. **`translate_english_value`** - Translates English text to target language
2. **`translate_formula`** - Translates Excel formulas while preserving logic

---

## 2. **CrewAI Tool Implementation**

### Tool 1: Text Translation Tool

```python
from crewai import Tool
from openai import OpenAI

client = OpenAI()

def translate_text_tool(english_text: str, target_language: str) -> str:
    """
    Translate English text to target language for financial statements
    
    Args:
        english_text: The English text to translate
        target_language: The target language (e.g., "French", "Spanish", "German")
    
    Returns:
        Translated text in the target language
    """
    response = client.responses.create(
        model="gpt-4.1",
        input=[
            {
                "role": "system",
                "content": f"""
# Identity
You are a professional translator specializing in IFRS-compliant financial disclosures.

# Instructions
- Translate the provided English text into formal, professional {target_language} for use in financial statements.
- Maintain tone, meaning, and structure.
- Use proper grammar and consider singular/plural and gender forms.
- Do not translate variable names or placeholders if present.
- Return only the final translation—no headings, no commentary, no formatting.
"""
            },
            {
                "role": "user",
                "content": f"""Translate the following English sentence into {target_language}:

{english_text}"""
            }
        ]
    )
    return response.output_text

# Create CrewAI Tool
text_translation_tool = Tool(
    name="translate_text",
    description="Translate English financial text to any target language while maintaining professional tone and IFRS compliance",
    func=translate_text_tool
)
```

### Tool 2: Formula Translation Tool

```python
def translate_excel_formula_tool(english_value: str, translated_value: str, english_formula: str, target_language: str) -> str:
    """
    Translate Excel formulas while preserving Excel logic and named ranges
    
    Args:
        english_value: Original English text value
        translated_value: Translated text value
        english_formula: Original Excel formula
        target_language: Target language for translation
    
    Returns:
        Translated Excel formula with apostrophe prefix
    """
    response = client.responses.create(
        model="gpt-4.1",
        input=[
            {
                "role": "system",
                "content": f"""
# Identity
You are an expert Excel formula translator focused on localizing financial statement text without breaking Excel logic.

# CRITICAL RULES - DO NOT VIOLATE:
- DO NOT translate Excel functions like IF, UPPER, LEN, OR, AND, etc.
- DO NOT translate named ranges like CompanyName, Capitalisation, Director_is_are, etc.
- DO NOT translate cell references like A1, B2, etc.
- DO NOT translate operators like =, +, -, *, /, etc.
- DO NOT translate parentheses, commas, or other Excel syntax
- ONLY translate hardcoded English text in quotation marks

# Instructions
- You will receive a formula in Excel that contains dynamic named ranges and static text.
- Your task is to translate ONLY the hardcoded English text inside quotation marks to formal {target_language}.
- DO NOT modify Excel logic (e.g., IF, OR, LOWER) or named ranges (e.g., Director_is_are, AFS_Name). 
- The translated formula MUST evaluate to the provided {target_language} sentence.
- Your response must be a valid Excel formula prefixed with a single apostrophe (') to prevent auto-evaluation.
- No additional text, no explanations—just return the formula as a single line.
"""
            },
            {
                "role": "user",
                "content": f"""
Original English value: "{english_value}"
Translated {target_language} value: "{translated_value}"
Original Excel formula: {english_formula}

Instructions:
Update the Excel formula to reflect the {target_language} value where applicable.
ONLY translate hardcoded English words or phrases in quotation marks.
DO NOT change Excel functions (IF, UPPER, LEN, etc.) or named ranges (CompanyName, etc.).
DO NOT change any Excel syntax, operators, or structure.

Return ONLY the final Excel formula with a single apostrophe prefix.
"""
            }
        ]
    )
    return response.output_text

# Create CrewAI Tool
formula_translation_tool = Tool(
    name="translate_excel_formula",
    description="Translate Excel formulas to target language while preserving Excel functions, named ranges, and syntax",
    func=translate_excel_formula_tool
)
```

---

## 3. **CrewAI Agent Implementation**

### Financial Translation Agent

```python
from crewai import Agent

# Create a specialized translation agent
translation_agent = Agent(
    role="Financial Translation Specialist",
    goal="Accurately translate financial statements and Excel formulas while maintaining IFRS compliance and Excel functionality",
    backstory="""You are an expert in financial translation with deep knowledge of IFRS standards, 
    Excel formulas, and multiple languages. You specialize in translating financial disclosures 
    while preserving the technical integrity of Excel formulas and maintaining professional tone.""",
    tools=[text_translation_tool, formula_translation_tool],
    verbose=True,
    allow_delegation=False
)
```

### Data Processing Agent

```python
import pandas as pd

def process_csv_data_tool(input_file: str, target_language: str) -> dict:
    """
    Process CSV data and prepare for translation
    
    Args:
        input_file: Path to input CSV file
        target_language: Target language for translation
    
    Returns:
        Dictionary with processing results and data summary
    """
    try:
        df = pd.read_csv(input_file, encoding='utf-8')
        
        # Add target language columns if they don't exist
        value_col = f'CellValue_{target_language}'
        formula_col = f'CellFormula_{target_language}'
        
        if value_col not in df.columns:
            df[value_col] = ''
        if formula_col not in df.columns:
            df[formula_col] = ''
        
        # Count records that need translation
        english_values = df['CellValue_English'].notna().sum()
        english_formulas = df['CellFormula_English'].notna().sum()
        
        return {
            "total_records": len(df),
            "english_values": english_values,
            "english_formulas": english_formulas,
            "target_language": target_language,
            "value_column": value_col,
            "formula_column": formula_col,
            "status": "ready_for_translation"
        }
    except Exception as e:
        return {"error": str(e), "status": "failed"}

# Create CrewAI Tool
csv_processing_tool = Tool(
    name="process_csv_data",
    description="Process CSV files and prepare data for translation by adding target language columns",
    func=process_csv_data_tool
)

# Create data processing agent
data_agent = Agent(
    role="Data Processing Specialist",
    goal="Prepare and validate CSV data for translation processing",
    backstory="""You are a data processing expert who specializes in preparing financial data 
    for translation. You ensure data integrity and proper column structure before translation begins.""",
    tools=[csv_processing_tool],
    verbose=True,
    allow_delegation=False
)
```

---

## 4. **CrewAI Task Implementation**

### Task 1: Data Preparation

```python
from crewai import Task

prepare_data_task = Task(
    description="""
    1. Load the CSV file from the provided input path
    2. Validate that required columns exist (CellValue_English, CellFormula_English)
    3. Add target language columns if they don't exist
    4. Return a summary of the data structure and translation requirements
    """,
    agent=data_agent,
    expected_output="""
    A dictionary containing:
    - total_records: Number of records to process
    - english_values: Number of English values to translate
    - english_formulas: Number of English formulas to translate
    - target_language: The language being translated to
    - value_column: Name of the target language value column
    - formula_column: Name of the target language formula column
    - status: "ready_for_translation" or "failed"
    """
)
```

### Task 2: Translation Processing

```python
translation_task = Task(
    description="""
    For each record in the CSV data:
    1. Extract the English value and formula
    2. Use the text translation tool to translate the English value
    3. Use the formula translation tool to translate the Excel formula
    4. Update the target language columns with the translations
    5. Provide progress updates and handle any translation errors
    """,
    agent=translation_agent,
    expected_output="""
    A comprehensive report including:
    - Number of records processed
    - Number of successful translations
    - Number of failed translations
    - List of any errors encountered
    - Updated CSV data with translations
    """
)
```

---

## 5. **Complete CrewAI Crew Implementation**

```python
from crewai import Crew

def create_translation_crew():
    """Create a CrewAI crew for financial translation"""
    
    # Create agents
    data_agent = Agent(
        role="Data Processing Specialist",
        goal="Prepare and validate CSV data for translation processing",
        backstory="""You are a data processing expert who specializes in preparing financial data 
        for translation. You ensure data integrity and proper column structure before translation begins.""",
        tools=[csv_processing_tool],
        verbose=True,
        allow_delegation=False
    )
    
    translation_agent = Agent(
        role="Financial Translation Specialist",
        goal="Accurately translate financial statements and Excel formulas while maintaining IFRS compliance and Excel functionality",
        backstory="""You are an expert in financial translation with deep knowledge of IFRS standards, 
        Excel formulas, and multiple languages. You specialize in translating financial disclosures 
        while preserving the technical integrity of Excel formulas and maintaining professional tone.""",
        tools=[text_translation_tool, formula_translation_tool],
        verbose=True,
        allow_delegation=False
    )
    
    # Create tasks
    prepare_data_task = Task(
        description="Prepare CSV data for translation by validating structure and adding target language columns",
        agent=data_agent,
        expected_output="Data processing summary with record counts and column information"
    )
    
    translation_task = Task(
        description="Translate English values and formulas to the target language while preserving Excel functionality",
        agent=translation_agent,
        expected_output="Complete translation report with updated data and error summary"
    )
    
    # Create crew
    crew = Crew(
        agents=[data_agent, translation_agent],
        tasks=[prepare_data_task, translation_task],
        verbose=True
    )
    
    return crew

# Usage
def run_translation_crew(input_file: str, target_language: str):
    """Run the translation crew with specified parameters"""
    crew = create_translation_crew()
    
    # Set context for the crew
    context = {
        "input_file": input_file,
        "target_language": target_language
    }
    
    result = crew.kickoff(context)
    return result
```

---

## 6. **Integration with Streamlit UI**

```python
import streamlit as st
from crewai import Crew

def streamlit_crew_interface():
    st.title("Financial Translation with CrewAI")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")
        target_language = st.selectbox(
            "Target Language",
            ["Afrikaans", "French", "Spanish", "German", "Portuguese", "Italian", "Dutch"]
        )
        
        input_file = st.file_uploader(
            "Upload CSV File",
            type=['csv'],
            help="Upload a CSV file with CellValue_English and CellFormula_English columns"
        )
    
    # Main interface
    if input_file is not None:
        if st.button("Start Translation"):
            with st.spinner("Processing with CrewAI..."):
                # Save uploaded file temporarily
                temp_file = f"temp_{input_file.name}"
                with open(temp_file, "wb") as f:
                    f.write(input_file.getbuffer())
                
                try:
                    # Run CrewAI crew
                    result = run_translation_crew(temp_file, target_language)
                    
                    # Display results
                    st.success("Translation completed!")
                    st.json(result)
                    
                except Exception as e:
                    st.error(f"Translation failed: {str(e)}")
                finally:
                    # Clean up temp file
                    import os
                    if os.path.exists(temp_file):
                        os.remove(temp_file)

if __name__ == "__main__":
    streamlit_crew_interface()
```

---

## 7. **Benefits of This Approach**

1. **Granular Control**: Each translation function is a separate tool that can be used independently
2. **Specialized Agents**: Different agents handle different aspects (data processing vs. translation)
3. **Scalability**: Easy to add new tools or modify existing ones
4. **Error Handling**: Each tool can have its own error handling and validation
5. **Flexibility**: Tools can be used in different combinations for different use cases
6. **Monitoring**: CrewAI provides detailed logging and monitoring of tool usage

---

## 8. **Next Steps**

1. **Install CrewAI**: `pip install crewai`
2. **Set up environment**: Configure OpenAI API key
3. **Test individual tools**: Verify each tool works independently
4. **Create agents**: Implement the specialized agents
5. **Build tasks**: Create the translation workflow tasks
6. **Deploy crew**: Run the complete translation crew
7. **Add UI**: Integrate with Streamlit or other UI framework

This approach gives you maximum flexibility and control while leveraging CrewAI's powerful agent-based workflow capabilities. 