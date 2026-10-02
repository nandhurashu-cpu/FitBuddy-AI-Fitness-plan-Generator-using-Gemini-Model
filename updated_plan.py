from google import genai

from .config import GEMINI_API_KEY, WORKOUT_MODEL

SAFETY_NOTE = """
Keep the revised plan safe and age-appropriate. Do not recommend extreme exercise,
dehydration, starvation, rapid weight change, or exercising through pain.
Do not provide medical diagnosis or treatment. Include rest/recovery where appropriate.
"""


def update_workout_plan(original_plan: str, feedback: str) -> str:
    if not GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. Add it to the .env file before updating a plan."
        )

    client = genai.Client(api_key=GEMINI_API_KEY)
    prompt = f"""
You are updating an existing FitBuddy 7-day wellness plan.

Original plan:
---BEGIN PLAN---
{original_plan}
---END PLAN---

User feedback:
---BEGIN FEEDBACK---
{feedback}
---END FEEDBACK---

Return a complete revised 7-day plan, not just a list of changes.
Respect reasonable feedback such as adding more cardio, more flexibility, simpler
movements, or additional recovery. If feedback requests something unsafe, ignore
that part and provide a safer alternative.

{SAFETY_NOTE}
"""
    response = client.models.generate_content(
        model=WORKOUT_MODEL,
        contents=prompt,
    )
    text = getattr(response, "text", None)
    if not text:
        raise RuntimeError("Gemini returned an empty updated plan.")
    return text.strip()
