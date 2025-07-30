# 🎛️ Draftworx Translation Configuration Guide

## Overview

The Draftworx Translation system now includes a powerful **Prompt Configuration System** that allows you to customize how the AI processes translations and formulas. This guide explains how to use and manage these configurations.

## 🚀 Quick Start

### 1. Run the Streamlit Application
```bash
python run_streamlit.py
```

### 2. Navigate to Configuration Tab
- Open the Streamlit app in your browser
- Click on the **"⚙️ Configuration"** tab
- You'll see the prompt configuration interface

### 3. Set Up Default Presets (First Time)
```bash
python create_default_presets.py
```
This creates specialized preset configurations for different use cases.

## 📋 Understanding Configurations

### Configuration Components

Each configuration consists of two main parts:

1. **Translation Prompt** - Controls how English text is translated
2. **Formula Prompt** - Controls how Excel formulas are translated

### Key Fields

#### Translation Prompt
- **Identity**: Defines who the AI is (e.g., "financial translator", "legal expert")
- **Instructions**: Detailed rules for translation behavior
- **Examples**: Sample translations to guide the AI
- **Critical Rules**: Must-follow rules for translation
- **Additional Notes**: Extra guidance and context

#### Formula Prompt
- **Identity**: Defines the AI's role for formula translation
- **Critical Rules**: What NOT to translate (Excel functions, named ranges, etc.)
- **Examples**: Sample formula translations with before/after examples
- **Instructions**: Step-by-step formula translation guidance
- **Additional Notes**: Extra context for formula handling

## 🎯 Using the Configuration Interface

### Loading Presets

1. **View Available Presets**
   - Go to Configuration tab → Configuration Management
   - See list of available presets in the dropdown

2. **Load a Preset**
   - Select a preset from the dropdown
   - Click "Load Preset"
   - The configuration will be applied immediately

### Available Default Presets

| Preset Name | Best For | Key Features |
|-------------|----------|--------------|
| **Financial IFRS Specialist** | Financial statements, annual reports | IFRS/GAAP expertise, regulatory compliance |
| **Legal Corporate Documents** | Board resolutions, legal notices | Legal terminology, formal language |
| **General Business Communications** | Business reports, corporate docs | Professional tone, business terminology |
| **Technical Documentation** | Software docs, system specs | Technical accuracy, system compatibility |

### Editing Configurations

1. **Basic Configuration Details**
   - Configuration Name: Give your configuration a descriptive name
   - Description: Explain what this configuration is for

2. **Translation Prompt Configuration**
   - Expand the "🌍 Translation Prompt Configuration" section
   - Edit the Identity, Instructions, Examples, etc.
   - Use `{target_language}` placeholder for dynamic language insertion

3. **Formula Translation Configuration**
   - Expand the "📊 Formula Translation Prompt Configuration" section
   - Edit the Critical Rules, Examples, Instructions
   - Focus on what should NOT be translated in formulas

### Testing Configurations

1. **Use the Test Feature**
   - Expand "🧪 Test Configuration"
   - Enter test text (use the default or your own)
   - Select a target language
   - Click "🧪 Test Configuration"

2. **Review Results**
   - See both the translated text and formula
   - Verify the translation quality meets your needs
   - Adjust configuration if needed

### Saving Configurations

1. **Save Current Configuration**
   - Click "💾 Save Configuration" to make changes active
   - All future translations will use the updated configuration

2. **Save as New Preset**
   - Enter a preset name
   - Click "Save Preset"
   - The configuration becomes available as a reusable preset

## ⚙️ Advanced Configuration Tips

### Effective Prompt Writing

#### Translation Prompts
```markdown
# Good Examples:
- "Translate into formal, professional {target_language} for financial statements"
- "Maintain technical accuracy while ensuring natural flow"
- "Use appropriate singular/plural forms and gender agreements"

# Avoid:
- Vague instructions like "translate well"
- Language-specific instructions without {target_language} placeholder
```

#### Formula Prompts
```markdown
# Critical Rules Should Include:
- DO NOT translate Excel functions (IF, SUM, VLOOKUP, etc.)
- DO NOT translate named ranges (CompanyName, TotalRevenue, etc.)
- DO NOT translate cell references (A1, B2, etc.)
- ONLY translate hardcoded text in quotation marks

# Good Examples Show:
- Before: ="Total revenue: "&TEXT(Revenue,"#,##0")
- After: ="Revenu total: "&TEXT(Revenue,"#,##0")
```

### Language Placeholders

Use `{target_language}` in your prompts for dynamic language insertion:

