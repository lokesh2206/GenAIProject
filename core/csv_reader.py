"""
CSV Reader Module - Handles CSV file reading and schema extraction
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
import io

class CSVReader:
    """Read and analyze CSV files"""
    
    def __init__(self):
        self.df: Optional[pd.DataFrame] = None
        self.schema: Dict[str, Any] = {}
        self.metadata: Dict[str, Any] = {}
    
    def read_csv(self, file_content: bytes, filename: str) -> pd.DataFrame:
        """
        Read CSV file from bytes
        
        Args:
            file_content: CSV file content as bytes
            filename: Name of the file
            
        Returns:
            pandas DataFrame
        """
        try:
            # Try different encodings
            encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
            
            for encoding in encodings:
                try:
                    self.df = pd.read_csv(io.BytesIO(file_content), encoding=encoding)
                    break
                except UnicodeDecodeError:
                    continue
            
            if self.df is None:
                raise ValueError("Unable to decode CSV file with supported encodings")
            
            # Extract schema and metadata
            self._extract_schema()
            self._extract_metadata(filename)
            
            return self.df
            
        except Exception as e:
            raise Exception(f"Error reading CSV file: {str(e)}")
    
    def _extract_schema(self):
        """Extract schema information from DataFrame"""
        if self.df is None:
            return
        
        schema_info = []
        
        for col in self.df.columns:
            col_info = {
                'column_name': col,
                'data_type': str(self.df[col].dtype),
                'non_null_count': int(self.df[col].count()),
                'null_count': int(self.df[col].isnull().sum()),
                'unique_count': int(self.df[col].nunique()),
                'sample_values': self._get_sample_values(col),
                'inferred_type': self._infer_column_type(col)
            }
            
            # Add numeric statistics if applicable
            if pd.api.types.is_numeric_dtype(self.df[col]):
                col_info.update({
                    'min': float(self.df[col].min()) if not pd.isna(self.df[col].min()) else None,
                    'max': float(self.df[col].max()) if not pd.isna(self.df[col].max()) else None,
                    'mean': float(self.df[col].mean()) if not pd.isna(self.df[col].mean()) else None,
                    'median': float(self.df[col].median()) if not pd.isna(self.df[col].median()) else None
                })
            
            schema_info.append(col_info)
        
        self.schema = {
            'columns': schema_info,
            'total_columns': len(self.df.columns),
            'column_names': list(self.df.columns)
        }
    
    def _extract_metadata(self, filename: str):
        """Extract metadata from DataFrame"""
        if self.df is None:
            return
        
        self.metadata = {
            'filename': filename,
            'total_rows': len(self.df),
            'total_columns': len(self.df.columns),
            'memory_usage_mb': self.df.memory_usage(deep=True).sum() / (1024 * 1024),
            'has_duplicates': self.df.duplicated().any(),
            'duplicate_count': int(self.df.duplicated().sum())
        }
    
    def _get_sample_values(self, column: str, n: int = 5) -> List[Any]:
        """Get sample values from a column"""
        if self.df is None:
            return []
        
        # Get non-null unique values
        unique_vals = self.df[column].dropna().unique()
        sample = unique_vals[:n].tolist()
        
        # Convert numpy types to Python types
        return [self._convert_to_python_type(val) for val in sample]
    
    def _convert_to_python_type(self, val: Any) -> Any:
        """Convert numpy types to Python types"""
        if isinstance(val, (np.integer, np.floating)):
            return val.item()
        elif isinstance(val, np.bool_):
            return bool(val)
        elif pd.isna(val):
            return None
        return val
    
    def _infer_column_type(self, column: str) -> str:
        """Infer semantic type of column"""
        if self.df is None:
            return "unknown"
        
        col_data = self.df[column]
        
        # Check if numeric
        if pd.api.types.is_numeric_dtype(col_data):
            if pd.api.types.is_integer_dtype(col_data):
                return "integer"
            return "float"
        
        # Check if datetime
        if pd.api.types.is_datetime64_any_dtype(col_data):
            return "datetime"
        
        # Check if boolean
        if pd.api.types.is_bool_dtype(col_data):
            return "boolean"
        
        # Check if categorical (low cardinality)
        if col_data.nunique() / len(col_data) < 0.05:
            return "categorical"
        
        # Default to string
        return "string"
    
    def get_schema_text(self) -> str:
        """Get schema as formatted text for LLM context"""
        if not self.schema:
            return ""
        
        text_parts = [
            f"Dataset Schema ({self.metadata.get('filename', 'Unknown')}):",
            f"Total Rows: {self.metadata.get('total_rows', 0)}",
            f"Total Columns: {self.schema.get('total_columns', 0)}",
            "\nColumn Details:"
        ]
        
        for col in self.schema.get('columns', []):
            col_text = f"\n- {col['column_name']} ({col['inferred_type']})"
            col_text += f"\n  Data Type: {col['data_type']}"
            col_text += f"\n  Non-Null: {col['non_null_count']}, Null: {col['null_count']}"
            col_text += f"\n  Unique Values: {col['unique_count']}"
            
            if col.get('sample_values'):
                col_text += f"\n  Sample Values: {col['sample_values']}"
            
            if 'min' in col:
                col_text += f"\n  Range: {col['min']} to {col['max']}"
                col_text += f"\n  Mean: {col['mean']:.2f}, Median: {col['median']:.2f}"
            
            text_parts.append(col_text)
        
        return "\n".join(text_parts)
    
    def get_dataframe(self) -> Optional[pd.DataFrame]:
        """Get the loaded DataFrame"""
        return self.df
    
    def get_schema(self) -> Dict[str, Any]:
        """Get schema dictionary"""
        return self.schema
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get metadata dictionary"""
        return self.metadata
