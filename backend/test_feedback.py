from unittest.mock import Mock, patch

import requests

from backend.feedback import (
    _apply_length_score_cap,
    _fallback_sample_answer,
    _generate_sample_answer,
)


def test_short_answer_score_caps():
    assert _apply_length_score_cap(9, 0) == 1
    assert _apply_length_score_cap(9, 5) == 3
    assert _apply_length_score_cap(9, 10) == 4
    assert _apply_length_score_cap(9, 20) == 6
    assert _apply_length_score_cap(9, 30) == 9


def test_existing_low_score_is_not_increased():
    assert _apply_length_score_cap(2, 5) == 2


def test_fallback_sample_answer_is_never_empty():
    result = _fallback_sample_answer(
        "Data Analyst",
        "What does a Pandas DataFrame represent?",
    )
    assert result
    assert "Data Analyst" in result


@patch("backend.feedback.requests.post")
def test_missing_sample_answer_is_repaired(mock_post):
    response = Mock()
    response.raise_for_status.return_value = None
    response.json.return_value = {
        "response": "A DataFrame is a two-dimensional labeled data structure."
    }
    mock_post.return_value = response

    result = _generate_sample_answer(
        "Data Analyst",
        "What does a Pandas DataFrame represent?",
    )

    assert result.startswith("A DataFrame")


@patch("backend.feedback.requests.post")
def test_failed_repair_uses_fallback(mock_post):
    mock_post.side_effect = requests.exceptions.ConnectionError(
        "Ollama is unavailable"
    )

    result = _generate_sample_answer(
        "Software Engineer",
        "What is a REST API?",
    )

    assert result
    assert "Software Engineer" in result