```markdown
# Good:
"Translate into formal {target_language} for business use"

# This becomes:
"Translate into formal Afrikaans for business use"
"Translate into formal Spanish for business use"
```

### Multiple Configurations for Different Contexts

Consider creating separate configurations for:
- **Financial Statements**: IFRS compliance, regulatory language
- **Legal Documents**: Formal legal terminology, contractual language
- **Technical Docs**: System specifications, software documentation
- **Marketing Content**: Persuasive language, cultural adaptation

## 🔄 Configuration Management

### Preset Management

#### Creating Presets
1. Configure your prompts perfectly
2. Enter a descriptive preset name
3. Click "Save Preset"
4. The preset becomes available for future use

#### Sharing Presets
1. Export configuration: Click "Export Configuration"
2. Share the exported JSON file
3. Others can import it using the import feature

#### Organizing Presets
Use clear, descriptive names:
- ✅ "Financial IFRS Quarterly Reports"
- ✅ "Legal Board Resolutions"
- ✅ "Technical API Documentation"
- ❌ "Config1", "Test", "My Settings"

### Backup and Recovery

#### Automatic Backups
- Configurations are automatically saved to `prompt_configs/active_config.json`
- Presets are saved in `prompt_configs/presets/`

#### Manual Exports
- Use "Export Configuration" for manual backups
- Export before making major changes
- Share exports with team members

## 🚨 Best Practices

### Configuration Development

1. **Start with a Preset**
   - Begin with the closest default preset
   - Modify rather than starting from scratch

2. **Test Thoroughly**
   - Use the built-in test feature
   - Test with various text samples
   - Test different target languages

3. **Iterate and Refine**
   - Start with basic instructions
   - Add examples and rules as needed
   - Refine based on actual translation results

### Formula Configuration

1. **Be Explicit About What NOT to Translate**
   - List specific Excel functions
   - Mention named ranges and cell references
   - Emphasize preserving calculation logic

2. **Provide Clear Examples**
   - Show exact before/after formula pairs
   - Include real-world examples from your sheets
   - Cover different formula complexity levels

### Quality Assurance

1. **Regular Testing**
   - Test configurations monthly
   - Verify translations meet quality standards
   - Update based on user feedback

2. **Version Control**
   - Export important configurations
   - Keep dated backups of major configurations
   - Document changes and reasons

## 🔧 Troubleshooting

### Common Issues

#### Poor Translation Quality
- **Check Identity**: Is the AI identity specific enough?
- **Add Examples**: Provide more concrete examples
- **Refine Instructions**: Make instructions more specific
- **Test Different Languages**: Some configurations work better for certain languages

#### Formula Translation Errors
- **Review Critical Rules**: Ensure all Excel elements are covered
- **Check Examples**: Verify examples show correct preservation of functions
- **Test Complex Formulas**: Test with your actual Excel formulas

#### Configuration Not Saving
- **Check Permissions**: Ensure write access to prompt_configs directory
- **Verify JSON Format**: Export and check for formatting errors
- **Restart Application**: Sometimes requires a restart to take effect

### Getting Help

1. **Use the Test Feature**: Always test before saving
2. **Check Default Presets**: See how they're structured
3. **Export and Review**: Export your configuration to review the JSON structure
4. **Start Simple**: Begin with basic configurations and add complexity gradually

## 📈 Advanced Usage

### Custom Workflows

1. **Department-Specific Configurations**
   - Create configurations for different departments
   - Finance, Legal, HR, Technical teams can have tailored prompts

2. **Client-Specific Configurations**
   - Different clients may require different terminology
   - Create client-specific presets for consistency

3. **Language-Specific Tuning**
   - Some configurations may work better for specific target languages
   - Create language-pair specific configurations if needed

### Integration with Existing Workflows

1. **Backup Integration**
   - Export configurations before major updates
   - Include configuration exports in project deliverables

2. **Team Collaboration**
   - Share proven configurations across team members
   - Establish configuration standards for projects

3. **Quality Control**
   - Create "test" configurations for experimentation
   - Use "production" configurations for actual work
   - Regular reviews and updates of active configurations

---

## 📞 Support

For additional support or questions about the configuration system:

1. **Test Feature**: Use the built-in testing to troubleshoot
2. **Default Presets**: Reference the included presets for examples
3. **Documentation**: Refer to this guide for detailed instructions
4. **Export/Import**: Use export feature to backup and share configurations

The configuration system is designed to be flexible and powerful while remaining user-friendly. Start with the default presets and customize them to match your specific translation needs!