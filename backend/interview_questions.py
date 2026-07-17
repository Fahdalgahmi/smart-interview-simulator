import random


QUESTIONS = {
    "Software Engineer": [
        "Explain what a REST API is.",
        "What is the difference between a list and a tuple in Python?",
        "What is object-oriented programming?",
        "Explain the difference between GET and POST requests.",
        "What is the purpose of version control?",
    ],
    "Data Analyst": [
        "What is the difference between INNER JOIN and LEFT JOIN?",
        "Explain the GROUP BY clause in SQL.",
        "What does a Pandas DataFrame represent?",
        "How do you handle missing data?",
        "What is the difference between WHERE and HAVING in SQL?",
    ],
    "Business Analyst": [
        "What is SWOT analysis?",
        "How do you gather business requirements?",
        "What is the purpose of a KPI?",
        "Explain the difference between functional and non-functional requirements.",
        "How would you handle conflicting stakeholder requirements?",
    ],
}


def get_available_roles() -> list[str]:
    return list(QUESTIONS.keys())


def get_random_question(role: str) -> str | None:
    role_questions = QUESTIONS.get(role)

    if not role_questions:
        return None

    return random.choice(role_questions)