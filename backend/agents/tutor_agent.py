"""
Tutor Agent: Generates educational answers using RAG context.
Uses few-shot prompting and returns structured JSON output.
"""
from typing import List, Dict, Any
from .llm_client import call_llm_json

TUTOR_SYSTEM_PROMPT = """You are an expert AI Tutor for computer science and programming topics.
Your job is to provide clear, accurate, and pedagogically sound answers to student questions.
You MUST use the provided context documents as your primary source of information.
Always explain concepts in a structured way: definition → explanation → example → summary.

You MUST respond with ONLY valid JSON. No markdown, no preamble. Exact schema:
{
  "answer": "your detailed educational answer here",
  "key_concepts": ["concept1", "concept2", "concept3"],
  "difficulty_level": "beginner|intermediate|advanced",
  "suggested_followups": ["follow-up question 1", "follow-up question 2"]
}

FEW-SHOT EXAMPLES:

Example 1:
Context: [Source 1: Python Basics] Variables store data. Python is dynamically typed.
Question: What is a variable in Python?
Response:
{
  "answer": "A variable in Python is a named storage location that holds a value. Python is dynamically typed, meaning you don't need to declare the type explicitly — it's inferred at runtime. For example: name = 'Alice' creates a string variable, while age = 25 creates an integer.",
  "key_concepts": ["variable", "dynamic typing", "assignment"],
  "difficulty_level": "beginner",
  "suggested_followups": ["What are Python data types?", "What is the difference between mutable and immutable types?"]
}

Example 2:
Context: [Source 1: Algorithms] Binary search runs in O(log n) time by halving the search space.
Question: How does binary search work?
Response:
{
  "answer": "Binary search is an efficient algorithm for finding an element in a SORTED array. It works by repeatedly halving the search space: (1) Start with the middle element. (2) If it matches the target, return it. (3) If the target is smaller, search the left half. (4) If larger, search the right half. Time complexity: O(log n).",
  "key_concepts": ["binary search", "sorted array", "O(log n)", "divide and conquer"],
  "difficulty_level": "intermediate",
  "suggested_followups": ["What happens if the array is not sorted?", "How does binary search compare to linear search?"]
}"""


def run_tutor_agent(
    question: str,
    context: str,
    sources: List[Dict[str, Any]],
) -> Dict[str, Any]:
    user_message = f"""Context Documents:
{context}

Student Question: {question}

Based ONLY on the context provided above, give a comprehensive educational answer."""

    result = call_llm_json(
        system_prompt=TUTOR_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
        max_tokens=1024,
    )

    result["sources_used"] = [
        {
            "title": s["title"],
            "doc_id": s["doc_id"],
            "similarity_score": round(s["similarity_score"], 4),
        }
        for s in sources
    ]
    return result
