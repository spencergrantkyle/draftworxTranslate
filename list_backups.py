#!/usr/bin/env python3
"""
Backup File Lister for Draftworx Translation
Lists available backup files and helps users choose which one to resume from
"""

import os
import glob
import pandas as pd
from datetime import datetime

def list_backup_files():
    """List all available backup files with statistics"""
    
    backup_dir = "Backup_OutputResults"
    
    if not os.path.exists(backup_dir):
        print(f"Backup directory '{backup_dir}' not found.")
        print("No backup files available.")
        return
    
    # Find all backup files
    backup_files = glob.glob(f"{backup_dir}/backup_*.csv")
    final_files = glob.glob(f"{backup_dir}/final_backup_*.csv")
    
    all_files = backup_files + final_files
    
    if not all_files:
        print(f"No backup files found in '{backup_dir}'.")
        return
    
    print("=" * 80)
    print("AVAILABLE BACKUP FILES")
    print("=" * 80)
    print(f"{'File':<50} {'Records':<10} {'Values':<10} {'Formulas':<10} {'Type':<10}")
    print("-" * 80)
    
    file_stats = []
    
    for file_path in sorted(all_files):
        try:
            # Get file info
            filename = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            
            # Load and analyze the file
            df = pd.read_csv(file_path, encoding='utf-8')
            total_records = len(df)
            translated_values = df['CellValue_Afrikaans'].notna().sum() if 'CellValue_Afrikaans' in df.columns else 0
            translated_formulas = df['CellFormula_Afrikaans'].notna().sum() if 'CellFormula_Afrikaans' in df.columns else 0
            
            # Determine file type
            if 'final_backup' in filename:
                file_type = "FINAL"
            else:
                file_type = "PROGRESS"
            
            # Calculate progress percentage
            if total_records > 0:
                progress_pct = (translated_values / total_records) * 100
            else:
                progress_pct = 0
            
            print(f"{filename:<50} {total_records:<10} {translated_values:<10} {translated_formulas:<10} {file_type:<10}")
            
            file_stats.append({
                'path': file_path,
                'filename': filename,
                'total_records': total_records,
                'translated_values': translated_values,
                'translated_formulas': translated_formulas,
                'progress_pct': progress_pct,
                'mod_time': mod_time,
                'file_size': file_size,
                'type': file_type
            })
            
        except Exception as e:
            print(f"{filename:<50} {'ERROR':<10} {'ERROR':<10} {'ERROR':<10} {'ERROR':<10}")
            print(f"  Error reading file: {e}")
    
    print("-" * 80)
    
    # Show summary
    if file_stats:
        print("\nSUMMARY:")
        print(f"Total backup files: {len(file_stats)}")
        
        # Find the most recent file
        most_recent = max(file_stats, key=lambda x: x['mod_time'])
        print(f"Most recent backup: {most_recent['filename']}")
        print(f"  Modified: {most_recent['mod_time'].strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  Progress: {most_recent['translated_values']}/{most_recent['total_records']} values ({most_recent['progress_pct']:.1f}%)")
        
        # Find the file with most progress
        most_progress = max(file_stats, key=lambda x: x['translated_values'])
        if most_progress != most_recent:
            print(f"Most progress: {most_progress['filename']}")
            print(f"  Progress: {most_progress['translated_values']}/{most_progress['total_records']} values ({most_progress['progress_pct']:.1f}%)")
        
        # Show resume command
        print(f"\nTo resume from the most recent backup, run:")
        print(f"python translate.py --resume-from \"{most_recent['path']}\"")
        
        # Show all resume commands
        print(f"\nAll resume commands:")
        for stat in file_stats:
            print(f"python translate.py --resume-from \"{stat['path']}\"  # {stat['filename']}")

def show_file_details(file_path):
    """Show detailed information about a specific backup file"""
    
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
        
        print("=" * 80)
        print(f"BACKUP FILE DETAILS: {os.path.basename(file_path)}")
        print("=" * 80)
        
        # Basic file info
        file_size = os.path.getsize(file_path)
        mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
        
        print(f"File path: {file_path}")
        print(f"File size: {file_size:,} bytes")
        print(f"Modified: {mod_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Total records: {len(df)}")
        
        # Column analysis
        print(f"\nColumns: {list(df.columns)}")
        
        # Translation progress
        if 'CellValue_Afrikaans' in df.columns:
            translated_values = df['CellValue_Afrikaans'].notna().sum()
            empty_values = df['CellValue_Afrikaans'].isna().sum()
            print(f"\nValue Translation Progress:")
            print(f"  Translated: {translated_values}")
            print(f"  Empty: {empty_values}")
            print(f"  Progress: {translated_values/len(df)*100:.1f}%")
        
        if 'CellFormula_Afrikaans' in df.columns:
            translated_formulas = df['CellFormula_Afrikaans'].notna().sum()
            empty_formulas = df['CellFormula_Afrikaans'].isna().sum()
            print(f"\nFormula Translation Progress:")
            print(f"  Translated: {translated_formulas}")
            print(f"  Empty: {empty_formulas}")
            print(f"  Progress: {translated_formulas/len(df)*100:.1f}%")
        
        # Sample data
        print(f"\nSample data (first 5 records):")
        print(df.head().to_string())
        
    except Exception as e:
        print(f"Error reading file: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Show details for specific file
        file_path = sys.argv[1]
        show_file_details(file_path)
    else:
        # List all backup files
        list_backup_files() 