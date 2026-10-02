# FitBuddy – AI Fitness Plan Generator

FitBuddy is a FastAPI web application based on the supplied project documentation. It uses Jinja2 for the frontend, SQLAlchemy + SQLite for persistence, and Google's current `google-genai` Python SDK for Gemini-powered generation.

## Project structure

```text
FitBuddy/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── gemini_generator.py
│   ├── gemini_flash_generator.py
│   ├── updated_plan.py
│   ├── schemas.py
│   └── routes.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── result.html
│   └── all_users.html
├── static/
│   └── css/
│       └── style.css
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Windows + VS Code setup

1. Install Python 3.11 or newer.
2. Open this folder in VS Code.
3. Open Terminal > New Terminal.
4. Create a virtual environment:

```powershell
python -m venv .venv
```

5. Activate it:

```powershell
.venv\Scripts\activate
```

6. Install dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

7. Copy `.env.example` to `.env`.
8. Put your Gemini API key in `.env`:

```text
GEMINI_API_KEY=your_real_key_here
```

9. Start the server:

```powershell
uvicorn app.main:app --reload
```

10. Open:

- Website: http://127.0.0.1:8000
- API docs: http://127.0.0.1:8000/docs
- Admin view: http://127.0.0.1:8000/view-all-users

## Testing

### Basic application test

Start the server and open the home page. Submit a sample user and confirm that:
- a 7-day plan is generated;
- a nutrition/recovery tip is shown;
- a row appears in the admin page.

### Feedback test

On the result page, submit feedback such as:

```text
Add more mobility work and make the plan easier.
```

Confirm that the updated plan is displayed and stored.

### API documentation

FastAPI automatically exposes Swagger UI at `/docs`.

## Important model note

The supplied documentation names older Gemini 1.5 Pro / Flash models and the older `google-generativeai` package. This implementation uses Google's newer `google-genai` SDK and a current Gemini model configured through `.env`, so the project is not tied to the deprecated model names in the original document.

## Safety note

FitBuddy is a software demonstration for general wellness planning. AI output is not medical advice. The prompts explicitly avoid extreme exercise, starvation, dehydration, rapid weight-change instructions, diagnosis, and exercising through pain. For injuries, illness, or uncertainty about exercise safety, users should stop and consult a qualified adult or health professional.
