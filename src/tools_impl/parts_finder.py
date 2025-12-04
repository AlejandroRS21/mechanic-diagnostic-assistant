"""
Tool 3: Find replacement parts compatible with a specific vehicle.
"""

from typing import Dict, List
from src.utils.helpers import get_logger, load_json_file, format_currency, filter_dict_list, contains_substring
from src.utils.config import PARTS_CATALOG_PATH

logger = get_logger(__name__)


def find_replacement_parts(vehicle: Dict[str, str], part_name: str) -> Dict:
    """
    Find replacement parts available for a specific vehicle.
    
    Args:
        vehicle: Dictionary with keys 'brand', 'model', 'year' (e.g., {"brand": "Toyota", "model": "Corolla", "year": "2018"})
        part_name: Name or category of part to find (e.g., "catalytic converter", "brake pads")
        
    Returns:
        Dictionary with list of available parts
    """
    brand = vehicle.get("brand", "").strip()
    model = vehicle.get("model", "").strip()
    year = vehicle.get("year", "").strip()
    
    vehicle_str = f"{brand} {model} {year}".strip()
    logger.info(f"Searching for '{part_name}' compatible with {vehicle_str}")
    
    try:
        # Load parts catalog
        parts_catalog = load_json_file(PARTS_CATALOG_PATH)
        parts_list = parts_catalog["parts"]
        
        # Search for parts matching the name
        matching_parts = []
        
        for part in parts_list:
            # Check if part name matches
            if contains_substring(part["name"], part_name, case_sensitive=False):
                # Check vehicle compatibility
                compatible = False
                
                if vehicle_str:
                    for compatible_vehicle in part["compatible_vehicles"]:
                        # Check if vehicle matches
                        if (contains_substring(compatible_vehicle, brand, case_sensitive=False) and
                            contains_substring(compatible_vehicle, model, case_sensitive=False)):
                            # Check year if specified
                            if year:
                                if year in compatible_vehicle or not any(char.isdigit() for char in year):
                                    compatible = True
                                    break
                            else:
                                compatible = True
                                break
                else:
                    # No vehicle specified, show all parts that match name
                    compatible = True
                
                if compatible:
                    matching_parts.append({
                        "id": part["id"],
                        "name": part["name"],
                        "price": part["price"],
                        "formatted_price": format_currency(part["price"]),
                        "type": part["type"],
                        "category": part["category"],
                        "warranty_months": part.get("warranty_months"),
                        "compatible_vehicles": part["compatible_vehicles"]
                    })
        
        # Sort by price to show both OEM and aftermarket options
        matching_parts.sort(key=lambda x: x["price"])
        
        result = {
            "vehicle": vehicle_str if vehicle_str else "Any vehicle",
            "part_searched": part_name,
            "parts_found": len(matching_parts),
            "parts": matching_parts
        }
        
        if matching_parts:
            logger.info(f"Found {len(matching_parts)} compatible parts")
            # Add price range summary
            prices = [p["price"] for p in matching_parts]
            result["price_range"] = {
                "min": min(prices),
                "max": max(prices),
                "formatted": f"{format_currency(min(prices))} - {format_currency(max(prices))}"
            }
        else:
            logger.warning(f"No parts found for '{part_name}' compatible with {vehicle_str}")
        
        return result
    
    except Exception as e:
        logger.error(f"Error finding parts: {e}")
        return {
            "error": str(e),
            "parts_found": 0,
            "parts": []
        }


if __name__ == "__main__":
    # Test the tool
    print("Testing parts finder tool...")
    print("-" * 50)
    
    # Test 1: Find catalytic converter for Toyota Corolla
    vehicle1 = {"brand": "Toyota", "model": "Corolla", "year": "2018"}
    result1 = find_replacement_parts(vehicle1, "catalytic converter")
    
    print(f"\nTest 1: Catalytic converter for {result1['vehicle']}")
    print(f"Parts found: {result1['parts_found']}")
    if result1['parts_found'] > 0:
        print(f"Price range: {result1['price_range']['formatted']}")
        for part in result1['parts']:
            print(f"  - {part['name']}: {part['formatted_price']} ({part['type']})")
    
    # Test 2: Find brake pads
    vehicle2 = {"brand": "Honda", "model": "Civic", "year": "2020"}
    result2 = find_replacement_parts(vehicle2, "brake pads")
    
    print(f"\nTest 2: Brake pads for {result2['vehicle']}")
    print(f"Parts found: {result2['parts_found']}")
    if result2['parts_found'] > 0:
        for part in result2['parts'][:2]:  # Show first 2
            print(f"  - {part['name']}: {part['formatted_price']} ({part['type']})")
    
    print("\n✅ Parts finder tool test completed")
