"""
Configuration module for Mechanic Diagnostic Assistant.
Loads environment variables and provides centralized configuration.
"""

import os
from dotenv import load_dotenv
from pathlib import Path
# Project Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Load environment variables from .env file
load_dotenv(BASE_DIR / ".env")

# API Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-4")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Groq API (Alternative - FAST & FREE)
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

# LangSmith Monitoring Configuration
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2", "true")
LANGCHAIN_ENDPOINT = os.getenv("LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY", "")
LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT", "mechanic-diagnostic-assistant")

# Application Settings
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./chroma_db")

# Project Paths
DATA_DIR = BASE_DIR / "data"
KNOWLEDGE_BASE_DIR = DATA_DIR / "knowledge_base"
MOCK_DATA_DIR = DATA_DIR / "mock_data"

# Knowledge Base Files
OBD_CODES_PATH = KNOWLEDGE_BASE_DIR / "obd_codes.json"
SYMPTOMS_PATH = KNOWLEDGE_BASE_DIR / "common_symptoms.json"
REPAIR_GUIDES_PATH = KNOWLEDGE_BASE_DIR / "repair_guides.txt"
PDF_DOCS_PATH = KNOWLEDGE_BASE_DIR / "pdfs"

# Mock Data Files
PARTS_CATALOG_PATH = MOCK_DATA_DIR / "parts_catalog.json"
LABOR_RATES_PATH = MOCK_DATA_DIR / "labor_rates.json"

# RAG Configuration
EMBEDDING_MODEL = "text-embedding-3-small"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
TOP_K_RESULTS = 3

# Validation
def validate_config():
    """Validate that required configuration is present."""
    missing = []
    
    if not OPENROUTER_API_KEY:
        missing.append("OPENROUTER_API_KEY")
    if not OPENAI_API_KEY:
        missing.append("OPENAI_API_KEY")
    if not LANGCHAIN_API_KEY:
        missing.append("LANGCHAIN_API_KEY")
    
    if missing:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing)}. "
            f"Please check your .env file."
        )
    
    return True

def get_config_summary():
    """Get a summary of current configuration (for debugging)."""
    return {
        "openrouter_model": OPENROUTER_MODEL,
        "embedding_model": EMBEDDING_MODEL,
        "chroma_db_path": CHROMA_DB_PATH,
        "langchain_project": LANGCHAIN_PROJECT,
        "debug": DEBUG,
    }


if __name__ == "__main__":
    # Test configuration
    print("Configuration Summary:")
    print("-" * 50)
    for key, value in get_config_summary().items():
        print(f"{key}: {value}")
    
    try:
        validate_config()
        print("\n✅ All required configuration is present")
    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}")
