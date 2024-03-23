from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api import deps
from app.models import Habit, User
from app.schemas.responses import HabitResponse
from app.schemas.requests import HabitCreateRequest
from sqlalchemy import delete, select,func

router = APIRouter()


@router.get("", response_model=List[HabitResponse])
async def get_all_habits(
    session: AsyncSession = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    # Query the database for all habits where the user_id matches the current user's id
    user_habits = await session.execute(select(Habit).where(Habit.user_id == current_user.id))
    habits = user_habits.scalars().all()
    return habits
@router.post("", response_model=HabitResponse)
async def create_habit(
    habit_create: HabitCreateRequest,
    session: AsyncSession = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),

):
    new_habit = Habit(
        name=habit_create.name,
        user_id=current_user.id  # Ensure the user_id is passed in the request
    )
    session.add(new_habit)
    await session.commit()
    return {
        "id": new_habit.id,
        "name": new_habit.name,
        "user_id": new_habit.user_id
    }

@router.put("", response_model=List[HabitResponse])
async def update_habits(
    habits: List[HabitCreateRequest],
    session: AsyncSession = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
):
    # Step 1: Delete all existing habits for the current user
    await session.execute(
        delete(Habit).where(Habit.user_id == current_user.id)
    )

    # Step 2: Add new habits based on the provided data
    new_habits = [
        Habit(
            name=habit_data.name,
            user_id=current_user.id,
            frequency=habit_data.frequency  # Use the ID of the current user
        ) for habit_data in habits
    ]

    session.add_all(new_habits)
    await session.commit()

    # Step 3: Prepare the response with the newly added habits
    updated_habits = [
        {
            "id": habit.id,
            "name": habit.name,
            "user_id": habit.user_id,
            "frequency": habit.frequency
        } for habit in new_habits
    ]

    return updated_habits

@router.delete("/{habit_id}")
async def delete_habit(
    habit_id: int,
    session: AsyncSession = Depends(deps.get_session),
):
    habit = await session.get(Habit, habit_id)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    session.delete(habit)
    await session.commit()
    return {"message": "Habit deleted successfully"}
