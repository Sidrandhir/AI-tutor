"""
AI Tutor + Evaluator System — FastAPI Application
Endpoints: POST /ask | POST /answer | POST /review | GET /sessions | GET /session/{id}
"""
import os
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# ✅ FIXED: correct relative imports (..agents, ..rag, ..data — one level up from api/)
from ..agents.orchestrator import (
    orchestrate_ask,
    orchestrate_answer,
    orchestrate_review,
    list_sessions,
    get_session,
)
from ..rag.engine import build_index
from ..data.docs import SAMPLE_DOCUMENTS


# ─── Lifespan ────────────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("[Startup] Building RAG index...")
    build_index(SAMPLE_DOCUMENTS)
    print(f"[Startup] Indexed {len(SAMPLE_DOCUMENTS)} documents. Ready.")
    yield
    print("[Shutdown] Goodbye.")


# ─── App ─────────────────────────────────────────────────────────────────────

app = FastAPI(
    title="AI Tutor + Evaluator",
    description="""
    A production-grade AI tutoring system with RAG, multi-agent orchestration,
    and Human-in-the-Loop (HIL) review.

    **Flow:** Student Question → RAG Retrieval → Tutor Agent → Student Answer → Evaluator Agent → Human Review → Final Output
    """,
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Request / Response Models ────────────────────────────────────────────────

class AskRequest(BaseModel):
    question: str = Field(..., min_length=5, description="Student's question")


class AnswerRequest(BaseModel):
    session_id: str = Field(..., description="Session ID from /ask response")
    student_answer: str = Field(..., min_length=5, description="Student's answer")


class ReviewRequest(BaseModel):
    session_id: str = Field(..., description="Session ID from /answer response")
    reviewer_name: str = Field(..., description="Name of the human reviewer")
    approved: bool = Field(..., description="True = approve AI evaluation, False = override")
    override_score: Optional[int] = Field(None, ge=0, le=100, description="Override score (0-100)")
    override_feedback: Optional[str] = Field(None, description="Override feedback text")


# ─── Endpoints ────────────────────────────────────────────────────────────────

@app.get("/", tags=["Health"])
def root():
    return {
        "status": "ok",
        "service": "AI Tutor + Evaluator",
        "endpoints": [
            "POST /ask — Ask a question",
            "POST /answer — Submit student answer for evaluation",
            "POST /review — Human reviewer approves or overrides",
            "GET /sessions — List all sessions",
            "GET /session/{session_id} — Get full session details",
        ],
    }


@app.post("/ask", tags=["Flow"], summary="Step 1: Ask a question")
def ask(req: AskRequest):
    try:
        return orchestrate_ask(req.question)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/answer", tags=["Flow"], summary="Step 2: Submit student answer")
def answer(req: AnswerRequest):
    try:
        return orchestrate_answer(req.session_id, req.student_answer)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/review", tags=["Flow"], summary="Step 3: Human review & HIL override")
def review(req: ReviewRequest):
    if not req.approved and req.override_score is None:
        raise HTTPException(
            status_code=400,
            detail="override_score is required when approved=false"
        )
    try:
        return orchestrate_review(
            session_id=req.session_id,
            reviewer_name=req.reviewer_name,
            approved=req.approved,
            override_score=req.override_score,
            override_feedback=req.override_feedback,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/sessions", tags=["Admin"], summary="List all sessions")
def sessions():
    all_sessions = list_sessions()
    return {"sessions": all_sessions, "count": len(all_sessions)}


@app.get("/session/{session_id}", tags=["Admin"], summary="Get full session details")
def session_detail(session_id: str):
    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail=f"Session {session_id} not found.")
    return session
