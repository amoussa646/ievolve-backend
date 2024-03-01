
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete, select,func
from sqlalchemy import cast, Numeric, Date
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date
from typing import Optional
from app.api import deps
from app.core.security import get_password_hash
from app.models import User, DayPlan
from app.schemas.requests import DayPlanCreateRequest,DayPlanSchema
from app.schemas.responses import DayPlanResponse
from datetime import date,datetime


router = APIRouter()
@router.post("", response_model=DayPlanResponse)
async def create_dayplan(
    dayplan_create: DayPlanCreateRequest,
    session: AsyncSession = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
):


    # Convert the date string to a datetime.date object
    try:
        dayplan_date = datetime.strptime(dayplan_create.date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format for 'date'. Use YYYY-MM-DD.")

    new_dayplan = DayPlan(
        user_id=current_user.id,
        date=dayplan_date)  # Use the converted date object
      
    session.add(new_dayplan)
    await session.commit()
    return {
        "id": str(new_dayplan.id),  # Convert UUID to string
        # Format other fields as necessary
    }
@router.get("", response_model=DayPlanResponse)
async def get_dayplan_for_date(
    user_id: str,
    dayplan_date: str,
    session: AsyncSession = Depends(deps.get_session)
):
    try:
        date_obj = datetime.strptime(dayplan_date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    query = select(DayPlan).where(
        DayPlan.user_id == user_id,
        cast(DayPlan.date, Date) == date_obj
    )
    result = await session.execute(query)
    dayplan = result.scalars().all()

    if not dayplan:
        return {}
    return DayPlanResponse.from_orm(dayplan[-1])
@router.put("", response_model=DayPlanResponse)
async def edit_dayplan(
    dayplan_id: str,
    dayplan_update: DayPlanCreateRequest,  # This Pydantic model should represent the editable fields of a DayPlan
    session: AsyncSession = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
):
    # Convert dayplan_id to a UUID object if necessary
    try:
        # Attempt to fetch the specific DayPlan instance by ID
        query = select(DayPlan).filter_by(id=dayplan_id, user_id=current_user.id)
        result = await session.execute(query)
        dayplan = result.scalars().one()
    except :
        raise HTTPException(status_code=404, detail="DayPlan not found")

    # Update the DayPlan instance with the provided data
    for var, value in vars(dayplan_update).items():
        setattr(dayplan, var, value) if value else None
    date_obj = datetime.strptime(dayplan_update.date, '%Y-%m-%d')

# Update the DayPlan instance with the converted date object
    dayplan.date = date_obj.date()
    session.add(dayplan)
    await session.commit()
    await session.refresh(dayplan)

    return dayplan
