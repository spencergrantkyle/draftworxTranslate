from openai import OpenAI

client = OpenAI()

def translate_english_value(english_value, target_language):
    response = client.responses.create(
        model="gpt-4.1",
        input=[
            {
                "role": "developer",
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

{english_value}"""
            }
        ]
    )
    return response.output_text


def translate_formula(english_value, translated_value, english_formula, target_language):
    response = client.responses.create(
        model="gpt-4.1",
        input=[
            {
                "role": "developer",
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

# Examples of CORRECT translations:

Example 1:
English value: "The company"
{target_language} value: "<translated>"
English formula: ="The company "&CompanyName
{target_language} formula: ="<translated>"&CompanyName

Example 2:
English value: "Total revenue"
{target_language} value: "<translated>"
English formula: =IF(TotalIncome>1000,"Total revenue exceeded","Within budget")
{target_language} formula: =IF(TotalIncome>1000,"<translated exceeded>","<translated within budget>")

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


english_value = "The operating results and statement of financial position of the company are fully set out in the attached financial statements and do not in my opinion require any further comment."
afrikaans_value = translate_english_value(english_value, "Afrikaans")
english_formula = '="The operating results and "&LOWER(GroupAFSPrefix)&"statement of financial position of the "&GroupEntityCase&" are fully set out in the attached financial statements and do not in"&Director_my_our&" opinion require any further comment."'

AfrikaansFormula = translate_formula(english_value, afrikaans_value, english_formula, "Afrikaans")
print(AfrikaansFormula)
