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
    Input format: JSON string with 'parts' (list) and 'labor_hours' (float)
    Example: '{"parts": ["CAT-001"], "labor_hours": 2.5}'
    """
    try:
        data = json.loads(input_str)
        parts = data.get('parts', [])
        labor_hours = float(data.get('labor_hours', 0))
        result = calculate_repair_cost(parts, labor_hours)
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Invalid input format: {str(e)}"})


def find_parts_wrapper(input_str: str) -> str:
    """
    Wrapper for parts finder.
    Input format: JSON string with 'vehicle' (dict) and 'part_name' (str)
    Example: '{"vehicle": {"brand": "Toyota", "model": "Corolla", "year": "2018"}, "part_name": "catalytic converter"}'
    """
    try:
        data = json.loads(input_str)
        vehicle = data.get('vehicle', {})
        part_name = data.get('part_name', '')
        result = find_replacement_parts(vehicle, part_name)
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Invalid input format: {str(e)}"})


def query_issues_wrapper(input_str: str) -> str:
    """
    Wrapper for known issues query.
    Input format: JSON string with 'brand', 'model', optional 'year'
    Example: '{"brand": "Toyota", "model": "Corolla", "year": 2018}'
    """
    try:
        data = json.loads(input_str)
        brand = data.get('brand', '')
        model = data.get('model', '')
        year = data.get('year')
        result = query_known_issues(brand, model, year)
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Invalid input format: {str(e)}"})


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
    
    Input: JSON string with:
    - "parts": List of part IDs or names (e.g., ["CAT-001", "BRK-001"])
    - "labor_hours": Estimated labor time as a number (e.g., 2.5)
    
    Example: '{"parts": ["CAT-001"], "labor_hours": 2.5}'
    
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
    
    Input: JSON string with:
    - "vehicle": Dict with "brand", "model", "year" (e.g., {"brand": "Toyota", "model": "Corolla", "year": "2018"})
    - "part_name": Name or category of part (e.g., "catalytic converter", "brake pads")
    
    Example: '{"vehicle": {"brand": "Toyota", "model": "Corolla", "year": "2018"}, "part_name": "catalytic converter"}'
    
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
    
    Input: JSON string with:
    - "brand": Vehicle brand (e.g., "Toyota")
    - "model": Vehicle model (e.g., "Corolla")
    - "year": Optional year (e.g., 2018)
    
    Example: '{"brand": "Toyota", "model": "Corolla", "year": 2018}'
    
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
