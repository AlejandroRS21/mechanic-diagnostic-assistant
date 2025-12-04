"""
Tool 2: Calculate repair costs based on parts and labor.
"""

from typing import List, Dict
from src.utils.helpers import get_logger, load_json_file, format_currency, calculate_total_with_tax
from src.utils.config import PARTS_CATALOG_PATH, LABOR_RATES_PATH

logger = get_logger(__name__)


def calculate_repair_cost(parts: List[str], labor_hours: float) -> Dict:
    """
    Calculate the total repair cost including parts, labor, and fees.
    
    Args:
        parts: List of part identifiers or names (e.g., ["CAT-001", "BRK-001"])
        labor_hours: Estimated labor time in hours
        
    Returns:
        Dictionary with itemized costs and totals
    """
    logger.info(f"Calculating repair cost for {len(parts)} parts and {labor_hours} hours labor")
    
    try:
        # Load parts catalog and labor rates
        parts_catalog = load_json_file(PARTS_CATALOG_PATH)
        labor_rates = load_json_file(LABOR_RATES_PATH)
        
        hourly_rate = labor_rates["shop_hourly_rate"]
        shop_supplies_percent = labor_rates["surcharges"]["shop_supplies_percent"]
        hazmat_fee = labor_rates["surcharges"]["hazardous_waste_fee"]
        tax_percent = labor_rates["surcharges"]["tax_percent"]
        
        # Calculate parts cost
        parts_cost = 0.0
        parts_details = []
        parts_list = parts_catalog["parts"]
        
        for part_id in parts:
            # Try to find part by ID or name
            found_part = None
            for part in parts_list:
                if (part["id"].lower() == part_id.lower() or 
                    part_id.lower() in part["name"].lower()):
                    found_part = part
                    break
            
            if found_part:
                parts_cost += found_part["price"]
                parts_details.append({
                    "id": found_part["id"],
                    "name": found_part["name"],
                    "price": found_part["price"],
                    "type": found_part["type"]
                })
            else:
                logger.warning(f"Part not found: {part_id}")
                parts_details.append({
                    "id": part_id,
                    "name": "Unknown part",
                    "price": 0.0,
                    "type": "Not Found"
                })
        
        # Calculate labor cost
        labor_cost = labor_hours * hourly_rate
        
        # Calculate subtotal
        subtotal = parts_cost + labor_cost
        
        # Calculate shop supplies fee
        shop_supplies = subtotal * (shop_supplies_percent / 100)
        
        # Calculate total before tax
        total_before_tax = subtotal + shop_supplies + hazmat_fee
        
        # Calculate tax
        tax_amount = total_before_tax * (tax_percent / 100)
        
        # Calculate grand total
        grand_total = total_before_tax + tax_amount
        
        result = {
            "parts_details": parts_details,
            "parts_cost": round(parts_cost, 2),
            "labor_hours": labor_hours,
            "hourly_rate": hourly_rate,
            "labor_cost": round(labor_cost, 2),
            "subtotal": round(subtotal, 2),
            "shop_supplies_fee": round(shop_supplies, 2),
            "hazmat_fee": hazmat_fee,
            "total_before_tax": round(total_before_tax, 2),
            "tax_amount": round(tax_amount, 2),
            "tax_percent": tax_percent,
            "grand_total": round(grand_total, 2),
            "formatted_total": format_currency(grand_total)
        }
        
        logger.info(f"Repair cost calculated: {format_currency(grand_total)}")
        return result
    
    except Exception as e:
        logger.error(f"Error calculating repair cost: {e}")
        return {
            "error": str(e),
            "grand_total": 0.0
        }


if __name__ == "__main__":
    # Test the tool
    print("Testing repair cost calculator tool...")
    print("-" * 50)
    
    # Test case: Catalytic converter replacement
    result = calculate_repair_cost(
        parts=["CAT-001", "OXY-001"],
        labor_hours=2.5
    )
    
    print("\nTest: Catalytic converter + oxygen sensor replacement")
    print(f"Parts cost: {format_currency(result['parts_cost'])}")
    print(f"Labor cost: {format_currency(result['labor_cost'])}")
    print(f"Total before tax: {format_currency(result['total_before_tax'])}")
    print(f"Tax: {format_currency(result['tax_amount'])}")
    print(f"GRAND TOTAL: {result['formatted_total']}")
    
    print(f"\nParts breakdown:")
    for part in result['parts_details']:
        print(f"  - {part['name']}: {format_currency(part['price'])} ({part['type']})")
    
    print("\n✅ Cost calculator tool test completed")
