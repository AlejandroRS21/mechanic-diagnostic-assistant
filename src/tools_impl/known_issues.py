"""
Tool 4: Query known issues for specific vehicle makes/models.
"""

from typing import Dict, List
from src.utils.helpers import get_logger, contains_substring
from src.utils.config import OBD_CODES_PATH, SYMPTOMS_PATH

logger = get_logger(__name__)


# Mock database of known vehicle-specific issues
# In a real application, this would be a more comprehensive database
KNOWN_ISSUES_DATABASE = {
    "Toyota Corolla": {
        "years": "2015-2020",
        "common_issues": [
            {
                "issue": "Premature catalytic converter failure",
                "frequency": "Common",
                "typical_mileage": "80,000-120,000 miles",
                "symptoms": ["P0420 code", "Check engine light", "Reduced fuel economy"],
                "note": "Known issue with 2015-2018 models, extended warranty may apply"
            },
            {
                "issue": "CVT transmission hesitation",
                "frequency": "Moderate",
                "typical_mileage": "60,000-100,000 miles",
                "symptoms": ["Delayed acceleration", "Slipping sensation", "Whining noise"],
                "note": "Regular CVT fluid changes can help prevent this issue"
            },
            {
                "issue": "Excessive oil consumption",
                "frequency": "Moderate",
                "typical_mileage": "70,000+ miles",
                "symptoms": ["Low oil level", "Blue smoke from exhaust"],
                "note": "Most common in 2015-2016 models"
            }
        ]
    },
    "Honda Civic": {
        "years": "2016-2021",
        "common_issues": [
            {
                "issue": "Fuel injector failure",
                "frequency": "Moderate",
                "typical_mileage": "50,000-80,000 miles",
                "symptoms": ["Rough idle", "Misfire codes", "Poor fuel economy"],
                "note": "More common in 1.5L turbo engines"
            },
            {
                "issue": "AC compressor clutch failure",
                "frequency": "Common",
                "typical_mileage": "80,000+ miles",
                "symptoms": ["AC not blowing cold", "Clicking noise from engine bay"],
                "note": "Extended warranty available for some model years"
            },
            {
                "issue": "Warped brake rotors",
                "frequency": "Common",
                "typical_mileage": "30,000-50,000 miles",
                "symptoms": ["Vibration when braking", "Pulsating brake pedal"],
                "note": "Regular brake inspections recommended"
            }
        ]
    },
    "Nissan Sentra": {
        "years": "2016-2020",
        "common_issues": [
            {
                "issue": "CVT transmission failure",
                "frequency": "Common",
                "typical_mileage": "60,000-100,000 miles",
                "symptoms": ["Shuddering", "Delayed engagement", "Transmission overheating"],
                "note": "Extended warranty program available for some model years"
            },
            {
                "issue": "Oxygen sensor failure",
                "frequency": "Moderate",
                "typical_mileage": "70,000+ miles",
                "symptoms": ["Check engine light", "Poor fuel economy"],
                "note": "Regular replacement recommended"
            }
        ]
    },
    "Ford F-150": {
        "years": "2015-2020",
        "common_issues": [
            {
                "issue": "Spark plug ejection (5.4L V8)",
                "frequency": "Moderate",
                "typical_mileage": "100,000+ miles",
                "symptoms": ["Misfire", "Loss of power", "Loud popping noise"],
                "note": "Helicoil repair required, preventive maintenance recommended"
            },
            {
                "issue": "EcoBoost turbo failure",
                "frequency": "Moderate",
                "typical_mileage": "80,000-120,000 miles",
                "symptoms": ["Loss of boost", "Blue smoke", "Rattling noise"],
                "note": "More common if oil changes are delayed"
            }
        ]
    },
    "Chevrolet Silverado": {
        "years": "2014-2019",
        "common_issues": [
            {
                "issue": "Active Fuel Management (AFM) lifter failure",
                "frequency": "Common",
                "typical_mileage": "80,000+ miles",
                "symptoms": ["Ticking noise", "Check engine light", "Rough running"],
                "note": "AFM delete kits available, some extended warranty coverage"
            },
            {
                "issue": "Water pump failure",
                "frequency": "Moderate",
                "typical_mileage": "60,000-100,000 miles",
                "symptoms": ["Coolant leak", "Overheating", "Squealing noise"],
                "note": "Regular coolant system maintenance recommended"
            }
        ]
    }
}


def query_known_issues(brand: str, model: str, year: int = None) -> Dict:
    """
    Query known issues for a specific vehicle make and model.
    
    Args:
        brand: Vehicle brand (e.g., "Toyota")
        model: Vehicle model (e.g., "Corolla")
        year: Optional year (e.g., 2018)
        
    Returns:
        Dictionary with known issues for the vehicle
    """
    vehicle_key = f"{brand} {model}".strip()
    logger.info(f"Querying known issues for: {vehicle_key} {year if year else ''}")
    
    try:
        # Search for matching vehicle in database
        matching_vehicle = None
        
        for key in KNOWN_ISSUES_DATABASE.keys():
            if (contains_substring(key, brand, case_sensitive=False) and 
                contains_substring(key, model, case_sensitive=False)):
                matching_vehicle = key
                break
        
        if matching_vehicle:
            vehicle_data = KNOWN_ISSUES_DATABASE[matching_vehicle]
            
            result = {
                "vehicle": matching_vehicle,
                "years_covered": vehicle_data["years"],
                "query_year": year,
                "issues_found": len(vehicle_data["common_issues"]),
                "common_issues": vehicle_data["common_issues"]
            }
            
            logger.info(f"Found {result['issues_found']} known issues for {matching_vehicle}")
            return result
        else:
            logger.info(f"No specific known issues data for {vehicle_key}")
            return {
                "vehicle": vehicle_key,
                "query_year": year,
                "issues_found": 0,
                "common_issues": [],
                "message": f"No specific known issues database entry for {vehicle_key}. "
                          "This doesn't mean the vehicle has no issues, just that we don't "
                          "have documented common problems in our database. Recommend standard "
                          "diagnostic procedures."
            }
    
    except Exception as e:
        logger.error(f"Error querying known issues: {e}")
        return {
            "error": str(e),
            "issues_found": 0,
            "common_issues": []
        }


if __name__ == "__main__":
    # Test the tool
    print("Testing known issues query tool...")
    print("-" * 50)
    
    # Test 1: Toyota Corolla
    result1 = query_known_issues("Toyota", "Corolla", 2018)
    print(f"\nTest 1: {result1['vehicle']} ({result1.get('query_year', 'Any year')})")
    print(f"Issues found: {result1['issues_found']}")
    if result1['issues_found'] > 0:
        for issue in result1['common_issues']:
            print(f"\n  Issue: {issue['issue']}")
            print(f"  Frequency: {issue['frequency']}")
            print(f"  Symptoms: {', '.join(issue['symptoms'][:2])}")
    
    # Test 2: Vehicle not in database
    result2 = query_known_issues("BMW", "3 Series", 2020)
    print(f"\nTest 2: BMW 3 Series 2020")
    print(f"Issues found: {result2['issues_found']}")
    if 'message' in result2:
        print(f"Message: {result2['message'][:100]}...")
    
    print("\n✅ Known issues tool test completed")
