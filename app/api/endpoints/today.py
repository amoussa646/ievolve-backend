from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from datetime import date, datetime
from app.models import TodayPlan, User  # Assuming you have this model
from app.schemas.requests import TodayPlanCreate
from app.schemas.responses import  TodayPlanResponse  # Assuming you have these schemas
from app.api import deps
from sqlalchemy import delete, select
router = APIRouter()

@router.get("/{today_date}", response_model=TodayPlanResponse)
async def get_today_plan(today_date: date, session: AsyncSession = Depends(deps.get_session),current_user: User = Depends(deps.get_current_user)):
    #print(today_date)
    query = select(TodayPlan).where(TodayPlan.date == today_date, TodayPlan.user_id == current_user.id)
    result = await session.execute(query)
    today_plan = result.scalars().first()

    if not today_plan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Today's plan not found")
    return today_plan

@router.post("", response_model=TodayPlanResponse)
async def create_today_plan(plan_data: TodayPlanCreate, session: AsyncSession = Depends(deps.get_session),current_user: User = Depends(deps.get_current_user)):
   
    new_today = TodayPlan(
        user_id=current_user.id,
        date= datetime.strptime(plan_data.date, "%Y-%m-%d").date() ,
        full_score=100,
        current_score=0,
        activities=[],
        habits=[]  # Use the converted date object
          # Assuming start is already a time or string that your model can handle
    )
    session.add(new_today)
    await session.commit()
    await session.refresh(new_today)
    return new_today

@router.put("", response_model=TodayPlanResponse)
async def update_today_plan( plan_data: TodayPlanCreate, session: AsyncSession = Depends(deps.get_session),current_user: User = Depends(deps.get_current_user)):
    
    query = select(TodayPlan).where(TodayPlan.date == datetime.strptime(plan_data.date, "%Y-%m-%d").date(), TodayPlan.user_id == current_user.id)
    result = await session.execute(query)
    today_plan = result.scalars().first()

    if not today_plan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Today's plan not found")
    
    for key, value in plan_data.dict().items():
        if key == "date":
           setattr(today_plan,key,datetime.strptime(plan_data.date, "%Y-%m-%d").date())
        else:
           setattr(today_plan, key, value)
    setattr(today_plan,"user_id",current_user.id)
    await session.commit()
    await session.refresh(today_plan)
    return today_plan
