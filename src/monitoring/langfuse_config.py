"""
Langfuse monitoring configuration for the Mechanic Diagnostic Assistant.
Enables tracing and monitoring of all LangChain agent operations.
"""

import os
from src.utils.helpers import get_logger

logger = get_logger(__name__)


def setup_langfuse():
    """
    Configure Langfuse monitoring for the application.
    This should be called before initializing any LangChain components.
    """
    try:
        # Get Langfuse credentials from environment
        langfuse_secret = os.getenv("LANGFUSE_SECRET_KEY", "")
        langfuse_public = os.getenv("LANGFUSE_PUBLIC_KEY", "")
        langfuse_host = os.getenv("LANGFUSE_BASE_URL", "https://cloud.langfuse.com")
        
        if langfuse_secret and langfuse_public:
            # Set environment variables for Langfuse (v3.x uses env vars)
            os.environ["LANGFUSE_SECRET_KEY"] = langfuse_secret
            os.environ["LANGFUSE_PUBLIC_KEY"] = langfuse_public
            os.environ["LANGFUSE_HOST"] = langfuse_host
            
            # Initialize Langfuse callback handler for LangChain (v3.x)
            from langfuse.langchain import CallbackHandler
            
            # In v3.x, CallbackHandler reads from environment variables
            langfuse_handler = CallbackHandler()
            
            logger.info(f"✅ Langfuse tracing enabled")
            logger.info(f"   View traces at: {langfuse_host}")
            
            return {
                "enabled": True,
                "handler": langfuse_handler,
                "host": langfuse_host
            }
        else:
            logger.warning("⚠️  Langfuse credentials not found - tracing disabled")
            return {
                "enabled": False,
                "handler": None,
                "host": None
            }
    
    except ImportError as e:
        logger.warning(f"⚠️  Langfuse import error: {e}")
        return {
            "enabled": False,
            "handler": None,
            "host": None
        }
    except Exception as e:
        logger.error(f"❌ Error setting up Langfuse: {e}")
        return {
            "enabled": False,
            "handler": None,
            "host": None
        }


def get_langfuse_handler():
    """Get the Langfuse callback handler for LangChain."""
    config = setup_langfuse()
    return config.get("handler")


if __name__ == "__main__":
    # Test the setup
    print("Setting up Langfuse monitoring...")
    config = setup_langfuse()
    
    print("\nLangfuse Configuration:")
    print("-" * 50)
    for key, value in config.items():
        if key != "handler":  # Don't print handler object
            print(f"{key}: {value}")
    
    if config["enabled"]:
        print(f"\n✅ Langfuse ready!")
    else:
        print(f"\n⚠️  Langfuse not configured")
