import pandas as pd
import os
from typing import Optional, Union, Dict, Any
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CSVReader:
    """
    A comprehensive CSV reader class using pandas to load CSV files into dataframes.
    """
    
    def __init__(self):
        """Initialize the CSV reader."""
        pass
    
    def read_csv(self, 
                 filepath: str, 
                 encoding: str = 'utf-8',
                 sep: str = ',',
                 header: Optional[Union[int, list]] = 0,
                 index_col: Optional[Union[int, str, list]] = None,
                 usecols: Optional[Union[list, callable]] = None,
                 skiprows: Optional[Union[int, list]] = None,
                 na_values: Optional[Union[str, list]] = None,
                 keep_default_na: bool = True,
                 dtype: Optional[Dict[str, Any]] = None,
                 **kwargs) -> pd.DataFrame:
        """
        Read a CSV file into a pandas DataFrame.
        
        Args:
            filepath (str): Path to the CSV file
            encoding (str): File encoding (default: 'utf-8')
            sep (str): Delimiter to use (default: ',')
            header (int, list, optional): Row number(s) to use as column names
            index_col (int, str, list, optional): Column(s) to use as index
            usecols (list, callable, optional): Columns to read
            skiprows (int, list, optional): Rows to skip
            na_values (str, list, optional): Values to treat as NaN
            keep_default_na (bool): Whether to keep default NaN values
            dtype (dict, optional): Data types for columns
            **kwargs: Additional pandas read_csv parameters
            
        Returns:
            pd.DataFrame: Loaded dataframe
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            ValueError: If there are issues with the file or parameters
        """
        try:
            # Validate filepath
            if not os.path.exists(filepath):
                raise FileNotFoundError(f"File not found: {filepath}")
            
            # Check if file is readable
            if not os.access(filepath, os.R_OK):
                raise PermissionError(f"Cannot read file: {filepath}")
            
            logger.info(f"Reading CSV file: {filepath}")
            
            # Read the CSV file
            df = pd.read_csv(
                filepath,
                encoding=encoding,
                sep=sep,
                header=header,
                index_col=index_col,
                usecols=usecols,
                skiprows=skiprows,
                na_values=na_values,
                keep_default_na=keep_default_na,
                dtype=dtype,
                **kwargs
            )
            
            logger.info(f"Successfully loaded CSV with shape: {df.shape}")
            return df
            
        except pd.errors.EmptyDataError:
            logger.error("The CSV file is empty")
            raise ValueError("The CSV file is empty")
        except pd.errors.ParserError as e:
            logger.error(f"Error parsing CSV file: {e}")
            raise ValueError(f"Error parsing CSV file: {e}")
        except Exception as e:
            logger.error(f"Unexpected error reading CSV: {e}")
            raise
    
    def read_csv_simple(self, filepath: str) -> pd.DataFrame:
        """
        Simple CSV reader with default settings.
        
        Args:
            filepath (str): Path to the CSV file
            
        Returns:
            pd.DataFrame: Loaded dataframe
        """
        return self.read_csv(filepath)
    
    def read_csv_with_info(self, filepath: str) -> tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Read CSV and return both dataframe and file information.
        
        Args:
            filepath (str): Path to the CSV file
            
        Returns:
            tuple: (DataFrame, file_info_dict)
        """
        df = self.read_csv(filepath)
        
        # Get file information
        file_info = {
            'filepath': filepath,
            'file_size': os.path.getsize(filepath),
            'shape': df.shape,
            'columns': list(df.columns),
            'dtypes': df.dtypes.to_dict(),
            'memory_usage': df.memory_usage(deep=True).sum(),
            'null_counts': df.isnull().sum().to_dict()
        }
        
        return df, file_info
    
    def preview_csv(self, filepath: str, n_rows: int = 5) -> pd.DataFrame:
        """
        Preview first n rows of a CSV file.
        
        Args:
            filepath (str): Path to the CSV file
            n_rows (int): Number of rows to preview
            
        Returns:
            pd.DataFrame: Preview dataframe
        """
        return self.read_csv(filepath, nrows=n_rows)
    
    def get_csv_info(self, filepath: str) -> Dict[str, Any]:
        """
        Get information about a CSV file without loading the full content.
        
        Args:
            filepath (str): Path to the CSV file
            
        Returns:
            dict: File information
        """
        try:
            # Read just the first few rows to get column info
            df_preview = self.read_csv(filepath, nrows=10)
            
            # Get file stats
            file_stats = os.stat(filepath)
            
            info = {
                'filepath': filepath,
                'file_size_bytes': file_stats.st_size,
                'file_size_mb': file_stats.st_size / (1024 * 1024),
                'last_modified': pd.Timestamp(file_stats.st_mtime, unit='s'),
                'columns': list(df_preview.columns),
                'column_count': len(df_preview.columns),
                'preview_shape': df_preview.shape,
                'sample_data': df_preview.head(3).to_dict('records')
            }
            
            return info
            
        except Exception as e:
            logger.error(f"Error getting CSV info: {e}")
            raise


# Example usage functions
def load_translation_csv(filepath: str = "LinkTranslations.csv") -> pd.DataFrame:
    """
    Load the translation CSV file with appropriate settings.
    
    Args:
        filepath (str): Path to the translation CSV file
        
    Returns:
        pd.DataFrame: Translation dataframe
    """
    reader = CSVReader()
    
    # For translation files, we might want to:
    # - Drop empty columns
    # - Set specific data types
    # - Handle encoding issues
    
    df = reader.read_csv(
        filepath,
        encoding='utf-8',
        na_values=['', 'nan', 'NaN', 'NULL', 'null'],
        keep_default_na=True
    )
    
    # Drop completely empty columns
    df = df.dropna(axis=1, how='all')
    
    # Drop completely empty rows
    df = df.dropna(how='all')
    
    return df


def main():
    """Example usage of the CSV reader."""
    reader = CSVReader()
    
    # Example 1: Simple read
    try:
        df = reader.read_csv_simple("LinkTranslations.csv")
        print(f"Loaded CSV with shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        print("\nFirst 5 rows:")
        print(df.head())
        
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 2: Get file info
    try:
        info = reader.get_csv_info("LinkTranslations.csv")
        print(f"\nFile info:")
        for key, value in info.items():
            print(f"  {key}: {value}")
            
    except Exception as e:
        print(f"Error getting info: {e}")
    
    # Example 3: Load translation file
    try:
        df_translations = load_translation_csv()
        print(f"\nTranslation file shape: {df_translations.shape}")
        print(f"Translation columns: {list(df_translations.columns)}")
        print("\nFirst 3 translation entries:")
        print(df_translations.head(3))
        
    except Exception as e:
        print(f"Error loading translations: {e}")


if __name__ == "__main__":
    main()
