
import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.tools_impl.known_issues import query_known_issues
from src.tools_impl.diagnostic_codes import search_diagnostic_code
from src.tools_impl.parts_finder import find_replacement_parts

def verify_expansion():
    print("Verifying Data Expansion...")
    print("-" * 50)
    
    # 1. Check BMW Issues
    print("\n1. Checking BMW 3 Series...")
    issues = query_known_issues("BMW", "3 Series", 2017)
    if issues['issues_found'] > 0:
        print(f"✅ Found {issues['issues_found']} BMW issues.")
    else:
        print("❌ BMW issues not found.")

    # 2. Check U0100 Code
    print("\n2. Checking U0100 Code...")
    code = search_diagnostic_code("U0100")
    if code['found']:
        print(f"✅ Found U0100: {code.get('description')}")
    else:
        print("❌ U0100 Code not found.")
        
    # 3. Check New Parts
    print("\n3. Checking Window Regulator for BMW...")
    vehicle = {"brand": "BMW", "model": "3 Series", "year": "2017"}
    parts = find_replacement_parts(vehicle, "window regulator")
    
    if parts.get('parts_found', 0) > 0:
        print(f"✅ Found {parts['parts_found']} parts.")
    else:
        print("❌ Window Regulator not found.")

if __name__ == "__main__":
    verify_expansion()
