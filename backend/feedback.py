import json

import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2"


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

Evaluate the candidate's answer using these criteria:
1. Technical accuracy
2. Relevance to the question
3. Clarity
4. Completeness
5. Use of examples

Interview role:
{role}

Interview question:
{question}

Candidate answer:
{cleaned_answer}

Return only valid JSON using exactly this structure:

{{
  "score": 1,
  "strengths": ["One specific strength"],
  "improvements": ["One specific area to improve"],
  "overall_feedback": "A concise evaluation of the answer.",
  "sample_answer": "A stronger example answer suitable for a junior candidate."
}}

Rules:
- score must be an integer from 1 to 10
- strengths must be a list of strings
- improvements must be a list of strings
- Be honest about weak, incomplete, incorrect, or unrelated answers
- Do not include markdown
- Do not include text outside the JSON object
- Do not invent strengths
- If there are no meaningful strengths, return an empty strengths list
- Improvements must be specific to the interview question
- The sample answer must be accurate, concise, and appropriate for a junior candidate
- If the answer has fewer than 5 words, the score must be between 1 and 2
- If the answer is unrelated to the question, the score must not be higher than 2
- If the answer is empty, the score must be 1
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
                    "temperature": 0.2
                }
            },
            timeout=120
        )

        response.raise_for_status()

        ollama_result = response.json()

        if "response" not in ollama_result:
            raise KeyError("Ollama response did not contain a 'response' field.")

        feedback = json.loads(ollama_result["response"])

        if not isinstance(feedback, dict):
            raise ValueError("Ollama returned an invalid feedback format.")

        score = int(feedback.get("score", 1))
        score = max(1, min(score, 10))

        if word_count == 0:
            score = 1
        elif word_count < 5:
            score = min(score, 2)

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
            feedback.get("sample_answer", "")
        ).strip()

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
            f"could not be completed. Your answer contained {word_count} words."
        ),
        "sample_answer": ""
    }