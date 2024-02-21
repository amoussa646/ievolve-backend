
# from typing import List
# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy import delete, select,func
# from sqlalchemy import cast, Numeric, Date
# from datetime import datetime

# from sqlalchemy.ext.asyncio import AsyncSession
# from datetime import date
# from typing import Optional
# from app.api import deps
# from app.core.security import get_password_hash
# from app.models import User, DayPlan ,Habit
# from app.schemas.requests import DayPlanCreateRequest,DayPlanSchema, HabitCreateRequest
# from app.schemas.responses import DayPlanResponse, HabitResponse
# from datetime import date


# router = APIRouter()

# @router.post("", response_model=HabitResponse)
# async def create_habit(
#     habit_create: HabitCreateRequest,
#     session: AsyncSession = Depends(deps.get_session),
#     current_user: User = Depends(deps.get_current_user),
# ):

  
#     new_habit = Habit(
#         user_id=current_user.id,        name = habit_create.name
#          # Assuming start is already a time or string that your model can handle
#     )
#     session.add(new_habit)
#     await session.commit()
#     return {
#       "name": new_habit.name
#     }

# @router.get("", response_model=DayPlanResponse)
# async def get_dayplan_for_date(
#     user_id: str,
#     dayplan_date: str,
#     session: AsyncSession = Depends(deps.get_session)
# ):
#     try:
#         date_obj = datetime.strptime(dayplan_date, "%Y-%m-%d").date()
#     except ValueError:
#         raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

#     query = select(DayPlan).where(
#         DayPlan.user_id == user_id,
#         cast(DayPlan.date, Date) == date_obj
#     )
#     result = await session.execute(query)
#     dayplan = result.scalars().all()

#     if not dayplan:
#         return {}
#     return DayPlanResponse(dayplan[-1])
# @router.put("", response_model=DayPlanResponse)
# async def edit_dayplan(
#     dayplan_id: str,
#     dayplan_update: DayPlanCreateRequest,  # This Pydantic model should represent the editable fields of a DayPlan
#     session: AsyncSession = Depends(deps.get_session),
#     current_user: User = Depends(deps.get_current_user),
# ):
#     # Convert dayplan_id to a UUID object if necessary
#     try:
#         # Attempt to fetch the specific DayPlan instance by ID
#         query = select(DayPlan).filter_by(id=dayplan_id, user_id=current_user.id)
#         result = await session.execute(query)
#         dayplan = result.scalars().one()
#     except :
#         raise HTTPException(status_code=404, detail="DayPlan not found")

#     # Update the DayPlan instance with the provided data
#     for var, value in vars(dayplan_update).items():
#         setattr(dayplan, var, value) if value else None

#     session.add(dayplan)
#     await session.commit()
#     await session.refresh(dayplan)

#     return DayPlanResponse.from_orm(dayplan)
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api import deps
from app.models import Habit
from app.schemas.responses import HabitResponse
from app.schemas.requests import HabitCreateRequest

router = APIRouter()

@router.post("", response_model=HabitResponse)
async def create_habit(
    habit_create: HabitCreateRequest,
    session: AsyncSession = Depends(deps.get_session)
):
    new_habit = Habit(
        name=habit_create.name,
        user_id=habit_create.user_id  # Ensure the user_id is passed in the request
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
    session: AsyncSession = Depends(deps.get_session)
):
    updated_habits = []
    for habit_data in habits:
        habit_id = habit_data.id  # Assuming HabitCreateRequest has an 'id' field
        habit = await session.get(Habit, habit_id)
        if not habit:
            raise HTTPException(status_code=404, detail=f"Habit {habit_id} not found")
        habit.name = habit_data.name
        await session.commit()
        updated_habits.append({
            "id": habit.id,
            "name": habit.name,
            "user_id": habit.user_id
        })
    return updated_habits

@router.delete("/{habit_id}")
async def delete_habit(
    habit_id: int,
    session: AsyncSession = Depends(deps.get_session)
):
    habit = await session.get(Habit, habit_id)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    session.delete(habit)
    await session.commit()
    return {"message": "Habit deleted successfully"}
