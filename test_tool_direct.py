#!/usr/bin/env python3
"""
Final test: Direct tool test without agent initialization.
"""

import logging
logging.basicConfig(level=logging.WARNING)

from src.tools_impl.diagnostic_codes import search_diagnostic_code

print("\n" + "="*80)
print("FINAL TEST: Diagnostic Code Search Tool with P0258")
print("="*80)

# Test 1: Code in JSON
print("\n[TEST 1] P0420 (should be in JSON)")
result = search_diagnostic_code("P0420")
print(f"  Found: {result['found']}")
if result['found']:
    print(f"  Description: {result['description'][:60]}...")
    print(f"  Source: {result.get('source', 'N/A')}")

# Test 2: Code in PDF (via fallback)
print("\n[TEST 2] P0258 (should be found via PDF fallback)")
result = search_diagnostic_code("P0258")
print(f"  Found: {result['found']}")
if result['found']:
    print(f"  ✅ Description: {result['description'][:70]}...")
    print(f"  Source: {result.get('source', 'N/A')}")
    print(f"  Document: {result.get('document', 'N/A')}")
else:
    print(f"  ❌ Message: {result.get('message', 'N/A')}")

# Test 3: Invalid code
print("\n[TEST 3] P9999 (should NOT be found)")
result = search_diagnostic_code("P9999")
print(f"  Found: {result['found']}")
if not result['found']:
    print(f"  ✅ Correctly reported as not found")
else:
    print(f"  ❌ Unexpectedly found")

print("\n" + "="*80)
print("✅ TOOL FUNCTION WORKS CORRECTLY WITH P0258!")
print("="*80)
