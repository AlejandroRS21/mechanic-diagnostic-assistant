#!/usr/bin/env python3
"""
Check what documents are actually in Qdrant.
"""

import logging
logging.basicConfig(level=logging.WARNING)

from src.rag.knowledge_base import KnowledgeBase
from qdrant_client import QdrantClient
from src.utils.config import QDRANT_PATH, QDRANT_COLLECTION_NAME

# Get basic info about the collection
client = QdrantClient(QDRANT_PATH)
collection_info = client.get_collection(QDRANT_COLLECTION_NAME)

print("\n" + "="*80)
print(f"QDRANT COLLECTION: {QDRANT_COLLECTION_NAME}")
print("="*80)
print(f"Total points: {collection_info.points_count}")
print(f"Vector size: {collection_info.config.params.vectors.size}")

# Get some sample documents
print("\n" + "="*80)
print("SAMPLING DOCUMENTS FROM QDRANT")
print("="*80)

kb = KnowledgeBase()

# Search for a known code that should be there
known_codes = ["P0420", "P0300", "P0420", "P0211", "P0215"]

for code in known_codes:
    results = kb.search(code, k=1)
    if results:
        result = results[0]
        content = result.page_content if hasattr(result, 'page_content') else str(result)[:200]
        print(f"\n{code}:")
        print(f"  Content: {content[:150]}")
        metadata = result.metadata if hasattr(result, 'metadata') else {}
        print(f"  Metadata: {metadata}")
    else:
        print(f"\n{code}: NO RESULTS")

# List all unique sources
print("\n" + "="*80)
print("SEARCHING FOR ALL P0XXX CODES")
print("="*80)

results = kb.search("P0", k=50)
codes_found = set()
for result in results:
    content = result.page_content if hasattr(result, 'page_content') else str(result)
    # Extract codes
    lines = content.split('\n')
    for line in lines:
        if 'P0' in line:
            # Try to extract the code
            parts = line.split()
            for part in parts:
                if part.startswith('P0') and len(part) >= 5:
                    codes_found.add(part[:5])

print(f"\nUnique P0XXX codes found in search results:")
for code in sorted(codes_found):
    print(f"  {code}")

# Check if P0258 is in any of them
if "P0258" in codes_found:
    print("\n✅ P0258 IS IN THE DATABASE")
else:
    print("\n❌ P0258 IS NOT IN THE DATABASE")
