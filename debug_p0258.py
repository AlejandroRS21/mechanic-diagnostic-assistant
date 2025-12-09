#!/usr/bin/env python3
"""
Debug script to see what's in the search results for P0258.
"""

import logging
logging.basicConfig(level=logging.INFO)

from src.rag.knowledge_base import KnowledgeBase

kb = KnowledgeBase()
results = kb.search("P0258", k=5)

print("\n" + "="*80)
print("SEARCH RESULTS FOR P0258")
print("="*80)

for i, result in enumerate(results):
    print(f"\n[RESULT {i+1}]")
    
    # Handle both Document objects and dict results
    if hasattr(result, 'page_content'):
        content = result.page_content
        metadata = result.metadata if hasattr(result, 'metadata') else {}
    else:
        content = result.get("content", "")
        metadata = result.get("metadata", {})
    
    print(f"Content preview (first 300 chars):\n{content[:300]}")
    print(f"Metadata: {metadata}")
    print(f"Contains 'P0258': {'P0258' in content.upper()}")
    print("-"*80)

print("\n✅ Debug search completed")
