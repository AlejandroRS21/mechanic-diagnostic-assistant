#!/usr/bin/env python3
"""
Search Qdrant directly for P0258 in all documents.
"""

import logging
logging.basicConfig(level=logging.WARNING)

from src.rag.knowledge_base import KnowledgeBase

kb = KnowledgeBase()

# Use the raw vectorstore search with higher k
results = kb.vectorstore.similarity_search("P0258", k=20)

print("\n" + "="*80)
print("DIRECT VECTORSTORE SEARCH FOR P0258 (k=20)")
print("="*80)

found_p0258 = False
for i, result in enumerate(results):
    content = result.page_content if hasattr(result, 'page_content') else result.get("content", "")
    
    if "P0258" in content.upper():
        print(f"\n✅ [RESULT {i+1}] - CONTAINS P0258!")
        print(f"Content:\n{content}")
        print(f"Metadata: {result.metadata if hasattr(result, 'metadata') else result.get('metadata', {})}")
        found_p0258 = True
        break

if not found_p0258:
    print("\n❌ P0258 NOT FOUND in any of the 20 results")
    print("\nShowing first result content:")
    result = results[0]
    print(result.page_content[:500] if hasattr(result, 'page_content') else str(result)[:500])
