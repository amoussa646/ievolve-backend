"""
SQL Alchemy models declaration.
https://docs.sqlalchemy.org/en/14/orm/declarative_styles.html#example-two-dataclasses-with-declarative-table
Dataclass style for powerful autocompletion support.

https://alembic.sqlalchemy.org/en/latest/tutorial.html
Note, it is used by alembic migrations logic, see `alembic/env.py`

Alembic shortcuts:
# create migration
alembic revision --autogenerate -m "migration_name"

# apply all migrations
alembic upgrade head
"""
import uuid
from typing import List

from sqlalchemy import String, Boolean, DateTime, ForeignKey, Integer, JSON,ARRAY, Date, Time
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda _: str(uuid.uuid4())
    )
    email: Mapped[str] = mapped_column(
        String(254), nullable=False, unique=True, index=True
    )
    hashed_password: Mapped[str] = mapped_column(String(128), nullable=False)
    first_name: Mapped[str] = mapped_column(String(128), nullable=True)
    last_name: Mapped[str] = mapped_column(String(128), nullable=True)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=True)
    latitude: Mapped[str] = mapped_column(String(128), nullable=True)
    longitude: Mapped[str] = mapped_column(String(128), nullable=True)

    address: Mapped[str] = mapped_column(String(128), nullable=True)
    title: Mapped[str] = mapped_column(String(10), nullable=True)
    username: Mapped[str] = mapped_column(String(128), nullable=True)
    avatar: Mapped[str] = mapped_column(String(128), nullable=True)
    language: Mapped[str] = mapped_column(String(20), nullable=True)
    status: Mapped[str] = mapped_column(String(128), nullable=True)
    token: Mapped[str] = mapped_column(String(128), nullable=True)
    last_access : Mapped[str] = mapped_column(String(128), nullable=True)
    is_authenticated: Mapped[bool] = mapped_column(Boolean, nullable=True)
    is_staff: Mapped[bool] = mapped_column(Boolean, nullable=True)
    is_chef: Mapped[bool] = mapped_column(Boolean, nullable=True)
    is_driver: Mapped[bool] = mapped_column(Boolean, nullable=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=True)
    last_login: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    new_user: Mapped[bool] = mapped_column(Boolean, nullable=True)
class Activity(Base):
    __tablename__ = "activity"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )
    date: Mapped[Date] = mapped_column(Date, nullable=True)
    start: Mapped[Time] = mapped_column(Time, nullable=True)
    end: Mapped[Time] = mapped_column(Time, nullable=True)
    activity: Mapped[str] = mapped_column(String(20), nullable=True)
    duration: Mapped[int] = mapped_column(Integer, nullable=True)

class DayPlan(Base):
    __tablename__ = "day_plan"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )
    date: Mapped[Date] = mapped_column(Date, nullable=True)

    # Relationship to Activity
    full_score:Mapped[int] = mapped_column(Integer, nullable=True)
    total_score:Mapped[int] = mapped_column(Integer, nullable=True)
    # New date column for activity date
    # start: Mapped[str] = mapped_column(Time,nullable=True)  # Adjusted to Time type
    # end: Mapped[str] = mapped_column(Time,nullable=True)  # Adjusted to Time type
    # activity: Mapped[str] = mapped_column(String(20),nullable=True)
    # duration: Mapped[str] = mapped_column(Integer,nullable=True)

class Habit(Base):
    __tablename__ = "habit"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )
    name : Mapped[str] = mapped_column(String(20), nullable=True)
    
