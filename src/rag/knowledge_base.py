"""
Knowledge base setup using Qdrant for vector storage.
Handles document embedding and vector database creation/management.
"""

from typing import List, Optional
from pathlib import Path

try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except ImportError:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from langchain_community.embeddings import HuggingFaceEmbeddings

try:
    from langchain.schema import Document
except ImportError:
    try:
        from langchain_core.documents import Document
    except ImportError:
        from langchain.docstore.document import Document
        
from langchain_community.vectorstores import Qdrant

from src.utils.helpers import get_logger
from src.utils.config import (
    QDRANT_PATH,
    QDRANT_COLLECTION_NAME,
    QDRANT_HOST,
    QDRANT_PORT,
    QDRANT_API_KEY,
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
    Manages the vector database for automotive knowledge using Qdrant.
    """
    
    def __init__(
        self,
        persist_directory: str = QDRANT_PATH,
        rebuild: bool = False
    ):
        """
        Initialize the knowledge base.
        
        Args:
            persist_directory: Directory to store Qdrant database
            rebuild: If True, rebuild the database from scratch
        """
        self.persist_directory = persist_directory
        self.collection_name = QDRANT_COLLECTION_NAME
        
        # Lazy load embeddings (avoid loading PyTorch at startup)
        self._embeddings = None
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
        # Qdrant client will be created on demand
        self.client = None
        
        self.vectorstore = None  # Qdrant client store
        
        # Initialize or load the database
        if rebuild or not self._database_exists():
            logger.info("Building knowledge base from scratch...")
            self._build_database()
        else:
            logger.info("Loading existing knowledge base...")
            self._load_database()
    
    @property
    def embeddings(self):
        """Lazy load embeddings to avoid loading PyTorch at startup."""
        if self._embeddings is None:
            logger.info("Loading HuggingFace embeddings (all-MiniLM-L6-v2)...")
            self._embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': True}
            )
        return self._embeddings
    
    def _database_exists(self) -> bool:
        """Check if the Qdrant database already exists."""
        try:
            # Check if directory exists and has content
            if QDRANT_HOST:
                # For remote, we would need to check collections
                client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT, api_key=QDRANT_API_KEY)
                collections = client.get_collections().collections
                return any(c.name == self.collection_name for c in collections)
            else:
                # For local, check if directory exists
                db_path = Path(self.persist_directory)
                return db_path.exists() and any(db_path.iterdir())
        except Exception as e:
            logger.warning(f"Error checking for existing database: {e}")
            return False
    
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
        
        # Create vector store using Qdrant directly
        logger.info("Creating embeddings and building vector database...")
        logger.info("(This may take a few minutes on first run...)")
        
        # Initialize Qdrant client
        if QDRANT_HOST:
            self.client = QdrantClient(
                host=QDRANT_HOST,
                port=QDRANT_PORT,
                api_key=QDRANT_API_KEY
            )
        else:
            self.client = QdrantClient(path=self.persist_directory)
        
        # Get embeddings for all chunks
        logger.info("Computing embeddings for all chunks...")
        texts = [chunk.page_content for chunk in chunks]
        metadatas = [chunk.metadata for chunk in chunks]
        embeddings = self.embeddings.embed_documents(texts)
        
        # Create collection if it doesn't exist
        try:
            collection_info = self.client.get_collection(self.collection_name)
            logger.info(f"Collection {self.collection_name} already exists, recreating...")
            self.client.delete_collection(self.collection_name)
        except Exception:
            pass  # Collection doesn't exist yet
        
        # Create collection with proper vector size
        vector_size = len(embeddings[0]) if embeddings else 384
        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
        )
        
        # Upsert points to collection
        logger.info(f"Upserting {len(embeddings)} embeddings to collection...")
        
        points = []
        for idx, (embedding, text, metadata) in enumerate(zip(embeddings, texts, metadatas)):
            point = PointStruct(
                id=idx,
                vector=embedding,
                payload={
                    "page_content": text,
                    "source": metadata.get("source", "unknown"),
                    "page": metadata.get("page", 0),
                    **metadata  # Include all metadata
                }
            )
            points.append(point)
        
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )
        
        logger.info(f"✅ Knowledge base built and saved to Qdrant collection '{self.collection_name}'")
    
    def _load_database(self):
        """Load an existing vector database."""
        try:
            if QDRANT_HOST:
                self.client = QdrantClient(
                    host=QDRANT_HOST,
                    port=QDRANT_PORT,
                    api_key=QDRANT_API_KEY
                )
            else:
                self.client = QdrantClient(path=self.persist_directory)
            
            # Load vectorstore from existing collection
            self.vectorstore = Qdrant(
                client=self.client,
                collection_name=self.collection_name,
                embeddings=self.embeddings
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
        if not self.client:
            raise ValueError("Vector store not initialized")
        
        logger.info(f"Searching knowledge base for: '{query}'")
        
        # Embed the query
        query_embedding = self.embeddings.embed_query(query)
        
        # Search using Qdrant client's query method
        search_results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_embedding,
            limit=k
        )
        
        # Convert scored points to Document objects
        documents = []
        for point in search_results.points:
            # Extract ALL metadata from the payload
            payload = point.payload or {}
            page_content = payload.get("page_content", "")
            
            # Build metadata dictionary with all available fields
            metadata = {
                "score": point.score
            }
            
            # Add all fields from payload except page_content
            for key, value in payload.items():
                if key != "page_content":
                    metadata[key] = value
            
            # Ensure essential fields have defaults
            if "source" not in metadata:
                metadata["source"] = "unknown"
            if "page" not in metadata:
                metadata["page"] = 0
            
            doc = Document(
                page_content=page_content,
                metadata=metadata
            )
            documents.append(doc)
        
        logger.info(f"Found {len(documents)} relevant documents")
        return documents
    
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
    
    def get_vectorstore(self) -> QdrantClient:
        """Get the underlying Qdrant client."""
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
