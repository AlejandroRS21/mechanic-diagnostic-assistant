#!/usr/bin/env python3
"""
Debug script to check if knowledge base documents are being loaded properly.
"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.utils.helpers import get_logger
from src.rag.document_loader import load_all_knowledge_base
from src.utils.config import (
    OBD_CODES_PATH,
    SYMPTOMS_PATH,
    REPAIR_GUIDES_PATH,
    PDF_DOCS_PATH
)

logger = get_logger(__name__)

print("=" * 60)
print("Loading Documents")
print("=" * 60)

# Check file paths
print(f"OBD_CODES_PATH: {OBD_CODES_PATH}")
print(f"  Exists: {OBD_CODES_PATH.exists()}")

print(f"SYMPTOMS_PATH: {SYMPTOMS_PATH}")
print(f"  Exists: {SYMPTOMS_PATH.exists()}")

print(f"REPAIR_GUIDES_PATH: {REPAIR_GUIDES_PATH}")
print(f"  Exists: {REPAIR_GUIDES_PATH.exists()}")

print(f"PDF_DOCS_PATH: {PDF_DOCS_PATH}")
print(f"  Exists: {PDF_DOCS_PATH.exists()}")

print("\nLoading all documents...")
documents = load_all_knowledge_base(
    OBD_CODES_PATH,
    SYMPTOMS_PATH,
    REPAIR_GUIDES_PATH,
    PDF_DOCS_PATH
)

print(f"\n✅ Total documents loaded: {len(documents)}")
if documents:
    print(f"First document:\n{documents[0]}")
else:
    print("❌ ERROR: No documents loaded!")
