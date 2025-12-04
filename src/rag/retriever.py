"""
Retriever configuration for querying the knowledge base.
"""

from typing import List, Dict
from langchain.docstore.document import Document
from langchain.vectorstores import Chroma

from src.utils.helpers import get_logger
from src.utils.config import TOP_K_RESULTS

logger = get_logger(__name__)


class KnowledgeRetriever:
    """
    Wrapper for retrieving relevant information from the knowledge base.
    """
    
    def __init__(self, vectorstore: Chroma, k: int = TOP_K_RESULTS):
        """
        Initialize the retriever.
        
        Args:
            vectorstore: ChromaDB vector store
            k: Number of documents to retrieve
        """
        self.vectorstore = vectorstore
        self.k = k
        self.retriever = vectorstore.as_retriever(
            search_kwargs={"k": k}
        )
    
    def retrieve(self, query: str) -> List[Document]:
        """
        Retrieve relevant documents for a query.
        
        Args:
            query: Search query
            
        Returns:
            List of relevant documents
        """
        logger.info(f"Retrieving documents for query: '{query}'")
        docs = self.retriever.get_relevant_documents(query)
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
            sources.append({
                "source": doc.metadata.get("source", "unknown"),
                "title": doc.metadata.get("repair_name") or doc.metadata.get("symptom") or doc.metadata.get("code") or doc.metadata.get("filename") or "Unknown Document",
                "type": doc.metadata.get("type", "unknown"),
                "page": doc.metadata.get("page", 1) if "page" in doc.metadata else None
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
