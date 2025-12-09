
from src.tools_impl.parts_finder import find_replacement_parts

def test_year_range():
    print("Testing Year Range Logic...")
    
    # Case 1: BMW 3 Series 2017 vs "BMW 3 Series 2015-2021"
    # This is expected to fail with current logic
    vehicle = {"brand": "BMW", "model": "3 Series", "year": "2017"}
    result = find_replacement_parts(vehicle, "window regulator")
    print(f"BMW 2017 Result: Found {result['parts_found']} parts")
    
    # Case 2: Matching string exact year
    # Let's say we had a part for 2017 specifically
    # For now, let's try Corolla 2018 vs "Toyota Corolla 2015-2020"
    # If the original code works, this should pass. If not, the original code is also broken for ranges.
    vehicle2 = {"brand": "Toyota", "model": "Corolla", "year": "2018"}
    result2 = find_replacement_parts(vehicle2, "catalytic converter")
    print(f"Corolla 2018 Result: Found {result2['parts_found']} parts")

if __name__ == "__main__":
    test_year_range()
