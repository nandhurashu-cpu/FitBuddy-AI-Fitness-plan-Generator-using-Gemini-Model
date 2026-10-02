from google import genai

from .config import GEMINI_API_KEY, TIP_MODEL


def generate_nutrition_tip_with_flash(goal: str) -> str:
    if not GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. Add it to the .env file before generating an AI tip."
        )

    client = genai.Client(api_key=GEMINI_API_KEY)
    prompt = f"""
Give one concise, practical nutrition or recovery tip that generally complements
a fitness goal of "{goal}".

Keep it age-appropriate and focused on balanced meals, hydration, sleep, and recovery.
Do not give calorie restrictions, fasting instructions, supplement prescriptions,
or advice for rapid weight change. Do not diagnose or treat medical conditions.
Maximum 100 words.
"""
    response = client.models.generate_content(
        model=TIP_MODEL,
        contents=prompt,
    )
    text = getattr(response, "text", None)
    if not text:
        raise RuntimeError("Gemini returned an empty nutrition/recovery tip.")
    return text.strip()
