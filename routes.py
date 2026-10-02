from pathlib import Path

from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from .database import (
    delete_user,
    get_all_users_with_plans,
    get_plan,
    get_user,
    save_plan,
    save_user,
    update_plan,
)
from .gemini_flash_generator import generate_nutrition_tip_with_flash
from .gemini_generator import generate_workout_gemini
from .schemas import FeedbackRequest, UserInput
from .updated_plan import update_workout_plan

BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"error": None},
    )


@router.post("/generate-workout", response_class=HTMLResponse)
def generate_workout(
    request: Request,
    user_id: str = Form(...),
    username: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
):
    try:
        user_input = UserInput(
            user_id=user_id,
            username=username,
            age=age,
            weight=weight,
            goal=goal,
            intensity=intensity,
        )
        workout_plan = generate_workout_gemini(
            username=user_input.username,
            age=user_input.age,
            weight=user_input.weight,
            goal=user_input.goal,
            intensity=user_input.intensity,
        )
        nutrition_tip = generate_nutrition_tip_with_flash(user_input.goal)

        save_user(user_input.model_dump())
        save_plan(user_input.user_id, workout_plan, nutrition_tip)

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "user": user_input.model_dump(),
                "workout_plan": workout_plan,
                "nutrition_tip": nutrition_tip,
                "error": None,
            },
        )
    except Exception as exc:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={"error": str(exc)},
            status_code=400,
        )


@router.get("/result/{user_id}", response_class=HTMLResponse)
def result(request: Request, user_id: str):
    user = get_user(user_id)
    plan = get_plan(user_id)
    if not user or not plan:
        raise HTTPException(status_code=404, detail="User or plan not found.")

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "user": {
                "user_id": user.user_id,
                "username": user.username,
                "age": user.age,
                "weight": user.weight,
                "goal": user.goal,
                "intensity": user.intensity,
            },
            "workout_plan": plan.updated_plan or plan.original_plan,
            "original_plan": plan.original_plan,
            "nutrition_tip": plan.nutrition_tip,
            "error": None,
        },
    )


@router.post("/submit-feedback", response_class=HTMLResponse)
def submit_feedback(
    request: Request,
    user_id: str = Form(...),
    feedback: str = Form(...),
):
    try:
        feedback_request = FeedbackRequest(user_id=user_id, feedback=feedback)
        user = get_user(feedback_request.user_id)
        plan = get_plan(feedback_request.user_id)

        if not user or not plan:
            raise HTTPException(status_code=404, detail="User or plan not found.")

        updated = update_workout_plan(plan.original_plan, feedback_request.feedback)
        update_plan(feedback_request.user_id, updated, feedback_request.feedback)

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "user": {
                    "user_id": user.user_id,
                    "username": user.username,
                    "age": user.age,
                    "weight": user.weight,
                    "goal": user.goal,
                    "intensity": user.intensity,
                },
                "workout_plan": updated,
                "original_plan": plan.original_plan,
                "nutrition_tip": plan.nutrition_tip,
                "feedback": feedback_request.feedback,
                "success": "Your plan was updated successfully.",
                "error": None,
            },
        )
    except Exception as exc:
        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "user": {"user_id": user_id},
                "workout_plan": "",
                "nutrition_tip": "",
                "feedback": feedback,
                "error": str(exc),
            },
            status_code=400,
        )


@router.get("/view-all-users", response_class=HTMLResponse)
def view_all_users(request: Request):
    rows = get_all_users_with_plans()
    return templates.TemplateResponse(
        request=request,
        name="all_users.html",
        context={"rows": rows},
    )


@router.post("/delete-user/{user_id}")
def remove_user(user_id: str):
    delete_user(user_id)
    return RedirectResponse(url="/view-all-users", status_code=303)
