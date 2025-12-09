#!/usr/bin/env python3
"""
Test P0258 search with new fallback mechanism.
This test verifies that P0258 (not in JSON) is found via vector search fallback.
"""

import sys
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_p0258_fallback():
    """Test that P0258 is found via vector search fallback."""
    print("\n" + "="*70)
    print("TEST: P0258 Search with Vector Database Fallback")
    print("="*70)
    
    try:
        from src.tools_impl.diagnostic_codes import search_diagnostic_code
        
        # Test 1: P0420 (should be in JSON)
        print("\n[TEST 1] P0420 - Should be found in JSON database")
        print("-" * 70)
        result1 = search_diagnostic_code("P0420")
        print(f"✅ Found: {result1['found']}")
        if result1['found']:
            print(f"   Description: {result1['description'][:80]}...")
            print(f"   Source: JSON Database")
        print(f"   Message: {result1.get('message', 'N/A')}")
        
        # Test 2: P0258 (NOT in JSON, should use fallback)
        print("\n[TEST 2] P0258 - Should be found via vector search fallback")
        print("-" * 70)
        result2 = search_diagnostic_code("P0258")
        print(f"Found: {result2['found']}")
        if result2['found']:
            print(f"✅ SUCCESS - P0258 found via fallback!")
            print(f"   Description: {result2['description'][:100]}...")
            print(f"   Source: {result2.get('source', 'N/A')}")
            print(f"   Document: {result2.get('document', 'N/A')}")
            if 'content_snippet' in result2:
                print(f"   Content preview: {result2['content_snippet'][:150]}...")
        else:
            print(f"❌ FAILED - P0258 not found")
            print(f"   Message: {result2.get('message', 'N/A')}")
        print(f"   Message: {result2.get('message', 'N/A')}")
        
        # Test 3: Invalid code (should not be found)
        print("\n[TEST 3] P9999 - Should not be found")
        print("-" * 70)
        result3 = search_diagnostic_code("P9999")
        print(f"Found: {result3['found']}")
        if not result3['found']:
            print(f"✅ Correctly reported as not found")
        print(f"   Message: {result3.get('message', 'N/A')}")
        
        # Summary
        print("\n" + "="*70)
        print("SUMMARY")
        print("="*70)
        p0420_ok = result1['found']
        p0258_ok = result2['found']
        p9999_ok = not result3['found']
        
        print(f"✅ P0420 (JSON search): {'PASS' if p0420_ok else 'FAIL'}")
        print(f"✅ P0258 (Vector fallback): {'PASS' if p0258_ok else 'FAIL'}")
        print(f"✅ P9999 (Not found): {'PASS' if p9999_ok else 'FAIL'}")
        
        if p0420_ok and p0258_ok and p9999_ok:
            print("\n🎉 ALL TESTS PASSED - Fallback mechanism working correctly!")
            return True
        else:
            print("\n⚠️  SOME TESTS FAILED - Review results above")
            return False
            
    except Exception as e:
        logger.error(f"Error during test: {e}", exc_info=True)
        print(f"\n❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    success = test_p0258_fallback()
    sys.exit(0 if success else 1)
