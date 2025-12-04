"""
Tool 1: Search for OBD-II diagnostic code information.
"""

from typing import Dict, Optional
from src.utils.helpers import get_logger, load_json_file, search_dict_list
from src.utils.config import OBD_CODES_PATH

logger = get_logger(__name__)


def search_diagnostic_code(code: str) -> Dict:
    """
    Search for information about an OBD-II diagnostic code.
    
    Args:
        code: OBD-II code (e.g., "P0420", "P0300")
        
    Returns:
        Dictionary with code information including description, causes, and repair cost
    """
    logger.info(f"Searching for diagnostic code: {code}")
    
    # Normalize code (uppercase, remove spaces)
    code = code.upper().strip()
    
    try:
        # Load OBD codes database
        obd_data = load_json_file(OBD_CODES_PATH)
        
        # Search for the code
        result = search_dict_list(obd_data, "code", code, case_sensitive=False)
        
        if result:
            logger.info(f"Found code {code}")
            return {
                "found": True,
                "code": result["code"],
                "description": result["description"],
                "system": result["system"],
                "severity": result["severity"],
                "common_causes": result["common_causes"],
                "typical_repair_cost_min": result["typical_repair_cost_min"],
                "typical_repair_cost_max": result["typical_repair_cost_max"],
                "repair_time_hours_min": result["repair_time_hours_min"],
                "repair_time_hours_max": result["repair_time_hours_max"],
                "diagnostic_steps": result.get("diagnostic_steps", [])
            }
        else:
            logger.warning(f"Code {code} not found in database")
            return {
                "found": False,
                "code": code,
                "message": f"Diagnostic code {code} not found in database. "
                          "This may be a manufacturer-specific code or a typo. "
                          "Please verify the code and try again."
            }
    
    except Exception as e:
        logger.error(f"Error searching for code {code}: {e}")
        return {
            "found": False,
            "code": code,
            "error": str(e)
        }


if __name__ == "__main__":
    # Test the tool
    print("Testing diagnostic code search tool...")
    print("-" * 50)
    
    # Test successful search
    result1 = search_diagnostic_code("P0420")
    print("\nTest 1: P0420")
    print(f"Found: {result1['found']}")
    if result1['found']:
        print(f"Description: {result1['description']}")
        print(f"Common causes: {len(result1['common_causes'])} listed")
    
    # Test code not found

    result2 = search_diagnostic_code("P9999")
    print("\nTest 2: P9999 (should not exist)")
    print(f"Found: {result2['found']}")
    print(f"Message: {result2.get('message', 'N/A')}")
    
    print("\n✅ Diagnostic code tool test completed")
