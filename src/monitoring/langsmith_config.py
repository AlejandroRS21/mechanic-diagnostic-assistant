"""
LangSmith monitoring configuration for the Mechanic Diagnostic Assistant.
Enables tracing and monitoring of all LangChain agent operations.
"""

import os
from src.utils.helpers import get_logger

logger = get_logger(__name__)


def setup_langsmith():
    """
    Configure LangSmith monitoring for the application.
    This should be called before initializing any LangChain components.
    """
    from src.utils.config import (
        LANGCHAIN_TRACING_V2,
        LANGCHAIN_ENDPOINT,
        LANGCHAIN_API_KEY,
        LANGCHAIN_PROJECT
    )
    
    # Set environment variables for LangSmith
    os.environ["LANGCHAIN_TRACING_V2"] = LANGCHAIN_TRACING_V2
    os.environ["LANGCHAIN_ENDPOINT"] = LANGCHAIN_ENDPOINT
    os.environ["LANGCHAIN_API_KEY"] = LANGCHAIN_API_KEY
    os.environ["LANGCHAIN_PROJECT"] = LANGCHAIN_PROJECT
    
    if LANGCHAIN_TRACING_V2.lower() == "true" and LANGCHAIN_API_KEY:
        logger.info(f"✅ LangSmith tracing enabled for project: {LANGCHAIN_PROJECT}")
        logger.info(f"   View traces at: https://smith.langchain.com/")
    else:
        logger.warning("⚠️  LangSmith tracing is disabled or API key not set")
    
    return {
        "enabled": LANGCHAIN_TRACING_V2.lower() == "true",
        "project": LANGCHAIN_PROJECT,
        "endpoint": LANGCHAIN_ENDPOINT
    }


def get_langsmith_url(run_id: str = None) -> str:
    """
    Generate a LangSmith URL for viewing traces.
    
    Args:
        run_id: Optional specific run ID to link to
        
    Returns:
        URL to LangSmith dashboard
    """
    from src.utils.config import LANGCHAIN_PROJECT
    
    base_url = "https://smith.langchain.com/"
    
    if run_id:
        return f"{base_url}public/{LANGCHAIN_PROJECT}/r/{run_id}"
    else:
        return f"{base_url}o/default/projects/p/{LANGCHAIN_PROJECT}"


if __name__ == "__main__":
    # Test the setup
    print("Setting up LangSmith monitoring...")
    config = setup_langsmith()
    
    print("\nLangSmith Configuration:")
    print("-" * 50)
    for key, value in config.items():
        print(f"{key}: {value}")
    
    print(f"\nDashboard URL: {get_langsmith_url()}")
