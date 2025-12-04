"""
Helper utility functions for the Mechanic Diagnostic Assistant.
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the given name."""
    return logging.getLogger(name)


def load_json_file(file_path: Path) -> Any:
    """
    Load data from a JSON file.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        Parsed JSON data
        
    Raises:
        FileNotFoundError: If file doesn't exist
        json.JSONDecodeError: If file contains invalid JSON
    """
    logger = get_logger(__name__)
    
    if not file_path.exists():
        logger.error(f"File not found: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.info(f"Successfully loaded JSON from {file_path}")
        return data
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in {file_path}: {e}")
        raise


def load_text_file(file_path: Path) -> str:
    """
    Load content from a text file.
    
    Args:
        file_path: Path to the text file
        
    Returns:
        File content as string
        
    Raises:
        FileNotFoundError: If file doesn't exist
    """
    logger = get_logger(__name__)
    
    if not file_path.exists():
        logger.error(f"File not found: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        logger.info(f"Successfully loaded text from {file_path}")
        return content
    except Exception as e:
        logger.error(f"Error reading {file_path}: {e}")
        raise


def format_currency(amount: float) -> str:
    """
    Format a number as currency (USD).
    
    Args:
        amount: Amount to format
        
    Returns:
        Formatted currency string
    """
    return f"${amount:,.2f}"


def format_error_message(error: Exception) -> str:
    """
    Format an exception as a user-friendly error message.
    
    Args:
        error: Exception to format
        
    Returns:
        Formatted error message
    """
    return f"Error: {type(error).__name__} - {str(error)}"


def pretty_print_json(data: Any, indent: int = 2) -> str:
    """
    Convert data to pretty-printed JSON string.
    
    Args:
        data: Data to convert
        indent: Indentation spaces
        
    Returns:
        Pretty-printed JSON string
    """
    return json.dumps(data, indent=indent, ensure_ascii=False)


def search_dict_list(
    data: List[Dict],
    key: str,
    value: Any,
    case_sensitive: bool = False
) -> Optional[Dict]:
    """
    Search for an item in a list of dictionaries by key-value pair.
    
    Args:
        data: List of dictionaries to search
        key: Key to search for
        value: Value to match
        case_sensitive: Whether to do case-sensitive string comparison
        
    Returns:
        First matching dictionary or None if not found
    """
    for item in data:
        if key not in item:
            continue
            
        item_value = item[key]
        
        # Handle string comparison
        if isinstance(value, str) and isinstance(item_value, str):
            if case_sensitive:
                if item_value == value:
                    return item
            else:
                if item_value.lower() == value.lower():
                    return item
        else:
            # Non-string comparison
            if item_value == value:
                return item
    
    return None


def filter_dict_list(
    data: List[Dict],
    key: str,
    value: Any,
    case_sensitive: bool = False
) -> List[Dict]:
    """
    Filter a list of dictionaries by key-value pair.
    
    Args:
        data: List of dictionaries to filter
        key: Key to filter by
        value: Value to match
        case_sensitive: Whether to do case-sensitive string comparison
        
    Returns:
        List of matching dictionaries
    """
    results = []
    
    for item in data:
        if key not in item:
            continue
            
        item_value = item[key]
        
        # Handle string comparison
        if isinstance(value, str) and isinstance(item_value, str):
            if case_sensitive:
                if item_value == value:
                    results.append(item)
            else:
                if item_value.lower() == value.lower():
                    results.append(item)
        else:
            # Non-string comparison
            if item_value == value:
                results.append(item)
    
    return results


def contains_substring(text: str, substring: str, case_sensitive: bool = False) -> bool:
    """
    Check if text contains substring.
    
    Args:
        text: Text to search in
        substring: Substring to search for
        case_sensitive: Whether to do case-sensitive comparison
        
    Returns:
        True if substring found, False otherwise
    """
    if not case_sensitive:
        text = text.lower()
        substring = substring.lower()
    
    return substring in text


def calculate_total_with_tax(subtotal: float, tax_percent: float) -> float:
    """
    Calculate total amount including tax.
    
    Args:
        subtotal: Amount before tax
        tax_percent: Tax percentage (e.g., 7.5 for 7.5%)
        
    Returns:
        Total amount including tax
    """
    tax_amount = subtotal * (tax_percent / 100)
    return subtotal + tax_amount


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate text to maximum length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix
