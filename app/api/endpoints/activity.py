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
from app.models import User, Activity
from app.schemas.requests import ActivityCreateRequest,ActivityEndRequest,ActivitySchema
from app.schemas.responses import ActivityResponse
from datetime import date


router = APIRouter()

##
@router.post("", response_model=ActivityResponse)
async def create_activity(
    activity_create: ActivityCreateRequest,
    session: AsyncSession = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
):

    try:
        start_time = datetime.strptime(activity_create.start, "%H:%M").time()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid time format for 'start'. Use HH:MM.")

    # Convert the date string to a datetime.date object
    try:
        activity_date = datetime.strptime(activity_create.date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format for 'date'. Use YYYY-MM-DD.")

    new_activity = Activity(
        user_id=current_user.id,
        date=activity_date,  # Use the converted date object
        start=start_time  # Assuming start is already a time or string that your model can handle
    )
    session.add(new_activity)
    await session.commit()
    return {
        "id": str(new_activity.id),  # Convert UUID to string
        "start": new_activity.start.strftime("%H:%M"),  # Format time as a string
        # Format other fields as necessary
    }
@router.get("/activities", response_model=List[ActivityResponse])
async def get_activities_for_date(
    user_id: str,
    activity_date: str,
    session: AsyncSession = Depends(deps.get_session)
):
    try:
        date_obj = datetime.strptime(activity_date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    query = select(Activity).where(
        Activity.user_id == user_id,
        cast(Activity.date, Date) == date_obj
    )
    result = await session.execute(query)
    activities = result.scalars().all()

    if not activities:
        return[]

    return [ActivityResponse.from_orm(activity) for activity in activities]
@router.patch("", response_model=ActivityResponse)
async def end_activity(
    activity_end: ActivityEndRequest,
    session: AsyncSession = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
):
   
# Fetch the existing activity by its ID
        stmt = select(Activity).where(Activity.id == activity_end.id, Activity.user_id == current_user.id)
        result = await session.execute(stmt)
        existing_activity = result.scalar_one_or_none()
        
        if existing_activity is None:
            raise HTTPException(status_code=201, detail="Activity not found")
        try:
            end_time = datetime.strptime(activity_end.end, "%H:%M").time()
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid time format. Use HH:MM.")
        try:
            duration_int = int(activity_end.duration)  # Convert string to integer
        except ValueError :
            raise HTTPException(status_code=400, detail="Invalid format for duration. Must be an integer.")
        # Update the existing activity
        existing_activity.end = end_time
        existing_activity.activity = activity_end.activity   
        existing_activity.duration = duration_int
        await session.commit()
        return existing_activity
    

# @router.get("/activity/{user_id}/last_activity", response_model=ActivityResponse)
# async def get_last_activity_for_user(
#     user_id: int,
#     session: AsyncSession = Depends(deps.get_session),
# ):
#     # Query to find the most recent activity for the specified user
#     stmt = select(Activity).where(Activity.user_id == user_id).order_by(Activity.id.desc()).limit(1)
#     result = await session.execute(stmt)
#     last_activity = result.scalar_one_or_none()

#     if last_activity is None:
#         raise HTTPException(status_code=404, detail="No activities found for the user")

#     return last_activity

@router.get("/filter", response_model=ActivityResponse)
async def get_last_activity_for_user(
    user_id: str,  # Changed from int to str to accommodate UUIDs
    activity_date: Optional[str] = None,
    fields: Optional[str] = None,
    session: AsyncSession = Depends(deps.get_session),
):
    query = select(Activity).where(Activity.user_id == user_id)

    # Filter by date if provided
    if activity_date:
        query = query.filter(cast(Activity.date, Date) == cast(activity_date, Date))

    # Order by ID or timestamp to get the last activity
    query = query.order_by(Activity.id.desc()).limit(1)

    result = await session.execute(query)
    last_activity = result.scalar_one_or_none()

    if last_activity is None:
        raise HTTPException(status_code=201, detail="No activities found for the user")

    # Optionally filter the fields of the response
    if fields:
        # Implement the logic to filter the response based on the requested fields
        # This might involve transforming the `last_activity` object into a dictionary
        # and selecting only the keys that match the `fields` parameter.
        pass

    return last_activity

@router.get("/month", response_model=float)  # Adjust the response model as needed
async def get_activity_month(
    user_id: str,
    start_date: str,
    end_date: str,
    session: AsyncSession = Depends(deps.get_session),
):
    try:
        # Convert string to date
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid date format: {e}")
    print("fffff")
    print(Activity.start)
    # Construct the base query
    query = select(func.sum(cast(Activity.duration, Numeric))).where(
    Activity.user_id == user_id,
    
    cast(Activity.date, Date) >= start_date_obj,
    cast(Activity.date, Date) <= end_date_obj
)

    # Execute the query
    result = await session.execute(query)
    total_month = result.scalar_one_or_none()

    if total_month is None:
        raise HTTPException(status_code=201, detail="No activities found for the user in the specified date range")

    return total_month

@router.get("/current_month/", response_model=ActivityResponse)  # Adjust ActivityResponse as needed
async def get_recent_activity(
    user_id: str,
    start_date: date,
    session: AsyncSession = Depends(deps.get_session),
):
    query = select(Activity).where(
        Activity.user_id == user_id,
        cast(Activity.date, Date) >= start_date
    ).order_by(Activity.id.desc()).limit(1)

    result = await session.execute(query)
    activity = result.scalar_one_or_none()

    if activity is None:
        raise HTTPException(status_code=201, detail="No matching activity found")

    return activity
# @router.delete("/me", status_code=204)
# async def delete_current_chef(
#     current_chef: Chef = Depends(deps.get_current_chef),
#     session: AsyncSession = Depends(deps.get_session),
# ):
#     """Delete current user"""
#     await session.execute(delete(Chef).where(Chef.id == current_chef.id))
#     await session.commit()

# async def getUserFromChef (chefId,session):
#      existing_chef = await session.execute(
#     select(Chef).where(Chef.id == chefId))
#      chef = existing_chef.scalar_one_or_none()
#      if not chef:
#         raise HTTPException(status_code=404, detail="Chef not found")
#      existing_user = await session.execute(select(User).where(User.id == chef.user_id))
#      user = existing_user.scalar_one_or_none()
#      if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#      chef_response = ChefResponse(
#         id= chef.id,
#         rating = str(chef.rating),
#         first_name= user.first_name,
#         last_name= user.last_name,
#         avatar= str(user.avatar),
#         kitchen_name= chef.kitchen_name,
#         latitude = user.latitude,
#         longitude = user.longitude
#    )
#      return chef_response

# @router.get("/{item_id}", response_model=ChefResponse)
# async def get_chef_details(item_id: str,session: AsyncSession = Depends(deps.get_session),):
#     # Assume you have a database session named 'db' and SQLAlchemy models named 'ItemModel', 'ChefModel', 'UserModel'
#     existing_item = await session.execute(
#     select(Item).where(Item.id == item_id)
# )

#     item = existing_item.scalar_one_or_none()
    
#     if not item:
#         raise HTTPException(status_code=404, detail="Item not found")
#     chef_response = await getUserFromChef(item.chef_id, session)
#     return chef_response


# from sqlalchemy import text

# from fastapi import  Query
# @router.get("/chefs/closest", response_model=List[ChefResponse])
# async def get_closest_chefs(
#     latitude: str = Query(...),
#     longitude: str = Query(...),
#     session: AsyncSession = Depends(deps.get_session),
# ):
#     # Query the closest chefs using Haversine formula
#     query = text(
#         """
#         SELECT
#             id::text, first_name, last_name, kitchen_name, avatar, latitude, longitude,
#             6371 * 2 * ASIN(SQRT(POWER(SIN((CAST(:lat AS DOUBLE PRECISION) - CAST(latitude AS DOUBLE PRECISION)) * pi() / 180 / 2), 2) +
#             COS(CAST(:lat AS DOUBLE PRECISION) * pi() / 180) * COS(CAST(latitude AS DOUBLE PRECISION) * pi() / 180) *
#             POWER(SIN((CAST(:lon AS DOUBLE PRECISION) - CAST(longitude AS DOUBLE PRECISION)) * pi() / 180 / 2), 2))) AS distance
#         FROM chef
#         ORDER BY distance
#         LIMIT 50
#         """
#     )

#     chefs = await session.execute(
#         query, 
#         {"lat": float(latitude), "lon": float(longitude)}
#     )
#     results_as_dict = chefs.mappings().all()
    
#     print(results_as_dict)
#     results = [
#         ChefResponse(
#             id=str(chef['id']),
#             first_name=chef['first_name'],
#             last_name=chef['last_name'],
#             kitchen_name=chef['kitchen_name'],
#             avatar=chef['avatar'],
#             latitude=chef['latitude'],
#             longitude=chef['longitude']
#         )
#         for chef in results_as_dict
#     ]

#     return results
    
