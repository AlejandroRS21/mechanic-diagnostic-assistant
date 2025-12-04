"""
Tests for RAG system.
Run with: pytest tests/test_rag.py -v
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def test_rag_imports():
    """Test RAG modules can be imported."""
    try:
        from src.rag.document_loader import load_all_knowledge_base
        from src.rag.knowledge_base import KnowledgeBase
        from src.rag.retriever import KnowledgeRetriever
        assert True
    except ImportError as e:
        pytest.fail(f"Failed to import RAG modules: {e}")


def test_document_loading():
    """Test that documents can be loaded."""
    from src.rag.document_loader import load_all_knowledge_base
    from src.utils.config import OBD_CODES_PATH, SYMPTOMS_PATH, REPAIR_GUIDES_PATH
    
    docs = load_all_knowledge_base(OBD_CODES_PATH, SYMPTOMS_PATH, REPAIR_GUIDES_PATH)
    
    assert len(docs) > 0, "No documents loaded"
    assert hasattr(docs[0], 'page_content'), "Document missing page_content"
    assert hasattr(docs[0], 'metadata'), "Document missing metadata"


@pytest.mark.skip(reason="Requires API keys and time - run manually")
def test_knowledge_base_search():
    """Test knowledge base search (requires API keys)."""
    from src.rag.knowledge_base import initialize_knowledge_base
    
    kb = initialize_knowledge_base(rebuild=False)
    results = kb.search("P0420 catalytic converter", k=3)
    
    assert len(results) > 0, "No search results"
    assert len(results) <= 3, "Too many results returned"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
