from google import genai

from .config import GEMINI_API_KEY, WORKOUT_MODEL

SAFETY_NOTE = """
Create general wellness guidance only. Do not diagnose conditions, prescribe treatment,
recommend extreme exercise, starvation, dehydration, supplements, or rapid weight change.
Avoid body-shaming language. Keep exercises beginner-friendly and include rest/recovery.
If a user has pain, injury, a medical condition, or is unsure whether an exercise is safe,
tell them to stop and speak with a qualified adult/health professional.
"""


def _client():
    if not GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. Add it to the .env file before generating an AI plan."
        )
    return genai.Client(api_key=GEMINI_API_KEY)


def generate_workout_gemini(
    username: str,
    age: int,
    weight: float,
    goal: str,
    intensity: str,
) -> str:
    prompt = f"""
You are FitBuddy, a safe wellness-planning assistant.

User:
- Name: {username}
- Age: {age}
- Weight: {weight} kg
- Goal: {goal}
- Preferred intensity: {intensity}

Generate a structured 7-day general fitness/wellness plan.
For each day include:
1. Focus
2. Warm-up (5-10 minutes)
3. Main activities with simple sets/reps or time
4. Cool-down/recovery

Use age-appropriate, non-extreme guidance. Include at least one recovery/rest-oriented day.
Do not make medical claims or prescribe a calorie target. Do not encourage exercising through pain.
End with a short safety note.

{SAFETY_NOTE}
"""
    response = _client().models.generate_content(
        model=WORKOUT_MODEL,
        contents=prompt,
    )
    text = getattr(response, "text", None)
    if not text:
        raise RuntimeError("Gemini returned an empty workout plan.")
    return text.strip()
