"""
Knowledge base setup using ChromaDB for vector storage.
Handles document embedding and vector database creation/management.
"""

from typing import List, Optional
from pathlib import Path

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document

from src.utils.helpers import get_logger
from src.utils.config import (
    CHROMA_DB_PATH,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    OBD_CODES_PATH,
    SYMPTOMS_PATH,
    REPAIR_GUIDES_PATH,
    PDF_DOCS_PATH
)
from src.rag.document_loader import load_all_knowledge_base

logger = get_logger(__name__)


class KnowledgeBase:
    """
    Manages the vector database for automotive knowledge.
    """
    
    def __init__(
        self,
        persist_directory: str = CHROMA_DB_PATH,
        rebuild: bool = False
    ):
        """
        Initialize the knowledge base.
        
        Args:
            persist_directory: Directory to store ChromaDB
            rebuild: If True, rebuild the database from scratch
        """
        self.persist_directory = persist_directory
        
        # Use HuggingFace embeddings (FREE alternative to OpenAI)
        logger.info("Initializing HuggingFace embeddings (all-MiniLM-L6-v2)...")
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
        self.vectorstore: Optional[Chroma] = None
        
        # Initialize or load the database
        if rebuild or not self._database_exists():
            logger.info("Building knowledge base from scratch...")
            self._build_database()
        else:
            logger.info("Loading existing knowledge base...")
            self._load_database()
    
    def _database_exists(self) -> bool:
        """Check if the ChromaDB database already exists."""
        db_path = Path(self.persist_directory)
        return db_path.exists() and any(db_path.iterdir())
    
    def _build_database(self):
        """Build the vector database from knowledge base files."""
        logger.info("Loading documents from knowledge base...")
        
        # Load all documents
        documents = load_all_knowledge_base(
            OBD_CODES_PATH,
            SYMPTOMS_PATH,
            REPAIR_GUIDES_PATH,
            PDF_DOCS_PATH
        )
        
        # Split documents into chunks
        logger.info("Splitting documents into chunks...")
        chunks = self.text_splitter.split_documents(documents)
        logger.info(f"Created {len(chunks)} chunks from {len(documents)} documents")
        
        # Create vector store
        logger.info("Creating embeddings and building vector database...")
        logger.info("(This may take a few minutes on first run...)")
        
        self.vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory=self.persist_directory,
            collection_name="automotive_knowledge"
        )
        
        # Persist to disk
        self.vectorstore.persist()
        logger.info(f"✅ Knowledge base built and persisted to {self.persist_directory}")
    
    def _load_database(self):
        """Load an existing vector database from disk."""
        try:
            self.vectorstore = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings,
                collection_name="automotive_knowledge"
            )
            logger.info("✅ Knowledge base loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load database: {e}")
            logger.info("Rebuilding database...")
            self._build_database()
    
    def search(self, query: str, k: int = 3) -> List[Document]:
        """
        Search the knowledge base for relevant documents.
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of relevant documents
        """
        if not self.vectorstore:
            raise ValueError("Vector store not initialized")
        
        logger.info(f"Searching knowledge base for: '{query}'")
        results = self.vectorstore.similarity_search(query, k=k)
        logger.info(f"Found {len(results)} relevant documents")
        
        return results
    
    def search_with_scores(self, query: str, k: int = 3) -> List[tuple]:
        """
        Search with relevance scores.
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of (document, score) tuples
        """
        if not self.vectorstore:
            raise ValueError("Vector store not initialized")
        
        logger.info(f"Searching knowledge base (with scores) for: '{query}'")
        results = self.vectorstore.similarity_search_with_score(query, k=k)
        logger.info(f"Found {len(results)} relevant documents")
        
        return results
    
    def get_vectorstore(self) -> Chroma:
        """Get the underlying vector store."""
        if not self.vectorstore:
            raise ValueError("Vector store not initialized")
        return self.vectorstore
    
    def rebuild(self):
        """Rebuild the knowledge base from scratch."""
        logger.info("Rebuilding knowledge base...")
        self._build_database()


def initialize_knowledge_base(rebuild: bool = False) -> KnowledgeBase:
    """
    Initialize and return the knowledge base.
    
    Args:
        rebuild: Whether to rebuild from scratch
        
    Returns:
        Initialized KnowledgeBase instance
    """
    try:
        kb = KnowledgeBase(rebuild=rebuild)
        return kb
    except Exception as e:
        logger.error(f"Failed to initialize knowledge base: {e}")
        raise


if __name__ == "__main__":
    # Test knowledge base
    print("Initializing knowledge base...")
    print("-" * 50)
    
    kb = initialize_knowledge_base(rebuild=False)
    
    # Test search
    test_query = "P0420 catalytic converter"
    print(f"\nTesting search for: '{test_query}'")
    print("-" * 50)
    
    results = kb.search(test_query, k=2)
    
    for i, doc in enumerate(results, 1):
        print(f"\nResult {i}:")
        print(f"Source: {doc.metadata.get('source', 'unknown')}")
        print(f"Content preview: {doc.page_content[:200]}...")
    
    print("\n✅ Knowledge base test completed")
