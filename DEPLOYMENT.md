# Deploy InterviewIQ

## 1. Push to GitHub

Create an empty public repository named `InterviewIQ`, then run from the project folder:

```powershell
git init
git add .
git commit -m "Complete InterviewIQ v1.0"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/InterviewIQ.git
git push -u origin main
```

Never commit `.env`. It is excluded by `.gitignore`.

## 2. Create a hosted PostgreSQL database

Create a free Neon project. In Neon, click **Connect** and copy the PostgreSQL connection string. Keep it private.

## 3. Deploy on Render

1. Sign in to Render with GitHub.
2. Select **New > Blueprint**.
3. Select the `InterviewIQ` repository.
4. Render reads `render.yaml`.
5. Enter the Neon connection string for `DATABASE_URL`.
6. Deploy.

The finished app will be available at the Render `onrender.com` address.

## Local development

```powershell
.\venv\Scripts\Activate.ps1
uvicorn backend.main:app --reload --reload-exclude "venv/*"
```

Open `http://127.0.0.1:8000`. The frontend is now served by FastAPI.
