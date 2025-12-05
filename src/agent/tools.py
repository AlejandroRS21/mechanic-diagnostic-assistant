"""
LangChain tools integration - wraps the 5 diagnostic tools for agent use.
"""

import json
from langchain.tools import Tool
from typing import List

from src.tools_impl.diagnostic_codes import search_diagnostic_code
from src.tools_impl.cost_calculator import calculate_repair_cost
from src.tools_impl.parts_finder import find_replacement_parts
from src.tools_impl.known_issues import query_known_issues
from src.tools_impl.estimate_generator import generate_estimate
from src.utils.helpers import get_logger

logger = get_logger(__name__)


# Wrapper functions that return strings (required by LangChain Tool)

def search_code_wrapper(code: str) -> str:
    """Wrapper for diagnostic code search."""
    result = search_diagnostic_code(code)
    return json.dumps(result, indent=2)


def calculate_cost_wrapper(input_str: str) -> str:
    """
    Wrapper for cost calculator.
    Input format: "parts: PART1, PART2, ... labor: HOURS"
    Example: "parts: CAT-001, O2-SENSOR labor: 2.5"
    """
    try:
        input_str = input_str.strip()
        
        # Try to parse simple format
        parts_list = []
        labor_hours = 0
        
        if "parts:" in input_str.lower() and "labor:" in input_str.lower():
            parts_section = input_str.lower().split("labor:")[0].replace("parts:", "").strip()
            labor_section = input_str.lower().split("labor:")[1].strip()
            
            parts_list = [p.strip() for p in parts_section.split(",") if p.strip()]
            try:
                labor_hours = float(labor_section.split()[0])
            except ValueError:
                pass
        else:
            # Try JSON fallback
            input_str_clean = input_str.strip().strip('"\'')
            data = json.loads(input_str_clean)
            parts_list = data.get('parts', [])
            labor_hours = float(data.get('labor_hours', 0))
        
        result = calculate_repair_cost(parts_list, labor_hours)
        return json.dumps(result, indent=2)
    except json.JSONDecodeError:
        return json.dumps({
            "error": "Invalid format. Use: 'parts: PART1, PART2 labor: HOURS'",
            "example": "parts: CAT-001, O2-SENSOR labor: 2.5",
            "input_received": input_str
        })
    except Exception as e:
        logger.error(f"Error in calculate_cost_wrapper: {e}")
        return json.dumps({"error": f"Error: {str(e)}"})


def find_parts_wrapper(input_str: str) -> str:
    """
    Wrapper for parts finder.
    Input format: "PART_NAME for BRAND MODEL YEAR"
    Example: "catalytic converter for Toyota Camry 2019"
    """
    try:
        # Parse the input
        input_str = input_str.strip()
        
        # Try to extract "for" pattern
        if " for " in input_str:
            part_name, vehicle_str = input_str.split(" for ", 1)
            part_name = part_name.strip()
            
            # Parse vehicle info
            parts = vehicle_str.strip().split()
            brand = parts[0] if len(parts) > 0 else ""
            model = parts[1] if len(parts) > 1 else ""
            year = None
            try:
                year = int(parts[2]) if len(parts) > 2 else None
            except ValueError:
                pass
            
            vehicle = {"brand": brand, "model": model}
            if year:
                vehicle["year"] = str(year)
        else:
            # Try JSON format as fallback
            input_str_clean = input_str.strip().strip('"\'')
            data = json.loads(input_str_clean)
            vehicle = data.get('vehicle', {})
            part_name = data.get('part_name', '')
        
        if not part_name or not vehicle.get('brand') or not vehicle.get('model'):
            return json.dumps({
                "error": "Invalid format. Use: 'PART_NAME for BRAND MODEL YEAR'",
                "example": "catalytic converter for Toyota Camry 2019",
                "input_received": input_str
            })
        
        result = find_replacement_parts(vehicle, part_name)
        return json.dumps(result, indent=2)
    except json.JSONDecodeError:
        # Failed JSON fallback
        return json.dumps({
            "error": "Invalid format. Use: 'PART_NAME for BRAND MODEL YEAR'",
            "example": "catalytic converter for Toyota Camry 2019",
            "input_received": input_str
        })
    except Exception as e:
        logger.error(f"Error in find_parts_wrapper: {e}")
        return json.dumps({"error": f"Error: {str(e)}"})


def query_issues_wrapper(vehicle_info: str) -> str:
    """
    Wrapper for known issues query.
    Input format: Space-separated "brand model year"
    Example: 'Toyota Camry 2019' or 'Honda Civic'
    """
    try:
        parts = vehicle_info.strip().split()
        brand = parts[0] if len(parts) > 0 else ""
        model = parts[1] if len(parts) > 1 else ""
        year = None
        try:
            year = int(parts[2]) if len(parts) > 2 else None
        except ValueError:
            pass
        
        if not brand or not model:
            return json.dumps({
                "error": "Invalid format. Use: 'Brand Model Year' (e.g., 'Toyota Camry 2019')",
                "input_received": vehicle_info
            })
        
        result = query_known_issues(brand, model, year)
        return json.dumps(result, indent=2)
    except Exception as e:
        logger.error(f"Error in query_issues_wrapper: {e}")
        return json.dumps({"error": f"Error: {str(e)}"})


