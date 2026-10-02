from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Float, Integer, String, Text, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

from .config import DATABASE_URL


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    username: Mapped[str] = mapped_column(String(100))
    age: Mapped[int] = mapped_column(Integer)
    weight: Mapped[float] = mapped_column(Float)
    goal: Mapped[str] = mapped_column(String(100))
    intensity: Mapped[str] = mapped_column(String(20))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Plan(Base):
    __tablename__ = "plans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String(50), index=True)
    original_plan: Mapped[str] = mapped_column(Text)
    updated_plan: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    nutrition_tip: Mapped[str] = mapped_column(Text)
    feedback: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def save_user(data: dict) -> User:
    with SessionLocal() as db:
        user = db.scalar(select(User).where(User.user_id == data["user_id"]))
        if user:
            user.username = data["username"]
            user.age = data["age"]
            user.weight = data["weight"]
            user.goal = data["goal"]
            user.intensity = data["intensity"]
        else:
            user = User(**data)
            db.add(user)
        db.commit()
        db.refresh(user)
        return user


def save_plan(user_id: str, original_plan: str, nutrition_tip: str) -> Plan:
    with SessionLocal() as db:
        plan = Plan(
            user_id=user_id,
            original_plan=original_plan,
            nutrition_tip=nutrition_tip,
        )
        db.add(plan)
        db.commit()
        db.refresh(plan)
        return plan


def get_user(user_id: str) -> Optional[User]:
    with SessionLocal() as db:
        return db.scalar(select(User).where(User.user_id == user_id))


def get_plan(user_id: str) -> Optional[Plan]:
    with SessionLocal() as db:
        return db.scalars(
            select(Plan).where(Plan.user_id == user_id).order_by(Plan.id.desc())
        ).first()


def update_plan(user_id: str, updated_plan: str, feedback: str) -> Optional[Plan]:
    with SessionLocal() as db:
        plan = db.scalars(
            select(Plan).where(Plan.user_id == user_id).order_by(Plan.id.desc())
        ).first()
        if not plan:
            return None
        plan.updated_plan = updated_plan
        plan.feedback = feedback
        db.commit()
        db.refresh(plan)
        return plan


def get_all_users_with_plans():
    with SessionLocal() as db:
        users = db.scalars(select(User).order_by(User.created_at.desc())).all()
        result = []
        for user in users:
            plan = db.scalars(
                select(Plan).where(Plan.user_id == user.user_id).order_by(Plan.id.desc())
            ).first()
            result.append((user, plan))
        return result


def delete_user(user_id: str) -> bool:
    with SessionLocal() as db:
        user = db.scalar(select(User).where(User.user_id == user_id))
        if not user:
            return False
        plans = db.scalars(select(Plan).where(Plan.user_id == user_id)).all()
        for plan in plans:
            db.delete(plan)
        db.delete(user)
        db.commit()
        return True
