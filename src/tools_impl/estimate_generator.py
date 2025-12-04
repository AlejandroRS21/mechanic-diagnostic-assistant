"""
Tool 5: Generate a formatted customer estimate/quote.
"""

from typing import Dict
from datetime import datetime
from src.utils.helpers import get_logger, format_currency
from src.utils.config import LABOR_RATES_PATH

logger = get_logger(__name__)


def generate_estimate(
    diagnosis: str,
    solution: Dict,
    vehicle_info: Dict = None,
    customer_name: str = "Customer"
) -> Dict:
    """
    Generate a formatted repair estimate for the customer.
    
    Args:
        diagnosis: Description of the diagnosed problem
        solution: Dictionary with keys 'parts' (list), 'labor_hours' (float), 'total_cost' (float)
        vehicle_info: Optional dict with 'brand', 'model', 'year'
        customer_name: Optional customer name
        
    Returns:
        Dictionary with formatted estimate and metadata
    """
    logger.info(f"Generating estimate for: {diagnosis}")
    
    try:
        # Extract data from solution
        parts = solution.get("parts", [])
        labor_hours = solution.get("labor_hours", 0)
        total_cost = solution.get("total_cost", solution.get("grand_total", 0))
        parts_cost = solution.get("parts_cost", 0)
        labor_cost = solution.get("labor_cost", 0)
        
        # Format vehicle info
        if vehicle_info:
            vehicle_str = f"{vehicle_info.get('brand', '')} {vehicle_info.get('model', '')} {vehicle_info.get('year', '')}".strip()
        else:
            vehicle_str = "Vehicle"
        
        # Generate estimate number
        estimate_number = f"EST-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        # Build formatted estimate text
        estimate_text = f"""
{'='*60}
                    REPAIR ESTIMATE
{'='*60}

Estimate #: {estimate_number}
Date: {datetime.now().strftime('%B %d, %Y')}
Customer: {customer_name}
Vehicle: {vehicle_str}

{'='*60}
DIAGNOSIS
{'='*60}
{diagnosis}

{'='*60}
RECOMMENDED REPAIR
{'='*60}
"""
        
        # Add parts list
        if parts:
            estimate_text += "\nParts Required:\n"
            for i, part in enumerate(parts, 1):
                if isinstance(part, dict):
                    part_name = part.get('name', 'Unknown Part')
                    part_price = part.get('price', 0)
                    part_type = part.get('type', '')
                    estimate_text += f"  {i}. {part_name} - {format_currency(part_price)} ({part_type})\n"
                else:
                    estimate_text += f"  {i}. {part}\n"
        
        # Add labor info
        estimate_text += f"\nLabor:\n  Estimated time: {labor_hours} hours\n"
        
        # Add cost breakdown
        estimate_text += f"""
{'='*60}
COST BREAKDOWN
{'='*60}
Parts Cost:          {format_currency(parts_cost)}
Labor Cost:          {format_currency(labor_cost)}
"""
        
        # Add additional fees if present
        if 'shop_supplies_fee' in solution:
            estimate_text += f"Shop Supplies:       {format_currency(solution['shop_supplies_fee'])}\n"
        if 'hazmat_fee' in solution:
            estimate_text += f"Hazmat Fee:          {format_currency(solution['hazmat_fee'])}\n"
        if 'tax_amount' in solution:
            estimate_text += f"Tax:                 {format_currency(solution['tax_amount'])}\n"
        
        estimate_text += f"""
{'='*60}
TOTAL ESTIMATE:      {format_currency(total_cost)}
{'='*60}

IMPORTANT NOTES:
- This is an estimate only. Final cost may vary based on actual
  condition and any additional issues discovered during repair.
- Estimate valid for 30 days from date issued.
- All parts come with manufacturer warranty.
- We reserve the right to refuse service.

Please contact us to schedule your repair or if you have any
questions about this estimate.

Thank you for your business!
{'='*60}
"""
        
        result = {
            "estimate_number": estimate_number,
            "date": datetime.now().isoformat(),
            "customer_name": customer_name,
            "vehicle": vehicle_str,
            "diagnosis": diagnosis,
            "parts_count": len(parts),
            "labor_hours": labor_hours,
            "estimated_cost": total_cost,
            "formatted_cost": format_currency(total_cost),
            "estimated_time": f"{int(labor_hours)}-{int(labor_hours)+1} hours" if labor_hours < 4 else f"{int(labor_hours//4)}-{int(labor_hours//4)+1} days",
            "formatted_estimate": estimate_text.strip()
        }
        
        logger.info(f"Estimate generated: {estimate_number} - {format_currency(total_cost)}")
        return result
    
    except Exception as e:
        logger.error(f"Error generating estimate: {e}")
        return {
            "error": str(e),
            "formatted_estimate": "Error generating estimate. Please try again."
        }


if __name__ == "__main__":
    # Test the tool
    print("Testing estimate generator tool...")
    print("-" * 50)
    
    # Mock solution data
    solution_data = {
        "parts": [
            {"name": "Catalytic Converter - OEM", "price": 650.00, "type": "OEM"},
            {"name": "Oxygen Sensor - Upstream", "price": 85.00, "type": "Aftermarket"}
        ],
        "labor_hours": 2.5,
        "parts_cost": 735.00,
        "labor_cost": 212.50,
        "shop_supplies_fee": 47.38,
        "hazmat_fee": 5.00,
        "tax_amount": 75.00,
        "grand_total": 1074.88
    }
    
    vehicle_info = {
        "brand": "Toyota",
        "model": "Corolla",
        "year": "2018"
    }
    
    result = generate_estimate(
        diagnosis="Diagnostic code P0420 detected. Catalytic converter efficiency below threshold. "
                  "Likely cause is deteriorated catalytic converter. Oxygen sensors tested and upstream "
                  "sensor also showing signs of failure.",
        solution=solution_data,
        vehicle_info=vehicle_info,
        customer_name="John Smith"
    )
    
    print("\n" + result['formatted_estimate'])
    
    print(f"\n✅ Estimate #{result['estimate_number']} generated successfully")
