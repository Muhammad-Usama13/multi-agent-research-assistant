"""
Upload Router
Handles PDF file uploads and stores extracted text for analysis.
"""
import os
import uuid
import tempfile

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

from modules.document_processor import DocumentProcessor

router = APIRouter()
processor = DocumentProcessor()

# In-memory store: {doc_id: {text, sections, filename}}
DOCUMENT_STORE: dict[str, dict] = {}


@router.post("/pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """Upload a PDF research paper and extract its text and sections."""
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    try:
        contents = await file.read()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(contents)
            tmp_path = tmp.name

        extracted = processor.process_pdf(tmp_path)
        os.unlink(tmp_path)

        doc_id = str(uuid.uuid4())
        DOCUMENT_STORE[doc_id] = {
            "filename": file.filename,
            "full_text": extracted["full_text"],
            "sections": extracted["sections"],
        }

        return JSONResponse({
            "doc_id": doc_id,
            "filename": file.filename,
            "pages": extracted.get("pages", 0),
            "sections_found": list(extracted["sections"].keys()),
            "preview": extracted["full_text"][:500] + "...",
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {str(e)}")


def get_document(doc_id: str) -> dict:
    """Retrieve a stored document by ID (used by analysis router)."""
    if doc_id not in DOCUMENT_STORE:
        raise HTTPException(status_code=404, detail="Document not found. Please upload again.")
    return DOCUMENT_STORE[doc_id]
