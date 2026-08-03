# InterviewIQ – AI Practice Studio

🚀 **Live Demo:** https://interviewiq-api-ro8g.onrender.com

💻 **GitHub Repository:** https://github.com/Fahdalgahmi/smart-interview-simulator

InterviewIQ is a full-stack AI-powered interview practice platform that helps users prepare for technical interviews through role-specific questions, automated answer evaluation, detailed feedback, and performance analytics.

---

## Features

- AI-generated interview questions
- Multiple career paths
  - Data Analyst
  - Business Analyst
  - Software Engineer
- Easy, Medium, and Hard difficulty levels
- AI-powered answer evaluation
- Performance score (1–10)
- Personalized strengths and improvement suggestions
- Suggested answer structure
- Interview history
- View previous interview details
- Delete interview attempts
- Analytics dashboard
- PostgreSQL database integration
- Responsive user interface

---

## Tech Stack

### Backend
- Python
- FastAPI
- SQLAlchemy
- PostgreSQL (Neon)
- REST API

### Frontend
- HTML5
- CSS3
- JavaScript

### AI
- Ollama
- Llama 3.2

### Deployment
- Render
- GitHub

---

## Project Structure

```
smart_interview_simulator/
│
├── backend/
├── frontend/
├── requirements.txt
├── README.md
├── render.yaml
└── .gitignore
```

---

## Installation

```bash
git clone https://github.com/Fahdalgahmi/smart-interview-simulator.git

cd smart_interview_simulator

python -m venv venv

# Windows
venv\Scripts\activate

pip install -r requirements.txt

uvicorn backend.main:app --reload
```

---

## API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | / | Home Page |
| GET | /health | Health Check |
| GET | /roles | Available Interview Roles |
| POST | /question | Generate Interview Question |
| POST | /feedback | Evaluate Candidate Answer |
| GET | /history | Interview History |
| GET | /analytics | Analytics Dashboard |
| DELETE | /history/{id} | Delete Interview |

---





## Future Enhancements

- User authentication
- Personalized accounts
- AI follow-up questions
- Resume analysis
- Export interview reports
- Leaderboards
- Email progress reports

---

## images

<img width="949" height="448" alt="1" src="https://github.com/user-attachments/assets/661dfc60-45d2-45c2-b1a3-765547b63380" />

<img width="942" height="445" alt="2" src="https://github.com/user-attachments/assets/5e6942ad-82c8-4328-815a-a9ea0281066b" />

<img width="960" height="447" alt="3" src="https://github.com/user-attachments/assets/2ab1e713-7c2e-410b-aa54-983bf34d16a5" />

<img width="942" height="442" alt="4" src="https://github.com/user-attachments/assets/56a64e6c-d204-4c84-95e7-87f628290be3" />

<img width="941" height="443" alt="5" src="https://github.com/user-attachments/assets/e3b2c7e3-6815-468e-9c87-1e01a793637c" />





## Author

**Fahd Algahmi**

Bachelor of Science in Computer Science  
Eastern Michigan University

GitHub: https://github.com/Fahdalgahmi

LinkedIn: https://www.linkedin.com/in/fahd-algahmi/

---

## License

This project is intended for educational and portfolio purposes.
