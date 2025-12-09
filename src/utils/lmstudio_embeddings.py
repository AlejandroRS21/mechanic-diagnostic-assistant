"""
LM Studio Embeddings Configuration
Local embeddings using LM Studio API compatible with OpenAI
"""

import os
from typing import List
import logging

logger = logging.getLogger(__name__)

try:
    from openai import OpenAI
except ImportError:
    logger.warning("openai package not installed. Install with: pip install openai")
    OpenAI = None


class LMStudioEmbeddings:
    """
    Embeddings provider using LM Studio locally
    
    Features:
    - 100% local (no internet required)
    - Free (no API costs)
    - Private (data stays on your machine)
    - Compatible with OpenAI API
    
    Requirements:
    1. Download LM Studio from https://lmstudio.ai
    2. Download embedding model (e.g., nomic-embed-text)
    3. Start Local Server in LM Studio
    4. Configure .env with LMSTUDIO_BASE_URL
    """
    
    def __init__(
        self,
        base_url: str = None,
        model: str = None,
        api_key: str = "not-needed"
    ):
        """
        Initialize LM Studio embeddings
        
        Args:
            base_url: LM Studio API endpoint (default: http://localhost:8000)
            model: Embedding model name (default: nomic-embed-text)
            api_key: API key (not needed for local LM Studio)
        """
        if OpenAI is None:
            raise ImportError(
                "openai package required. Install with: pip install openai"
            )
        
        self.base_url = base_url or os.getenv(
            "LMSTUDIO_BASE_URL",
            "http://localhost:8000"
        )
        
        self.model = model or os.getenv(
            "LMSTUDIO_EMBEDDING_MODEL",
            "nomic-embed-text"
        )
        
        self.api_key = api_key or os.getenv("LMSTUDIO_API_KEY", "not-needed")
        
        # Initialize OpenAI client pointing to LM Studio
        self.client = OpenAI(
            base_url=f"{self.base_url}/v1",
            api_key=self.api_key
        )
        
        # Verify connection
        self._verify_connection()
    
    def _verify_connection(self):
        """Verify LM Studio is running and accessible"""
        try:
            logger.info(f"Connecting to LM Studio at {self.base_url}...")
            
            # Try to list available models
            models = self.client.models.list()
            
            logger.info(f"✅ Connected to LM Studio")
            logger.info(f"   Base URL: {self.base_url}")
            logger.info(f"   Model: {self.model}")
            logger.info(f"   Available models: {len(list(models))}")
            
        except Exception as e:
            error_msg = (
                f"❌ Cannot connect to LM Studio\n"
                f"   Base URL: {self.base_url}\n"
                f"   Error: {str(e)}\n\n"
                f"Solutions:\n"
                f"1. Download LM Studio from https://lmstudio.ai\n"
                f"2. Download an embedding model (e.g., nomic-embed-text)\n"
                f"3. Go to 'Local Server' tab\n"
                f"4. Select your embedding model\n"
                f"5. Click 'Start Server'\n"
                f"6. Wait for 'Ready to accept connections' message"
            )
            logger.error(error_msg)
            raise ConnectionError(error_msg)
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of documents
        
        Args:
            texts: List of text strings to embed
            
        Returns:
            List of embedding vectors (each is a list of floats)
        """
        try:
            logger.debug(f"Embedding {len(texts)} documents...")
            
            embeddings = []
            for i, text in enumerate(texts):
                try:
                    # Create embedding via OpenAI API (compatible interface)
                    response = self.client.embeddings.create(
                        model=self.model,
                        input=text
                    )
                    
                    embedding = response.data[0].embedding
                    embeddings.append(embedding)
                    
                    if (i + 1) % 10 == 0:
                        logger.debug(f"  Embedded {i + 1}/{len(texts)} documents")
                
                except Exception as e:
                    logger.error(f"Error embedding text {i}: {e}")
                    raise
            
            logger.debug(f"✅ Generated {len(embeddings)} embeddings")
            return embeddings
        
        except Exception as e:
            logger.error(f"Error in embed_documents: {e}")
            raise
    
    def embed_query(self, text: str) -> List[float]:
        """
        Generate embedding for a query
        
        Args:
            text: Query text to embed
            
        Returns:
            Embedding vector (list of floats)
        """
        try:
            logger.debug(f"Embedding query: {text[:50]}...")
            
            response = self.client.embeddings.create(
                model=self.model,
                input=text
            )
            
            embedding = response.data[0].embedding
            logger.debug(f"✅ Generated query embedding (dim={len(embedding)})")
            
            return embedding
        
        except Exception as e:
            logger.error(f"Error in embed_query: {e}")
            raise
    
    @property
    def embedding_dim(self) -> int:
        """Get dimension of embeddings"""
        # Most embedding models have fixed dimensions
        # nomic-embed-text: 768
        # all-miniLM-L6-v2: 384
        # Default to 768 if unknown
        model_dims = {
            "nomic-embed-text": 768,
            "all-miniLM-L6-v2": 384,
            "bge-small-en-v1.5": 384,
        }
        return model_dims.get(self.model, 768)


# Example usage and testing
if __name__ == "__main__":
    import logging
    
    # Setup logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger = logging.getLogger(__name__)
    
    try:
        # Initialize embeddings
        print("\n🧪 Testing LM Studio Embeddings\n")
        embeddings = LMStudioEmbeddings()
        
        # Test 1: Single embedding
        print("📝 Test 1: Single embedding")
        text = "P0258 is a diagnostic code for fuel injection"
        embedding = embeddings.embed_query(text)
        print(f"   Text: {text}")
        print(f"   Embedding dimension: {len(embedding)}")
        print(f"   First 3 values: {embedding[:3]}\n")
        
        # Test 2: Multiple embeddings
        print("📝 Test 2: Multiple embeddings")
        texts = [
            "P0420 Catalyst System Efficiency Below Threshold",
            "P0300 Random Misfire Detected",
            "P0171 System Too Lean"
        ]
        embeddings_list = embeddings.embed_documents(texts)
        print(f"   Generated {len(embeddings_list)} embeddings")
        print(f"   Each with dimension: {len(embeddings_list[0])}\n")
        
        # Test 3: Similarity calculation
        print("📝 Test 3: Similarity between embeddings")
        import numpy as np
        
        def cosine_similarity(a, b):
            return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
        
        sim = cosine_similarity(embeddings_list[0], embeddings_list[1])
        print(f"   Similarity between 'P0420' and 'P0300': {sim:.4f}\n")
        
        print("✅ All tests passed!\n")
        
    except Exception as e:
        print(f"❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