def generate_estimate_wrapper(input_str: str) -> str:
    """
    Wrapper for estimate generator.
    Input format: JSON string with 'diagnosis', 'solution' (dict), optional 'vehicle_info', 'customer_name'
    """
    try:
        data = json.loads(input_str)
        diagnosis = data.get('diagnosis', '')
        solution = data.get('solution', {})
        vehicle_info = data.get('vehicle_info')
        customer_name = data.get('customer_name', 'Customer')
        result = generate_estimate(diagnosis, solution, vehicle_info, customer_name)
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Invalid input format: {str(e)}"})


# Define LangChain Tools

diagnostic_code_tool = Tool(
    name="search_diagnostic_code",
    description="""
    Search for information about an OBD-II diagnostic trouble code (DTC).
    
    Input: A diagnostic code as a string (e.g., "P0420", "P0300")
    
    Returns: Detailed information including:
    - Code description
    - System affected
    - Severity level
    - Common causes
    - Typical repair cost range
    - Diagnostic steps
    
    Use this tool when the mechanic mentions a specific OBD-II code or when you need
    to look up what a code means.
    """,
    func=search_code_wrapper
)

cost_calculator_tool = Tool(
    name="calculate_repair_cost",
    description="""
    Calculate the total cost of a repair including parts, labor, and fees.
    
    Input: "parts: PART1, PART2, PART3 labor: HOURS"
    - PART1, PART2, etc: Part IDs or names (e.g., CAT-001, BRK-001)
    - HOURS: Estimated labor time in hours (e.g., 2.5, 3)
    
    Examples:
    - "parts: CAT-001 labor: 2.5"
    - "parts: CAT-001, O2-SENSOR, BRK-001 labor: 3"
    
    Returns: Detailed cost breakdown including:
    - Parts cost with details
    - Labor cost
    - Shop fees and taxes
    - Grand total
    
    Use this tool to calculate repair costs when you know what parts are needed
    and how long the repair will take.
    """,
    func=calculate_cost_wrapper
)

parts_finder_tool = Tool(
    name="find_replacement_parts",
    description="""
    Find replacement parts compatible with a specific vehicle.
    
    Input: "PART_NAME for BRAND MODEL YEAR"
    - PART_NAME: Name or category of part (e.g., catalytic converter, brake pads, alternator)
    - BRAND: Vehicle brand (e.g., Toyota, Honda)
    - MODEL: Vehicle model (e.g., Camry, Civic)
    - YEAR: Optional year (e.g., 2019)
    
    Examples:
    - "catalytic converter for Toyota Camry 2019"
    - "brake pads for Honda Civic 2018"
    - "alternator for Ford Focus" (without year)
    
    Returns: List of compatible parts with:
    - Part names and IDs
    - Prices (both OEM and aftermarket options)
    - Warranty information
    
    Use this tool when you need to find what parts are available and their prices
    for a specific vehicle.
    """,
    func=find_parts_wrapper
)

known_issues_tool = Tool(
    name="query_known_issues",
    description="""
    Query database of common/known issues for specific vehicle makes and models.
    
    Input: Space-separated format "BRAND MODEL YEAR"
    - BRAND: Vehicle brand (e.g., Toyota, Honda, Ford)
    - MODEL: Vehicle model (e.g., Corolla, Civic, Focus)
    - YEAR: Optional year (e.g., 2018, 2019, 2020)
    
    Examples:
    - "Toyota Camry 2019"
    - "Honda Civic 2018"
    - "Ford Focus" (without year)
    
    Returns: List of known common issues including:
    - Issue description
    - Frequency (how common it is)
    - Typical symptoms
    - Additional notes
    
    Use this tool when you want to check if there are known common problems
    for a particular vehicle that might explain the symptoms.
    """,
    func=query_issues_wrapper
)

estimate_generator_tool = Tool(
    name="generate_estimate",
    description="""
    Generate a formatted, professional repair estimate/quote for the customer.
    
    Input: JSON string with:
    - "diagnosis": Description of the problem (string)
    - "solution": Dict with repair details including parts list, labor_hours, and costs
    - "vehicle_info": Optional dict with vehicle details
    - "customer_name": Optional customer name (default: "Customer")
    
    Returns: Formatted estimate document with:
    - Estimate number and date
    - Diagnosis explanation
    - Parts and labor breakdown
    - Total cost
    - Professional formatting
    
    Use this tool as the FINAL step when you have completed the diagnosis
    and calculated costs, and you're ready to present a formal estimate to the mechanic
    to show their customer.
    """,
    func=generate_estimate_wrapper
)


# Export all tools as a list
def get_all_tools() -> List[Tool]:
    """Get all available diagnostic tools for the agent."""
    tools = [
        diagnostic_code_tool,
        cost_calculator_tool,
        parts_finder_tool,
        known_issues_tool,
        estimate_generator_tool
    ]
    
    logger.info(f"Loaded {len(tools)} tools for agent")
    return tools


if __name__ == "__main__":
    # Test tools
    print("Testing LangChain tools...")
    print("-" * 60)
    
    tools = get_all_tools()
    
    print(f"\n✅ {len(tools)} tools loaded:")
    for tool in tools:
        print(f"  - {tool.name}")
    
    # Test diagnostic code tool
    print("\nTest: search_diagnostic_code")
    result = diagnostic_code_tool.run("P0420")
    print(f"Result preview: {result[:150]}...")
    
    print("\n✅ Tools test completed")
