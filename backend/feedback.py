import json
import os

from google import genai


def evaluate_candidate_answer(
    role: str,
    question: str,
    answer: str
) -> dict:
    """
    Evaluate an interview answer using Google Gemini.
    """

    cleaned_answer = answer.strip()
    word_count = len(cleaned_answer.split())

    if not cleaned_answer:
        return {
            "score": 0,
            "strengths": [],
            "improvements": ["Provide an answer before submitting."],
            "overall_feedback": "No answer was provided.",
            "sample_answer": "",
            "word_count": 0
        }

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not set. Set it in PowerShell before starting the server."
        )

    client = genai.Client(api_key=api_key)

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
  "improvements": ["One specific improvement"],
  "overall_feedback": "A concise evaluation of the answer",
  "sample_answer": "A stronger example answer"
}}

The score must be an integer from 1 to 10.

Do not include Markdown.
Do not include ```json.
Return only the JSON object.
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        response_text = response.text.strip()

        if response_text.startswith("```json"):
            response_text = response_text[7:]

        if response_text.startswith("```"):
            response_text = response_text[3:]

        if response_text.endswith("```"):
            response_text = response_text[:-3]

        result = json.loads(response_text.strip())

        score = int(result.get("score", 1))
        score = max(1, min(score, 10))

        return {
            "score": score,
            "strengths": result.get("strengths", []),
            "improvements": result.get("improvements", []),
            "overall_feedback": result.get(
                "overall_feedback",
                "Feedback was generated successfully."
            ),
            "sample_answer": result.get("sample_answer", ""),
            "word_count": word_count
        }

    except json.JSONDecodeError:
        return {
            "score": 1,
            "strengths": [],
            "improvements": [
                "The AI response could not be processed. Please try again."
            ],
            "overall_feedback": "Gemini returned an invalid response format.",
            "sample_answer": "",
            "word_count": word_count
        }

    except Exception as error:
        return {
            "score": 1,
            "strengths": [],
            "improvements": [
                "The AI evaluation service is temporarily unavailable."
            ],
            "overall_feedback": f"Gemini error: {str(error)}",
            "sample_answer": "",
            "word_count": word_count
        }