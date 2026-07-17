from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.database import Base, engine, get_database
from backend.feedback import evaluate_candidate_answer
from backend.interview_questions import (
    get_available_roles,
    get_random_question,
)
from backend.models import (
    AnswerRequest,
    InterviewAttempt,
    RoleRequest,
)

app = FastAPI(
    title="Smart Interview Simulator API",
    description=(
        "Backend API for generating interview questions "
        "and evaluating candidate answers."
    ),
    version="1.0.0",
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "project": "Smart Interview Simulator",
        "status": "running",
    }


@app.get("/roles")
def get_roles():
    return {
        "roles": get_available_roles(),
    }


@app.post("/question")
def generate_question(request: RoleRequest):
    question = get_random_question(request.role)

    if question is None:
        raise HTTPException(
            status_code=400,
            detail="Invalid interview role.",
        )

    return {
        "role": request.role,
        "question": question,
    }


@app.post("/feedback")
def evaluate_answer(
    request: AnswerRequest,
    database: Session = Depends(get_database),
):
    evaluation = evaluate_candidate_answer(request.answer)

    interview_attempt = InterviewAttempt(
        role=request.role,
        question=request.question,
        answer=request.answer,
        score=evaluation["score"],
        overall_feedback=evaluation["overall_feedback"],
    )

    database.add(interview_attempt)
    database.commit()
    database.refresh(interview_attempt)

    return {
        "id": interview_attempt.id,
        "role": request.role,
        "question": request.question,
        "answer": request.answer,
        **evaluation,
    }


@app.get("/history")
def get_history(
    database: Session = Depends(get_database),
):
    statement = (
        select(InterviewAttempt)
        .order_by(InterviewAttempt.created_at.desc())
    )

    attempts = database.scalars(statement).all()

    return [
        {
            "id": attempt.id,
            "role": attempt.role,
            "question": attempt.question,
            "answer": attempt.answer,
            "score": attempt.score,
            "overall_feedback": attempt.overall_feedback,
            "created_at": attempt.created_at,
        }
        for attempt in attempts
    ]


@app.get("/history/{attempt_id}")
def get_history_item(
    attempt_id: int,
    database: Session = Depends(get_database),
):
    attempt = database.get(
        InterviewAttempt,
        attempt_id,
    )

    if attempt is None:
        raise HTTPException(
            status_code=404,
            detail="Interview attempt not found.",
        )

    return {
        "id": attempt.id,
        "role": attempt.role,
        "question": attempt.question,
        "answer": attempt.answer,
        "score": attempt.score,
        "overall_feedback": attempt.overall_feedback,
        "created_at": attempt.created_at,
    }


@app.delete("/history/{attempt_id}")
def delete_history_item(
    attempt_id: int,
    database: Session = Depends(get_database),
):
    attempt = database.get(
        InterviewAttempt,
        attempt_id,
    )

    if attempt is None:
        raise HTTPException(
            status_code=404,
            detail="Interview attempt not found.",
        )

    database.delete(attempt)
    database.commit()

    return {
        "message": "Interview attempt deleted.",
        "id": attempt_id,
    }


@app.get("/analytics")
def get_analytics(
    database: Session = Depends(get_database),
):
    attempts = database.scalars(
        select(InterviewAttempt)
    ).all()

    total_interviews = len(attempts)

    if total_interviews == 0:
        return {
            "total_interviews": 0,
            "average_score": 0,
            "highest_score": 0,
            "most_practiced_role": None,
        }

    scores = [
        attempt.score
        for attempt in attempts
    ]

    role_counts = {}

    for attempt in attempts:
        role_counts[attempt.role] = (
            role_counts.get(attempt.role, 0) + 1
        )

    most_practiced_role = max(
        role_counts,
        key=role_counts.get,
    )

    return {
        "total_interviews": total_interviews,
        "average_score": round(
            sum(scores) / total_interviews,
            1,
        ),
        "highest_score": max(scores),
        "most_practiced_role": most_practiced_role,
    }