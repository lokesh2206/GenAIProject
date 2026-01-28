"""
Utility helper functions
"""
import logging
from typing import Any
import json

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

def format_bytes(size: int) -> str:
    """
    Format bytes to human readable format
    
    Args:
        size: Size in bytes
        
    Returns:
        Formatted string
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} TB"

def safe_json_dumps(obj: Any) -> str:
    """
    Safely convert object to JSON string
    
    Args:
        obj: Object to convert
        
    Returns:
        JSON string
    """
    try:
        return json.dumps(obj, indent=2, default=str)
    except Exception as e:
        return str(obj)

def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Truncate text to maximum length
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."
