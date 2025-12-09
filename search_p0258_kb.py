#!/usr/bin/env python3
"""
Search Qdrant directly for P0258 in all documents using the knowledge_base method.
"""

import logging
logging.basicConfig(level=logging.WARNING)

from src.rag.knowledge_base import KnowledgeBase

kb = KnowledgeBase()

# Use the knowledge base search_with_scores method with higher k
try:
    results_with_scores = kb.search_with_scores("P0258", k=20)
except:
    # Fallback to regular search
    results_with_scores = kb.search("P0258", k=20)

print("\n" + "="*80)
print("KNOWLEDGE BASE SEARCH FOR P0258 (k=20)")
print("="*80)

found_p0258 = False
for i, item in enumerate(results_with_scores):
    # Handle both tuple and Document returns
    if isinstance(item, tuple):
        result, score = item
    else:
        result = item
        score = "N/A"
    
    content = result.page_content if hasattr(result, 'page_content') else str(result)[:500]
    
    if "P0258" in content.upper():
        print(f"\n✅ [RESULT {i+1}] - CONTAINS P0258! (Score: {score})")
        print(f"Content:\n{content}")
        metadata = result.metadata if hasattr(result, 'metadata') else {}
        print(f"Metadata: {metadata}")
        found_p0258 = True
        break
    else:
        print(f"[{i+1}] Score: {score}, Contains P0258: False")

if not found_p0258:
    print("\n❌ P0258 NOT FOUND in any of the 20 results")
