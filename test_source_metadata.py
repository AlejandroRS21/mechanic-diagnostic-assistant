#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to verify source metadata extraction is working correctly.
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
from src.rag.retriever import KnowledgeRetriever
from src.utils.helpers import get_logger

logger = get_logger(__name__)

print("=" * 70)
print("TEST: Source Metadata Extraction")
print("=" * 70)

try:
    # Initialize knowledge base
    print("\nInitializing knowledge base...")
    kb = initialize_knowledge_base(rebuild=False)
    print("Knowledge base loaded")
    
    # Create retriever
    retriever = KnowledgeRetriever(kb, k=3)
    print("Retriever created")
    
    # Test queries in different languages
    test_queries = [
        "P0420 catalytic converter",
        "squealing noise when braking",
        "ruido al frenar"
    ]
    
    for query in test_queries:
        print("\n" + "=" * 70)
        print(f"Query: {query}")
        print("=" * 70)
        
        # Retrieve with sources
        context, sources = retriever.retrieve_with_sources(query)
        
        print(f"\nFound {len(sources)} sources:")
        for i, source in enumerate(sources, 1):
            print(f"\n{i}. Title: {source.get('title', 'Unknown')}")
            print(f"   Source: {source.get('source', 'unknown')}")
            print(f"   Type: {source.get('type', 'unknown')}")
            print(f"   Page: {source.get('page', 'N/A')}")
            print(f"   Score: {source.get('score', 0)}")
    
    print("\n" + "=" * 70)
    print("TEST COMPLETED SUCCESSFULLY")
    print("=" * 70)
    
except Exception as e:
    print(f"\nError during test: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
