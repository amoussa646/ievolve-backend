from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.core.security import get_password_hash
from app.models import User, Activity
from app.schemas.requests import ActivityCreateRequest,ActivityEndRequest
from app.schemas.responses import ActivityResponse

router = APIRouter()

##
@router.post("/", response_model=ActivityResponse)
async def create_activity(
    activity_create: ActivityCreateRequest,
    session: AsyncSession = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
):

    new_activity = Activity(
        
        user_id=current_user.id,
        start=activity_create.start,
        
    )
    session.add(new_activity)
    await session.commit()
    return new_activity


@router.put("/", response_model=ActivityResponse)
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
            raise HTTPException(status_code=404, detail="Activity not found")

        # Update the existing activity
        existing_activity.end = activity_end.end
        existing_activity.activity = activity_end.activity   
        
        await session.commit()
        return existing_activity
    


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
    
