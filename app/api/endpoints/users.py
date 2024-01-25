from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.core.security import get_password_hash
from app.models import User
from app.schemas.requests import UserCreateRequest, UserUpdatePasswordRequest, UserUpdateRequest
from app.schemas.responses import UserResponse

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def read_current_user(
    current_user: User = Depends(deps.get_current_user),

):
    """Get current user"""
    print(current_user)
    user_response = UserResponse(
        id=current_user.id,
        first_name= current_user.first_name,
        last_name = current_user.last_name,
        email=current_user.email,
        name=current_user.first_name + " " + current_user.last_name,
        phone_number=current_user.phone_number,
        address= current_user.address
        
    )
    return user_response


@router.delete("/me", status_code=204)
async def delete_current_user(
    current_user: User = Depends(deps.get_current_user),
    session: AsyncSession = Depends(deps.get_session),
):
    """Delete current user"""
    await session.execute(delete(User).where(User.id == current_user.id))
    await session.commit()

@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_update: UserUpdateRequest,
    current_user: User = Depends(deps.get_current_user),
    session: AsyncSession = Depends(deps.get_session),
):
    """Update current user information"""

    # Update the user's information
    
    current_user.first_name = user_update.first_name
    current_user.last_name = user_update.last_name
    current_user.email = user_update.email
    current_user.phone_number = user_update.phone_number
    current_user.address = user_update.address
    
    if user_update.latitude is not None:
        current_user.latitude = user_update.latitude

    if user_update.longitude is not None:
        current_user.longitude = user_update.longitude


    # Commit the changes to the database
    await session.commit()

    # Return the updated user
    return current_user

@router.post("/reset-password", response_model=UserResponse)
async def reset_current_user_password(
    user_update_password: UserUpdatePasswordRequest,
    session: AsyncSession = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
):
    """Update current user password"""
    current_user.hashed_password = get_password_hash(user_update_password.password)
    session.add(current_user)
    await session.commit()
    return current_user


@router.post("/signup", response_model=UserResponse)
async def register_new_user(
    new_user: UserCreateRequest,
    session: AsyncSession = Depends(deps.get_session),
):
    print(new_user)
    print("???")
    """Create new user"""
    result = await session.execute(select(User).where(User.email == new_user.email))
    if result.scalars().first() is not None:
        raise HTTPException(status_code=400, detail="Cannot use this email address")
    user = User(
        email=new_user.email,
        hashed_password=get_password_hash(new_user.password),
        # first_name = new_user.first_name ,
        # last_name = new_user.last_name,
        # address = new_user.address,
        # phone_number = new_user.phone_number,
        # avatar = "https://pixabay.com/vectors/avatar-icon-placeholder-facebook-1577909/",
        # latitude = new_user.latitude,
        # longitude = new_user.longitude
    )
    session.add(user)
    await session.commit()
    return user
