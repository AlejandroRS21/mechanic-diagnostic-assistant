#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to check if P0258 is in the PDF documents.
"""

import sys
import os
import io

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.rag.knowledge_base import initialize_knowledge_base
from src.utils.helpers import get_logger

logger = get_logger(__name__)

print("=" * 70)
print("TEST: Search for P0258 in Knowledge Base")
print("=" * 70)

try:
    # Initialize knowledge base
    print("\nInitializing knowledge base...")
    kb = initialize_knowledge_base(rebuild=False)
    print("Knowledge base loaded")
    
    # Search for P0258
    print("\n" + "=" * 70)
    print("Searching for: P0258")
    print("=" * 70)
    
    results = kb.search("P0258", k=5)
    
    print(f"\nFound {len(results)} results:")
    for i, doc in enumerate(results, 1):
        print(f"\n{i}. Source: {doc.metadata.get('source', 'unknown')}")
        print(f"   Type: {doc.metadata.get('type', 'unknown')}")
        print(f"   Score: {doc.metadata.get('score', 0)}")
        print(f"   Content preview (first 200 chars):")
        print(f"   {doc.page_content[:200]}...")
    
    # Also search for "Fuel Injector Circuit" which is what P0258 is about
    print("\n" + "=" * 70)
    print("Searching for: Fuel Injector Circuit")
    print("=" * 70)
    
    results2 = kb.search("Fuel Injector Circuit", k=5)
    
    print(f"\nFound {len(results2)} results:")
    for i, doc in enumerate(results2, 1):
        print(f"\n{i}. Source: {doc.metadata.get('source', 'unknown')}")
        print(f"   Content preview (first 200 chars):")
        content_preview = doc.page_content[:200]
        if "P0258" in doc.page_content:
            print(f"   *** CONTAINS P0258 ***")
            # Find and show the section with P0258
            lines = doc.page_content.split('\n')
            for j, line in enumerate(lines):
                if "P0258" in line:
                    start = max(0, j-2)
                    end = min(len(lines), j+3)
                    print(f"\n   Context around P0258:")
                    print(f"   {chr(10).join(lines[start:end])}")
                    break
        else:
            print(f"   {content_preview}...")
    
    print("\n" + "=" * 70)
    print("TEST COMPLETED")
    print("=" * 70)
    
except Exception as e:
    print(f"\nError during test: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
