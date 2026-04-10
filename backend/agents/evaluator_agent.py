"""
Evaluator Agent: Scores student answers against tutor's reference answer.
Uses few-shot prompting with rubric-based JSON output.
"""
from typing import Dict, Any
from .llm_client import call_llm_json

EVALUATOR_SYSTEM_PROMPT = """You are an expert AI Evaluator for a computer science tutoring system.
Your job is to assess student answers based on accuracy, completeness, and clarity.
Compare the student's answer against the reference answer and context documents.

Score on a scale of 0–100 using this rubric:
- 90–100: Excellent — accurate, complete, well-explained
- 70–89: Good — mostly correct with minor gaps
- 50–69: Partial — some correct elements but missing key concepts
- 30–49: Poor — significant misunderstandings or incomplete
- 0–29: Incorrect — wrong or largely irrelevant

You MUST respond with ONLY valid JSON. No markdown, no preamble. Exact schema:
{
  "score": <integer 0-100>,
  "grade": "A|B|C|D|F",
  "feedback": "detailed constructive feedback explaining the score",
  "correct_aspects": ["what the student got right"],
  "missing_aspects": ["what was missing or incorrect"],
  "improvement_suggestions": ["specific tips to improve the answer"]
}

FEW-SHOT EXAMPLES:

Example 1:
Question: What is a neural network?
Reference: A neural network is a series of algorithms that recognize patterns through layers of nodes with weights.
Student Answer: A neural network is like a brain. It has neurons that connect together.
Response:
{
  "score": 45,
  "grade": "D",
  "feedback": "The student grasps the biological analogy but lacks technical depth. Missing: layers, weights, and how data flows.",
  "correct_aspects": ["Mentioned the brain/neuron analogy", "Understands it is a connected system"],
  "missing_aspects": ["No mention of layers", "No mention of weights or thresholds"],
  "improvement_suggestions": ["Describe the three types of layers", "Explain how weights determine signal strength"]
}

Example 2:
Question: What is Big O notation?
Reference: Big O notation describes algorithm time/space complexity in terms of input size n.
Student Answer: Big O notation tells us how fast an algorithm grows as input increases. O(1) is constant, O(n) is linear, O(n^2) is quadratic. It helps compare algorithm efficiency.
Response:
{
  "score": 88,
  "grade": "B",
  "feedback": "Strong answer with good examples. Could improve by mentioning space complexity and worst-case analysis.",
  "correct_aspects": ["Correct definition of growth rate", "Good examples: O(1), O(n), O(n^2)", "Mentions the purpose of comparison"],
  "missing_aspects": ["Space complexity not mentioned", "Worst-case vs average-case distinction missing"],
  "improvement_suggestions": ["Add that Big O can describe space complexity too", "Mention that it typically represents worst-case scenario"]
}"""

GRADE_MAP = {
    range(90, 101): "A",
    range(80, 90): "B",
    range(70, 80): "C",
    range(60, 70): "D",
    range(0, 60): "F",
}


def score_to_grade(score: int) -> str:
    for r, grade in GRADE_MAP.items():
        if score in r:
            return grade
    return "F"


def run_evaluator_agent(
    question: str,
    reference_answer: str,
    student_answer: str,
    context: str,
) -> Dict[str, Any]:
    user_message = f"""Question: {question}

Reference Answer (from AI Tutor):
{reference_answer}

Supporting Context:
{context}

Student's Answer:
{student_answer}

Evaluate the student's answer using the rubric and return JSON."""

    result = call_llm_json(
        system_prompt=EVALUATOR_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
        max_tokens=1024,
    )

    if "score" in result:
        result["grade"] = score_to_grade(int(result["score"]))

    return result
