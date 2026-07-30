# Smart Interview Simulator

An AI-powered interview practice application that generates role-specific
questions, evaluates candidate answers, provides detailed feedback, and tracks
performance over time.

The application uses a local Ollama language model, allowing interview
evaluations to run without API fees or external AI service quotas.

## Features

- Role-specific interview questions
- AI-powered answer evaluation
- Scores from 1 to 10
- Strengths and improvement suggestions
- Suggested example answers
- Interview history
- Delete saved interview attempts
- Performance analytics
- PostgreSQL data storage
- Local and private AI processing with Ollama

## Technology Stack

### Backend
- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Ollama
- Requests

### Frontend
- HTML
- CSS
- JavaScript

## How It Works

1. The user selects an interview role.
2. The application generates a role-specific question.
3. The user submits an answer.
4. FastAPI sends the question and answer to the local Ollama model.
5. Ollama returns structured feedback in JSON format.
6. The interview result is stored in PostgreSQL.
7. The dashboard updates the interview history and analytics.

## Analytics

The application tracks:

- Total interviews completed
- Average interview score
- Highest score
- Most-practiced role

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/Fahdalgahmi/smart-interview-simulator.git
cd smart-interview-simulator