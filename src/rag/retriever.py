"""
Retriever configuration for querying the knowledge base.
"""

from typing import List, Dict
from qdrant_client import QdrantClient

try:
    from langchain.schema import Document
except ImportError:
    try:
        from langchain_core.documents import Document
    except ImportError:
        from langchain.docstore.document import Document

from src.utils.helpers import get_logger
from src.utils.config import TOP_K_RESULTS, QDRANT_HOST, QDRANT_PORT, QDRANT_API_KEY, QDRANT_COLLECTION_NAME
from src.rag.knowledge_base import KnowledgeBase

logger = get_logger(__name__)


class KnowledgeRetriever:
    """
    Wrapper for retrieving relevant information from the knowledge base.
    """
    
    def __init__(self, knowledge_base: 'KnowledgeBase', k: int = TOP_K_RESULTS):
        """
        Initialize the retriever.
        
        Args:
            knowledge_base: KnowledgeBase instance
            k: Number of documents to retrieve
        """
        self.knowledge_base = knowledge_base
        self.k = k
    
    def retrieve(self, query: str) -> List[Document]:
        """
        Retrieve relevant documents for a query.
        
        Args:
            query: Search query
            
        Returns:
            List of relevant documents
        """
        logger.info(f"Retrieving documents for query: '{query}'")
        docs = self.knowledge_base.search(query, k=self.k)
        logger.info(f"Retrieved {len(docs)} documents")
        return docs
    
    def format_context(self, documents: List[Document]) -> str:
        """
        Format retrieved documents into a context string for the LLM.
        
        Args:
            documents: List of retrieved documents
            
        Returns:
            Formatted context string
        """
        if not documents:
            return "No relevant information found in knowledge base."
        
        context_parts = []
        for i, doc in enumerate(documents, 1):
            source = doc.metadata.get('source', 'unknown')
            content = doc.page_content.strip()
            
            context_parts.append(
                f"[Source {i}: {source}]\n{content}\n"
            )
        
        context = "\n".join(context_parts)
        return context
    
    def retrieve_and_format(self, query: str) -> str:
        """
        Retrieve documents and format them as context.
        
        Args:
            query: Search query
            
        Returns:
            Formatted context string
        """
        docs = self.retrieve(query)
        return self.format_context(docs)

    def retrieve_with_sources(self, query: str) -> tuple[str, List[Dict]]:
        """
        Retrieve documents and return formatted context with source metadata.
        
        Args:
            query: Search query
            
        Returns:
            Tuple of (formatted_context, list_of_source_metadata)
        """
        docs = self.retrieve(query)
        context = self.format_context(docs)
        
        sources = []
        for doc in docs:
            metadata = doc.metadata or {}
            
            # Build source title based on document type
            source_type = metadata.get("type", "").lower()
            source_name = metadata.get("source", "unknown").lower()
            
            # Create descriptive title
            if source_type == "diagnostic_code":
                title = f"OBD Code {metadata.get('code', 'Unknown')}"
            elif source_type == "symptom":
                title = f"Symptom: {metadata.get('symptom', 'Unknown')}"
            elif source_type == "repair_guide":
                title = f"Repair Guide: {metadata.get('repair_name', 'Unknown')}"
            elif "pdf" in source_name or "manual" in source_name:
                title = metadata.get("filename", "Technical Manual")
            else:
                # Fallback to repair_name, symptom, code, or filename
                title = (
                    metadata.get("repair_name") or 
                    metadata.get("symptom") or 
                    metadata.get("code") or 
                    metadata.get("filename") or 
                    f"Document ({source_name})"
                )
            
            sources.append({
                "source": source_name,
                "title": title,
                "type": source_type,
                "page": metadata.get("page"),
                "score": round(metadata.get("score", 0), 3)
            })
            
        return context, sources
    
    def get_base_retriever(self):
        """Get the underlying LangChain retriever."""
        return self.retriever


if __name__ == "__main__":
    # Test retriever
    from src.rag.knowledge_base import initialize_knowledge_base
    
    print("Initializing retriever...")
    print("-" * 50)
    
    kb = initialize_knowledge_base()
    retriever = KnowledgeRetriever(kb.get_vectorstore(), k=3)
    
    # Test retrieval
    test_query = "rough idle and engine stalling"
    print(f"\nTest query: '{test_query}'")
    print("-" * 50)
    
    context = retriever.retrieve_and_format(test_query)
    
    print("\nFormatted context:")
    print(context)
    
    print("\n✅ Retriever test completed")
