"""
Orchestrator: Coordinates the full RAG → Tutor → Evaluator → HIL pipeline.
Manages session state and inter-agent communication.
"""
import uuid
import time
from typing import Dict, Any, Optional
from datetime import datetime, timezone

from ..rag.engine import search, format_context
from .tutor_agent import run_tutor_agent
from .evaluator_agent import run_evaluator_agent, score_to_grade

# In-memory session store (replace with Redis/DB in production)
_sessions: Dict[str, Dict[str, Any]] = {}


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _log_event(session: Dict[str, Any], event: str, data: Any = None):
    session["audit_log"].append({
        "timestamp": _utc_now(),
        "event": event,
        "data": data,
    })


def get_session(session_id: str) -> Optional[Dict[str, Any]]:
    return _sessions.get(session_id)


def list_sessions() -> list:
    return [
        {
            "session_id": sid,
            "status": s["status"],
            "question": s["question"],
            "created_at": s["created_at"],
            "ai_score": s["evaluator_response"]["score"] if s.get("evaluator_response") else None,
            "final_score": s["final_output"]["evaluation"]["final_score"] if s.get("final_output") else None,
            "human_override": s["final_output"]["evaluation"]["human_override"] if s.get("final_output") else None,
        }
        for sid, s in _sessions.items()
    ]


def orchestrate_ask(question: str) -> Dict[str, Any]:
    session_id = str(uuid.uuid4())
    session = {
        "session_id": session_id,
        "created_at": _utc_now(),
        "status": "processing_rag",
        "question": question,
        "rag_context": None,
        "rag_sources": [],
        "tutor_response": None,
        "student_answer": None,
        "evaluator_response": None,
        "human_review": None,
        "final_output": None,
        "audit_log": [],
    }
    _sessions[session_id] = session
    _log_event(session, "question_received", {"question": question})

    # RAG retrieval
    t0 = time.time()
    sources = search(question, top_k=3)
    context = format_context(sources)
    _log_event(session, "rag_retrieved", {
        "num_chunks": len(sources),
        "retrieval_time_s": round(time.time() - t0, 3),
        "sources": [s["title"] for s in sources],
    })

    # Tutor Agent
    session["status"] = "tutor_generating"
    session["rag_context"] = context
    session["rag_sources"] = sources
    t0 = time.time()
    tutor_response = run_tutor_agent(question, context, sources)
    _log_event(session, "tutor_completed", {
        "difficulty_level": tutor_response.get("difficulty_level"),
        "generation_time_s": round(time.time() - t0, 3),
    })

    session["tutor_response"] = tutor_response
    session["status"] = "awaiting_student_answer"

    return {
        "session_id": session_id,
        "question": question,
        "ai_answer": tutor_response.get("answer"),
        "key_concepts": tutor_response.get("key_concepts", []),
        "difficulty_level": tutor_response.get("difficulty_level"),
        "suggested_followups": tutor_response.get("suggested_followups", []),
        "sources": tutor_response.get("sources_used", []),
        "status": session["status"],
    }


def orchestrate_answer(session_id: str, student_answer: str) -> Dict[str, Any]:
    session = get_session(session_id)
    if not session:
        raise ValueError(f"Session {session_id} not found.")
    if session["status"] != "awaiting_student_answer":
        raise ValueError(f"Session is in state '{session['status']}', expected 'awaiting_student_answer'.")

    session["student_answer"] = student_answer
    session["status"] = "evaluating"
    _log_event(session, "student_answer_received", {"answer_length": len(student_answer)})

    t0 = time.time()
    evaluator_response = run_evaluator_agent(
        question=session["question"],
        reference_answer=session["tutor_response"]["answer"],
        student_answer=student_answer,
        context=session["rag_context"],
    )
    _log_event(session, "evaluation_completed", {
        "ai_score": evaluator_response.get("score"),
        "ai_grade": evaluator_response.get("grade"),
        "evaluation_time_s": round(time.time() - t0, 3),
    })

    session["evaluator_response"] = evaluator_response
    session["status"] = "awaiting_human_review"

    return {
        "session_id": session_id,
        "question": session["question"],
        "student_answer": student_answer,
        "ai_evaluation": {
            "score": evaluator_response.get("score"),
            "grade": evaluator_response.get("grade"),
            "feedback": evaluator_response.get("feedback"),
            "correct_aspects": evaluator_response.get("correct_aspects", []),
            "missing_aspects": evaluator_response.get("missing_aspects", []),
            "improvement_suggestions": evaluator_response.get("improvement_suggestions", []),
        },
        "status": session["status"],
        "message": "Evaluation complete. Submit to /review for human override or approval.",
    }


def orchestrate_review(
    session_id: str,
    reviewer_name: str,
    approved: bool,
    override_score: Optional[int] = None,
    override_feedback: Optional[str] = None,
) -> Dict[str, Any]:
    session = get_session(session_id)
    if not session:
        raise ValueError(f"Session {session_id} not found.")
    if session["status"] != "awaiting_human_review":
        raise ValueError(f"Session is in state '{session['status']}', expected 'awaiting_human_review'.")

    ai_score = session["evaluator_response"].get("score")
    ai_feedback = session["evaluator_response"].get("feedback")
    ai_grade = session["evaluator_response"].get("grade")

    final_score = override_score if (not approved and override_score is not None) else ai_score
    final_feedback = override_feedback if (not approved and override_feedback) else ai_feedback
    final_grade = score_to_grade(int(final_score))

    human_review = {
        "reviewer": reviewer_name,
        "reviewed_at": _utc_now(),
        "approved": approved,
        "override_score": override_score,
        "override_feedback": override_feedback,
    }
    session["human_review"] = human_review

    _log_event(session, "human_review_completed", {
        "reviewer": reviewer_name,
        "approved": approved,
        "ai_score": ai_score,
        "final_score": final_score,
        "overridden": not approved,
    })

    final_output = {
        "session_id": session_id,
        "question": session["question"],
        "ai_answer": session["tutor_response"]["answer"],
        "key_concepts": session["tutor_response"].get("key_concepts", []),
        "difficulty_level": session["tutor_response"].get("difficulty_level"),
        "student_answer": session["student_answer"],
        "sources": session["tutor_response"].get("sources_used", []),
        "evaluation": {
            "ai_score": ai_score,
            "ai_grade": ai_grade,
            "ai_feedback": ai_feedback,
            "final_score": final_score,
            "final_grade": final_grade,
            "final_feedback": final_feedback,
            "human_override": not approved,
            "reviewer": reviewer_name,
            "reviewed_at": human_review["reviewed_at"],
        },
        "audit_log": session["audit_log"],
        "status": "completed",
    }

    session["final_output"] = final_output
    session["status"] = "completed"
    return final_output
