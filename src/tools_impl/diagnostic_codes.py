"""
Tool 1: Search for OBD-II diagnostic code information.
"""

from typing import Dict, Optional
from src.utils.helpers import get_logger, load_json_file, search_dict_list
from src.utils.config import OBD_CODES_PATH

logger = get_logger(__name__)


def search_diagnostic_code(code: str) -> Dict:
    """
    Search for information about an OBD-II diagnostic code.
    
    Args:
        code: OBD-II code (e.g., "P0420", "P0300")
        
    Returns:
        Dictionary with code information including description, causes, and repair cost
    """
    logger.info(f"Searching for diagnostic code: {code}")
    
    # Normalize code (uppercase, remove spaces)
    code = code.upper().strip()
    
    try:
        # Load OBD codes database
        obd_data = load_json_file(OBD_CODES_PATH)
        
        # Search for the code
        result = search_dict_list(obd_data, "code", code, case_sensitive=False)
        
        if result:
            logger.info(f"Found code {code}")
            return {
                "found": True,
                "code": result["code"],
                "description": result["description"],
                "system": result["system"],
                "severity": result["severity"],
                "common_causes": result["common_causes"],
                "typical_repair_cost_min": result["typical_repair_cost_min"],
                "typical_repair_cost_max": result["typical_repair_cost_max"],
                "repair_time_hours_min": result["repair_time_hours_min"],
                "repair_time_hours_max": result["repair_time_hours_max"],
                "diagnostic_steps": result.get("diagnostic_steps", [])
            }
        else:
            # Fallback 1: Search in vector database (PDFs) for codes not in JSON
            logger.info(f"Code {code} not found in JSON, searching in vector database...")
            try:
                from src.rag.knowledge_base import KnowledgeBase
                kb = KnowledgeBase()
                search_results = kb.search(code, k=5)
                
                if search_results and len(search_results) > 0:
                    # Look for the code in the search results
                    found_in_document = False
                    description = ""
                    content = ""
                    metadata = {}
                    
                    for result in search_results:
                        result_content = result.page_content if hasattr(result, 'page_content') else result.get("content", "")
                        result_metadata = result.metadata if hasattr(result, 'metadata') else result.get("metadata", {})
                        
                        # Check if the code is explicitly mentioned in the document
                        if code.upper() in result_content.upper():
                            found_in_document = True
                            content = result_content
                            metadata = result_metadata
                            
                            # Extract the specific line containing the code
                            lines = result_content.split('\n')
                            for line in lines:
                                if code.upper() in line.upper():
                                    description = line.strip()
                                    break
                            
                            if not description and len(lines) > 0:
                                description = lines[0].strip()
                            
                            break
                    
                    if found_in_document:
                        logger.info(f"Found {code} explicitly in vector database")
                        return {
                            "found": True,
                            "code": code,
                            "description": description or f"Diagnostic code {code}",
                            "source": "PDF Documents",
                            "document": metadata.get("title", "Repair Manual") if isinstance(metadata, dict) else str(metadata),
                            "content_snippet": content[:500] if isinstance(content, str) else "",
                            "message": f"Code {code} found in repair documentation (not in primary database)"
                        }
            except Exception as e:
                logger.info(f"Vector database search failed ({str(e)[:50]}), trying direct PDF search...")
            
            # Fallback 2: Direct PDF file search
            logger.info(f"Attempting direct PDF search for {code}...")
            try:
                from pathlib import Path
                import os
                from src.utils.config import PDF_DOCS_PATH
                
                if PDF_DOCS_PATH and Path(PDF_DOCS_PATH).exists():
                    for pdf_file in Path(PDF_DOCS_PATH).glob("*.pdf"):
                        try:
                            from langchain_community.document_loaders import PyPDFLoader
                            loader = PyPDFLoader(str(pdf_file))
                            pages = loader.load()
                            
                            for page in pages:
                                page_content = page.page_content if hasattr(page, 'page_content') else str(page)
                                if code.upper() in page_content.upper():
                                    # Found the code in this PDF
                                    logger.info(f"Found {code} in PDF: {pdf_file.name}")
                                    
                                    # Extract the specific section
                                    lines = page_content.split('\n')
                                    description = ""
                                    for line in lines:
                                        if code.upper() in line.upper():
                                            description = line.strip()
                                            break
                                    
                                    return {
                                        "found": True,
                                        "code": code,
                                        "description": description or f"Diagnostic code {code}",
                                        "source": f"{pdf_file.name}",
                                        "document": pdf_file.name,
                                        "content_snippet": page_content[:500],
                                        "message": f"Code {code} found in {pdf_file.name}"
                                    }
                        except Exception as pdf_error:
                            logger.warning(f"Error reading {pdf_file}: {pdf_error}")
                            continue
            except Exception as e:
                logger.warning(f"Direct PDF search failed: {e}")
            
            # Code not found anywhere
            logger.warning(f"Code {code} not found in JSON, vector database, or PDFs")
            return {
                "found": False,
                "code": code,
                "message": f"Diagnostic code {code} not found in database or documentation. "
                          "This may be a manufacturer-specific code or a typo. "
                          "Please verify the code and try again."
            }
    
    except Exception as e:
        logger.error(f"Error searching for code {code}: {e}")
        return {
            "found": False,
            "code": code,
            "error": str(e)
        }


if __name__ == "__main__":
    # Test the tool
    print("Testing diagnostic code search tool...")
    print("-" * 50)
    
    # Test successful search
    result1 = search_diagnostic_code("P0420")
    print("\nTest 1: P0420")
    print(f"Found: {result1['found']}")
    if result1['found']:
        print(f"Description: {result1['description']}")
        print(f"Common causes: {len(result1['common_causes'])} listed")
    
    # Test code not found

    result2 = search_diagnostic_code("P9999")
    print("\nTest 2: P9999 (should not exist)")
    print(f"Found: {result2['found']}")
    print(f"Message: {result2.get('message', 'N/A')}")
    
    print("\n✅ Diagnostic code tool test completed")
