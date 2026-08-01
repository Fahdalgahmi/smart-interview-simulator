# InterviewIQ – AI Practice Studio

InterviewIQ is a full-stack interview practice platform that helps users prepare for technical interviews by generating role-specific questions, evaluating answers with AI, tracking interview history, and analyzing performance.

---

## Features

- Role-specific interview questions
- AI-powered answer evaluation
- Score (1–10)
- Strengths and improvement suggestions
- Sample answer generation
- Interview history
- Delete interview history
- Performance analytics dashboard
- Responsive user interface

---

## Tech Stack

### Backend
- FastAPI
- Python
- PostgreSQL
- SQLAlchemy

### Frontend
- HTML
- CSS
- JavaScript

### AI
- Ollama
- Llama 3.2

---

## Project Structure

```
smart_interview_simulator/
│
├── backend/
├── frontend/
├── database/
├── screenshots/
├── requirements.txt
└── README.md
```

---

## Installation

```bash
git clone <repository-url>

cd smart_interview_simulator

pip install -r requirements.txt

uvicorn app.main:app --reload
```

---

## API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | /roles | Get interview roles |
| POST | /question | Generate interview question |
| POST | /feedback | Evaluate answer |
| GET | /history | Interview history |
| DELETE | /history/{id} | Delete attempt |
| GET | /analytics | Performance dashboard |

---

## Screenshots

(Add screenshots here)

---

## Future Improvements

- User authentication
- Difficulty levels
- AI follow-up questions
- Leaderboard
- Cloud deployment
- Resume feedback

---

## Author

Fahd Algahmi