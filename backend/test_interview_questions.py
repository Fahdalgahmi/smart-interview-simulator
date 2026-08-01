from backend.interview_questions import (
    DIFFICULTIES,
    QUESTIONS,
    get_available_difficulties,
    get_available_roles,
    get_random_question,
)


def test_question_bank_has_ten_questions_per_level():
    for role_questions in QUESTIONS.values():
        assert set(role_questions) == {"Easy", "Medium", "Hard"}
        assert all(len(questions) == 10 for questions in role_questions.values())


def test_roles_and_difficulties_are_available():
    assert get_available_roles() == list(QUESTIONS)
    assert get_available_difficulties() == list(DIFFICULTIES)


def test_selected_difficulty_is_respected():
    question, difficulty = get_random_question("Data Analyst", "Hard")
    assert difficulty == "Hard"
    assert question in QUESTIONS["Data Analyst"]["Hard"]


def test_recent_question_is_not_repeated():
    first_question = QUESTIONS["Software Engineer"]["Easy"][0]
    for _ in range(20):
        question, _ = get_random_question(
            "Software Engineer",
            "Easy",
            [first_question],
        )
        assert question != first_question


def test_mix_returns_a_real_difficulty():
    question, difficulty = get_random_question("Business Analyst", "Mix")
    assert difficulty in {"Easy", "Medium", "Hard"}
    assert question in QUESTIONS["Business Analyst"][difficulty]


def test_invalid_role_or_difficulty_returns_none():
    assert get_random_question("Unknown", "Easy") is None
    assert get_random_question("Data Analyst", "Unknown") is None
