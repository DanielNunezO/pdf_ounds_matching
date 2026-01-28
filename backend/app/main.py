"""
FastAPI Application for PDF Bounds Matching

Provides REST API endpoints for PDF text extraction, entity extraction,
and text matching with bounds.
"""
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import tempfile
import os
from pathlib import Path

try:
    from .pdf_extractor import PDFExtractor
    from .llm_extractor import EntityExtractor
    from .strategy_factory import MatchingStrategyFactory
except ImportError:
    from pdf_extractor import PDFExtractor
    from llm_extractor import EntityExtractor
    from strategy_factory import MatchingStrategyFactory


app = FastAPI(
    title="PDF Bounds Matching API",
    description="API for extracting text from PDFs and matching entities with bounding boxes",
    version="1.0.0"
)

# CORS middleware for frontend access
# WARNING: In production, replace "*" with specific frontend URLs
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class EntityExtractionRequest(BaseModel):
    """Request model for entity extraction."""
    text: str = Field(..., description="Text to extract entities from")
    entity_types: Optional[List[str]] = Field(None, description="Types of entities to extract")


class MatchRequest(BaseModel):
    """Request model for matching entities."""
    entity: str = Field(..., description="Entity to match in PDF")
    strategy: str = Field("exact", description="Matching strategy (exact, fuzzy, contextual)")
    threshold: Optional[float] = Field(80.0, description="Threshold for fuzzy/contextual matching")
    context_window: Optional[int] = Field(3, description="Context window for contextual matching")


# Global storage for uploaded PDFs (in production, use proper storage)
pdf_storage: Dict[str, str] = {}


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "message": "PDF Bounds Matching API",
        "status": "running",
        "version": "1.0.0"
    }


@app.post("/api/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload a PDF file for processing.
    
    Args:
        file: PDF file to upload
        
    Returns:
        Dictionary with file_id for subsequent operations
    """
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    # Save file temporarily
    tmp_file = None
    try:
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        content = await file.read()
        tmp_file.write(content)
        tmp_file.close()
        tmp_path = tmp_file.name
        
        # Store path with generated ID
        file_id = Path(tmp_path).stem
        pdf_storage[file_id] = tmp_path
        
        return {
            "file_id": file_id,
            "filename": file.filename,
            "message": "PDF uploaded successfully"
        }
    except Exception as e:
        # Clean up temporary file if upload fails
        if tmp_file and os.path.exists(tmp_file.name):
            os.remove(tmp_file.name)
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")


@app.get("/api/extract-text/{file_id}")
async def extract_text(file_id: str):
    """
    Extract text with bounds from uploaded PDF.
    
    Args:
        file_id: ID of uploaded PDF file
        
    Returns:
        Dictionary with extracted text bounds
    """
    if file_id not in pdf_storage:
        raise HTTPException(status_code=404, detail="PDF file not found")
    
    pdf_path = pdf_storage[file_id]
    
    try:
        extractor = PDFExtractor(pdf_path)
        text_bounds = extractor.extract_text_with_bounds()
        full_text = extractor.extract_full_text()
        
        return {
            "file_id": file_id,
            "full_text": full_text,
            "text_bounds": [tb.to_dict() for tb in text_bounds],
            "total_words": len(text_bounds)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting text: {str(e)}")


@app.post("/api/extract-entities")
async def extract_entities(request: EntityExtractionRequest):
    """
    Extract entities from text using LLM.
    
    Args:
        request: Entity extraction request with text and optional entity types
        
    Returns:
        Dictionary with extracted entities
    """
    try:
        extractor = EntityExtractor()
        entities = extractor.extract_entities(request.text, request.entity_types)
        
        return {
            "entities": entities,
            "count": len(entities)
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting entities: {str(e)}")


@app.post("/api/extract-named-entities")
async def extract_named_entities(request: EntityExtractionRequest):
    """
    Extract categorized named entities from text using LLM.
    
    Args:
        request: Entity extraction request with text
        
    Returns:
        Dictionary with categorized entities
    """
    try:
        extractor = EntityExtractor()
        entities = extractor.extract_named_entities(request.text)
        
        return {
            "entities": entities,
            "total_count": sum(len(v) for v in entities.values())
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting entities: {str(e)}")


@app.post("/api/match/{file_id}")
async def match_entity(file_id: str, request: MatchRequest):
    """
    Match entity in PDF using specified strategy.
    
    Args:
        file_id: ID of uploaded PDF file
        request: Match request with entity and strategy details
        
    Returns:
        Dictionary with match results
    """
    if file_id not in pdf_storage:
        raise HTTPException(status_code=404, detail="PDF file not found")
    
    pdf_path = pdf_storage[file_id]
    
    try:
        # Extract text bounds
        extractor = PDFExtractor(pdf_path)
        text_bounds = extractor.extract_text_with_bounds()
        
        # Create matching strategy
        strategy = MatchingStrategyFactory.create_strategy(
            request.strategy,
            threshold=request.threshold,
            context_window=request.context_window
        )
        
        # Perform matching
        matches = strategy.match(request.entity, text_bounds)
        
        return {
            "file_id": file_id,
            "entity": request.entity,
            "strategy": request.strategy,
            "matches": [match.to_dict() for match in matches],
            "match_count": len(matches)
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error matching entity: {str(e)}")


@app.get("/api/strategies")
async def get_strategies():
    """
    Get available matching strategies.
    
    Returns:
        Dictionary with available strategies and their descriptions
    """
    return {
        "strategies": [
            {
                "name": "exact",
                "description": "Exact string matching",
                "parameters": []
            },
            {
                "name": "fuzzy",
                "description": "Fuzzy matching using Levenshtein distance",
                "parameters": [
                    {"name": "threshold", "type": "float", "default": 80.0, "description": "Minimum confidence score (0-100)"}
                ]
            },
            {
                "name": "contextual",
                "description": "Contextual matching considering surrounding text",
                "parameters": [
                    {"name": "threshold", "type": "float", "default": 70.0, "description": "Minimum confidence score (0-100)"},
                    {"name": "context_window", "type": "int", "default": 3, "description": "Number of surrounding words to consider"}
                ]
            }
        ]
    }


@app.delete("/api/cleanup/{file_id}")
async def cleanup_pdf(file_id: str):
    """
    Clean up uploaded PDF file.
    
    Args:
        file_id: ID of PDF file to remove
        
    Returns:
        Success message
    """
    if file_id not in pdf_storage:
        raise HTTPException(status_code=404, detail="PDF file not found")
    
    pdf_path = pdf_storage[file_id]
    
    try:
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
        del pdf_storage[file_id]
        
        return {"message": "PDF file cleaned up successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error cleaning up file: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    # Bind to localhost for security during development
    # In production, configure host/port via environment variables
    uvicorn.run(app, host="127.0.0.1", port=8000)
