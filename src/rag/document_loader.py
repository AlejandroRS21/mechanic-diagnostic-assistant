"""
Document loader for the knowledge base.
Loads and processes documents from various sources (JSON, TXT).
"""

import json
from typing import List

try:
    from langchain.schema import Document
except ImportError:
    try:
        from langchain_core.documents import Document
    except ImportError:
        from langchain.docstore.document import Document
        
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader

from src.utils.helpers import get_logger, load_json_file, load_text_file

logger = get_logger(__name__)


def load_obd_codes(file_path: Path) -> List[Document]:
    """
    Load OBD-II codes from JSON file and convert to LangChain Documents.
    
    Args:
        file_path: Path to obd_codes.json
        
    Returns:
        List of Document objects
    """
    logger.info("Loading OBD codes...")
    
    obd_data = load_json_file(file_path)
    documents = []
    
    for code_info in obd_data:
        # Create a comprehensive text representation
        content = f"""
OBD-II Code: {code_info['code']}
Description: {code_info['description']}
System: {code_info['system']}
Severity: {code_info['severity']}

Common Causes:
{chr(10).join(f"- {cause}" for cause in code_info['common_causes'])}

Typical Repair Cost: ${code_info['typical_repair_cost_min']}-${code_info['typical_repair_cost_max']}
Repair Time: {code_info['repair_time_hours_min']}-{code_info['repair_time_hours_max']} hours

Diagnostic Steps:
{chr(10).join(f"{i+1}. {step}" for i, step in enumerate(code_info['diagnostic_steps']))}
"""
        
        # Create metadata for better retrieval
        metadata = {
            "source": "obd_codes",
            "code": code_info['code'],
            "system": code_info['system'],
            "severity": code_info['severity'],
            "type": "diagnostic_code"
        }
        
        documents.append(Document(page_content=content.strip(), metadata=metadata))
    
    logger.info(f"Loaded {len(documents)} OBD code documents")
    return documents


def load_symptoms(file_path: Path) -> List[Document]:
    """
    Load common symptoms from JSON file and convert to LangChain Documents.
    
    Args:
        file_path: Path to common_symptoms.json
        
    Returns:
        List of Document objects
    """
    logger.info("Loading common symptoms...")
    
    symptoms_data = load_json_file(file_path)
    documents = []
    
    for symptom_info in symptoms_data:
        # Create text representation
        content = f"""
Symptom: {symptom_info['symptom']}
Category: {symptom_info['category']}
Severity: {symptom_info['severity']}

Possible Causes (with probability):
{chr(10).join(f"- {cause['cause']} ({cause['probability']}% probability)" 
              for cause in symptom_info['possible_causes'])}

Diagnostic Questions to Ask:
{chr(10).join(f"- {q}" for q in symptom_info['diagnostic_questions'])}
"""
        
        metadata = {
            "source": "symptoms",
            "symptom": symptom_info['symptom'],
            "category": symptom_info['category'],
            "severity": symptom_info['severity'],
            "type": "symptom_diagnosis"
        }
        
        documents.append(Document(page_content=content.strip(), metadata=metadata))
    
    logger.info(f"Loaded {len(documents)} symptom documents")
    return documents


def load_repair_guides(file_path: Path) -> List[Document]:
    """
    Load repair guides from text file and convert to LangChain Documents.
    
    Args:
        file_path: Path to repair_guides.txt
        
    Returns:
        List of Document objects
    """
    logger.info("Loading repair guides...")
    
    content = load_text_file(file_path)
    
    # Split by repair sections (marked by ===)
    sections = content.split('===')
    documents = []
    
    for section in sections:
        section = section.strip()
        if not section:
            continue
        
        # Extract repair name from first line
        lines = section.split('\n')
        repair_name = lines[0].strip() if lines else "Unknown Repair"
        
        metadata = {
            "source": "repair_guides",
            "repair_name": repair_name,
            "type": "repair_procedure"
        }
        
        documents.append(Document(page_content=section, metadata=metadata))
    
    logger.info(f"Loaded {len(documents)} repair guide documents")
    return documents


def load_pdfs(directory_path: Path) -> List[Document]:
    """
    Load all PDF documents from a directory.
    
    Args:
        directory_path: Path to directory containing PDFs
        
    Returns:
        List of Document objects
    """
    if not directory_path.exists():
        logger.warning(f"PDF directory not found: {directory_path}")
        return []
        
    logger.info(f"Loading PDFs from {directory_path}...")
    
    documents = []
    pdf_files = list(directory_path.glob("*.pdf"))
    
    for pdf_file in pdf_files:
        try:
            loader = PyPDFLoader(str(pdf_file))
            docs = loader.load()
            
            # Add metadata
            for doc in docs:
                doc.metadata["source"] = "pdf_manual"
                doc.metadata["filename"] = pdf_file.name
                doc.metadata["type"] = "manual"
                
            documents.extend(docs)
            logger.info(f"Loaded {pdf_file.name}: {len(docs)} pages")
            
        except Exception as e:
            logger.error(f"Failed to load {pdf_file.name}: {e}")
            
    logger.info(f"Total PDF pages loaded: {len(documents)}")
    return documents


def load_all_knowledge_base(
    obd_codes_path: Path,
    symptoms_path: Path,
    repair_guides_path: Path,
    pdf_docs_path: Path = None
) -> List[Document]:
    """
    Load all knowledge base documents.
    
    Args:
        obd_codes_path: Path to OBD codes JSON
        symptoms_path: Path to symptoms JSON
        repair_guides_path: Path to repair guides TXT
        pdf_docs_path: Optional path to directory containing PDFs
        
    Returns:
        Combined list of all documents
    """
    logger.info("Loading complete knowledge base...")
    
    all_documents = []
    
    # Load each source
    all_documents.extend(load_obd_codes(obd_codes_path))
    all_documents.extend(load_symptoms(symptoms_path))
    all_documents.extend(load_repair_guides(repair_guides_path))
    
    if pdf_docs_path:
        all_documents.extend(load_pdfs(pdf_docs_path))
    
    logger.info(f"Total documents loaded: {len(all_documents)}")
    
    return all_documents


if __name__ == "__main__":
    # Test document loading
    from src.utils.config import (
        OBD_CODES_PATH,
        SYMPTOMS_PATH,
        REPAIR_GUIDES_PATH
    )
    
    print("Testing document loader...")
    print("-" * 50)
    
    docs = load_all_knowledge_base(
        OBD_CODES_PATH,
        SYMPTOMS_PATH,
        REPAIR_GUIDES_PATH
    )
    
    print(f"\n✅ Successfully loaded {len(docs)} documents")
    print("\nSample document:")
    print(docs[0].page_content[:200])
    print(f"\nMetadata: {docs[0].metadata}")
