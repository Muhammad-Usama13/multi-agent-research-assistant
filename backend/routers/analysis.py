"""
Analysis Router
Accepts a query (topic) or doc_id (uploaded PDF) and runs the full multi-agent pipeline.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from agents.orchestrator import ResearchOrchestrator
from routers.upload import get_document

router = APIRouter()
orchestrator = ResearchOrchestrator()


class AnalysisRequest(BaseModel):
    query: Optional[str] = None          # topic-based search
    doc_id: Optional[str] = None         # uploaded PDF id
    mode: str = "full"                   # full | summary | critique


class AnalysisResponse(BaseModel):
    status: str
    query: str
    summary: dict
    reader_analysis: dict
    explanation: dict
    critique: dict
    report: str


@router.post("/run", response_model=AnalysisResponse)
async def run_analysis(request: AnalysisRequest):
    """Run the full multi-agent analysis pipeline."""
    if not request.query and not request.doc_id:
        raise HTTPException(
            status_code=400,
            detail="Provide either a 'query' (research topic) or 'doc_id' (uploaded PDF).",
        )

    try:
        # --- Determine text source ---
        if request.doc_id:
            doc = get_document(request.doc_id)
            paper_text = doc["full_text"]
            sections = doc["sections"]
            query = request.query or doc["filename"]
        else:
            # Search ArXiv and fetch top paper text
            from modules.search_module import SearchModule
            searcher = SearchModule()
            results = searcher.search(request.query, max_results=3)
            if not results:
                raise HTTPException(status_code=404, detail="No papers found for this query.")

            paper_text = results[0]["abstract"]
            sections = {"abstract": paper_text}
            query = request.query

        # --- Run multi-agent pipeline ---
        result = orchestrator.run(
            query=query,
            paper_text=paper_text,
            sections=sections,
            mode=request.mode,
        )

        return AnalysisResponse(
            status="success",
            query=query,
            summary=result["summary"],
            reader_analysis=result["reader"],
            explanation=result["explanation"],
            critique=result["critique"],
            report=result["report"],
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.get("/search")
async def search_papers(q: str, max_results: int = 5):
    """Search ArXiv for research papers by topic."""
    from modules.search_module import SearchModule
    try:
        searcher = SearchModule()
        results = searcher.search(q, max_results=max_results)
        return {"query": q, "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
