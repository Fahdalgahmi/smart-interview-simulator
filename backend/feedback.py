import json

import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2"


def _apply_length_score_cap(score: int, word_count: int) -> int:
    """Prevent extremely short answers from receiving inflated scores."""
    if word_count == 0:
        return 1
    if word_count <= 5:
        return min(score, 3)
    if word_count <= 10:
        return min(score, 4)
    if word_count <= 20:
        return min(score, 6)
    return score


def _fallback_sample_answer(role: str, question: str) -> str:
    """Return useful guidance when Ollama cannot produce a model answer."""
    return (
        f"For this {role} question, start with a direct definition or answer. "
        "Then explain the key idea in two or three clear points, describe when "
        "or why it is used, and finish with a short practical example. Make "
        f"sure every point directly addresses: {question}"
    )


def _generate_sample_answer(role: str, question: str) -> str:
    """Ask Ollama to repair a missing sample answer."""
    repair_prompt = f"""
You are helping a junior {role} candidate prepare for an interview.

Question:
{question}

Write one technically accurate model answer in 3 to 6 sentences. Be direct,
clear, and include a brief example when useful. Return only the answer text.
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": repair_prompt,
                "stream": False,
                "options": {"temperature": 0.2},
            },
            timeout=120,
        )
        response.raise_for_status()
        sample_answer = str(response.json().get("response", "")).strip()
        if sample_answer:
            return sample_answer
    except (
        requests.exceptions.RequestException,
        KeyError,
        TypeError,
        ValueError,
    ):
        pass

    return _fallback_sample_answer(role, question)


def evaluate_candidate_answer(
    role: str,
    question: str,
    answer: str
) -> dict:
    """
    Evaluate an interview answer using a local Ollama model.

    Args:
        role: The selected interview role.
        question: The interview question.
        answer: The candidate's submitted answer.

    Returns:
        A dictionary containing the score, strengths, improvements,
        overall feedback, sample answer, and word count.
    """
    cleaned_answer = answer.strip()
    word_count = len(cleaned_answer.split())

    prompt = f"""
You are an experienced technical interviewer evaluating a junior-level candidate.

Evaluate the candidate fairly, consistently, and objectively.

Scoring Rubric:
10 = Perfect answer. Technically correct, complete, exceptionally clear, includes an excellent practical example.
9 = Excellent answer. Correct, detailed, and only missing a tiny detail.
8 = Strong answer. Correct, clear, and mostly complete, but missing one useful detail or example.
7 = Good answer. Mostly correct with a few minor omissions.
6 = Acceptable answer. Generally correct but incomplete or lacking explanation.
5 = Basic understanding but several important concepts are missing.
4 = Partial understanding with significant missing information.
3 = Limited understanding with technical mistakes.
2 = Mostly incorrect, vague, or unrelated.
1 = Empty, meaningless, or completely incorrect.

Evaluate using these criteria:
1. Technical accuracy
2. Relevance to the question
3. Clarity
4. Completeness
5. Practical examples

Important Instructions:
- Judge the candidate at the junior level for the selected interview role.
- Do not award a high score for a correct phrase that lacks explanation.
- A technically correct but extremely short answer is still incomplete.
- Give credit for correct additional information.
- Only lower the score for genuine technical mistakes or missing concepts.
- Use the entire 1-10 scoring range.
- Score the answer that was actually written, not what the candidate may have meant.

Interview Role:
{role}

Interview Question:
{question}

Candidate Answer:
{cleaned_answer}

Return ONLY valid JSON using exactly this format:

{{
  "score": 1,
  "strengths": [
    "One specific strength"
  ],
  "improvements": [
    "One specific improvement"
  ],
  "overall_feedback": "A concise explanation of the score.",
  "sample_answer": "A stronger answer appropriate for a junior candidate."
}}

Rules:
- score must be an integer between 1 and 10
- strengths must be a JSON array of strings
- improvements must be a JSON array of strings
- overall_feedback must explain WHY the score was assigned
- sample_answer must be technically accurate
- Do not invent strengths
- Do not invent weaknesses
- If there are no meaningful strengths, return an empty list
- If there are no meaningful improvements, return an empty list
- If the answer contains 1-5 words, the score must not exceed 3
- If the answer contains 6-10 words, the score must not exceed 4
- If the answer contains 11-20 words, the score must not exceed 6
- If the answer is unrelated, the score must not exceed 2
- If the answer is empty, the score must be exactly 1
- Return ONLY the JSON object
- Strengths must quote or reference specific ideas from the candidate's answer
- Improvements must identify exactly what is missing, unclear, or inaccurate
- Do not say "add more detail" unless you name the specific detail
- Do not say "provide an example" if the candidate already included an example
- Do not repeat the question in the feedback
- Avoid generic feedback that could apply to any answer
- If the answer is already strong, provide one advanced improvement instead of inventing a basic weakness
- The sample answer should preserve the candidate's correct ideas and improve them
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "format": "json",
                "stream": False,
                "options": {
                    "temperature": 0.1,
                    "seed": 42
                }
            },
            timeout=120
        )

        response.raise_for_status()

        ollama_result = response.json()

        if "response" not in ollama_result:
            raise KeyError(
                "Ollama response did not contain a 'response' field."
            )

        feedback = json.loads(ollama_result["response"])

        if not isinstance(feedback, dict):
            raise ValueError(
                "Ollama returned an invalid feedback format."
            )

        score = int(feedback.get("score", 1))
        score = max(1, min(score, 10))

        score = _apply_length_score_cap(score, word_count)

        strengths = feedback.get("strengths", [])
        improvements = feedback.get("improvements", [])

        if not isinstance(strengths, list):
            strengths = []

        if not isinstance(improvements, list):
            improvements = []

        strengths = [
            str(item).strip()
            for item in strengths
            if str(item).strip()
        ]

        improvements = [
            str(item).strip()
            for item in improvements
            if str(item).strip()
        ]

        overall_feedback = str(
            feedback.get(
                "overall_feedback",
                "The answer was evaluated successfully."
            )
        ).strip()

        sample_answer = str(
            feedback.get(
                "sample_answer",
                ""
            )
        ).strip()

        if not sample_answer:
            sample_answer = _generate_sample_answer(role, question)

        return {
            "score": score,
            "word_count": word_count,
            "strengths": strengths,
            "improvements": improvements,
            "overall_feedback": overall_feedback,
            "sample_answer": sample_answer
        }

    except requests.exceptions.ConnectionError:
        print(
            "Ollama evaluation error: "
            "Could not connect to Ollama at localhost:11434."
        )

    except requests.exceptions.Timeout:
        print(
            "Ollama evaluation error: "
            "The model took too long to respond."
        )

    except requests.exceptions.HTTPError as error:
        print(f"Ollama HTTP error: {error}")

    except (
        requests.exceptions.RequestException,
        json.JSONDecodeError,
        KeyError,
        TypeError,
        ValueError
    ) as error:
        print(f"Ollama evaluation error: {error}")

    return {
        "score": 0,
        "word_count": word_count,
        "strengths": [],
        "improvements": [
            "AI feedback is temporarily unavailable."
        ],
        "overall_feedback": (
            "Your answer was saved, but the local AI evaluation "
            f"could not be completed. Your answer contained "
            f"{word_count} words."
        ),
        "sample_answer": _fallback_sample_answer(role, question)
    }
