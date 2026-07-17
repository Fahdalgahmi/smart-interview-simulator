def evaluate_candidate_answer(answer: str) -> dict:
    cleaned_answer = answer.strip()
    words = cleaned_answer.split()
    word_count = len(words)

    strengths = []
    improvements = []

    if word_count >= 40:
        score = 9
        strengths.append("The answer is detailed and well developed.")
    elif word_count >= 20:
        score = 7
        strengths.append("The answer provides a reasonable explanation.")
        improvements.append("Add more technical detail or a practical example.")
    elif word_count >= 10:
        score = 5
        strengths.append("The answer shows a basic understanding of the topic.")
        improvements.append("Explain the concept more clearly and completely.")
    else:
        score = 3
        improvements.append("The answer is too short.")
        improvements.append("Explain your reasoning and include an example.")

    if "example" in cleaned_answer.lower():
        strengths.append("The answer includes or references an example.")
        score = min(score + 1, 10)
    else:
        improvements.append("Include a practical example to support your explanation.")

    if word_count >= 15 and "." in cleaned_answer:
        strengths.append("The answer is presented in complete sentences.")
    else:
        improvements.append("Use complete sentences and a clear structure.")

    if score >= 8:
        overall_feedback = (
            "This is a strong interview answer. It demonstrates clear understanding "
            "and would likely make a positive impression."
        )
    elif score >= 6:
        overall_feedback = (
            "This is a good starting answer, but it needs more depth and specificity."
        )
    elif score >= 4:
        overall_feedback = (
            "The answer shows some understanding, but it needs clearer explanation."
        )
    else:
        overall_feedback = (
            "The answer needs significant improvement before it would be strong in an interview."
        )

    sample_answer = (
        "A strong answer should define the concept clearly, explain why it matters, "
        "and include a practical example that demonstrates how it is used."
    )

    return {
        "score": score,
        "word_count": word_count,
        "strengths": strengths,
        "improvements": improvements,
        "overall_feedback": overall_feedback,
        "sample_answer": sample_answer,
    }