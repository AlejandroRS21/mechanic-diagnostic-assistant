#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test script para verificar que el retriever funciona correctamente.
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, '/content')

from src.rag.knowledge_base import initialize_knowledge_base
from src.rag.retriever import KnowledgeRetriever

print("=" * 60)
print("Test 1: Inicializar Knowledge Base")
print("=" * 60)

try:
    kb = initialize_knowledge_base(rebuild=True)
    print("✅ Knowledge base inicializado correctamente")
except Exception as e:
    print(f"❌ Error al inicializar: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("Test 2: Crear Retriever")
print("=" * 60)

try:
    retriever = KnowledgeRetriever(kb, k=3)
    print("✅ Retriever creado correctamente")
except Exception as e:
    print(f"❌ Error al crear retriever: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("Test 3: Buscar documentos")
print("=" * 60)

try:
    query = "P0420 catalytic converter"
    docs = kb.search(query, k=3)
    print(f"✅ Búsqueda exitosa: {len(docs)} documentos encontrados")
    for i, doc in enumerate(docs, 1):
        print(f"\n  Doc {i}:")
        print(f"    Fuente: {doc.metadata.get('source', 'unknown')}")
        print(f"    Preview: {doc.page_content[:100]}...")
except Exception as e:
    print(f"❌ Error en búsqueda: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("Test 4: Retriever retrieve_with_sources")
print("=" * 60)

try:
    context, sources = retriever.retrieve_with_sources("El auto hace ruido al frenar")
    print(f"✅ retrieve_with_sources exitoso")
    print(f"   Context length: {len(context)} chars")
    print(f"   Sources found: {len(sources)}")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("✅ TODOS LOS TESTS PASARON")
print("=" * 60)
