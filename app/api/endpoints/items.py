from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.models import Chef, Item
from app.schemas.requests import ItemCreateRequest
from app.schemas.responses import ItemResponse

router = APIRouter()

@router.post("/create", response_model=ItemResponse)
async def create_item(
    item_create: ItemCreateRequest,
    session: AsyncSession = Depends(deps.get_session),
    current_chef: Chef = Depends(deps.get_current_chef),
):

    # Create the new item
    new_item = Item(
        chef_id=current_chef.id,
        name=item_create.name,
        price = item_create.price,
        description=item_create.description,
        ingredients=item_create.ingredients,
        image_url=item_create.image_url,
        category=item_create.category,
        sub_category=item_create.sub_category,
        extra_attributes=item_create.extra_attributes,
        rating="0",
        totalRatings="0"
        # Add any other fields you need to populate for Item model
    )
    session.add(new_item)
    await session.commit()
    return new_item


@router.get("/by-chef/{chef_id}", response_model=list[ItemResponse])
async def get_items_by_chef(
    chef_id: str,
    is_active: bool = Query(None),
    is_approved: bool = Query(None),
    category: str = Query(None),
    sub_category: str = Query(None),
   session: AsyncSession = Depends(deps.get_session),
):

 
    filters = [
        Item.chef_id == chef_id,
        Item.category == category if category else True,
        Item.sub_category == sub_category if sub_category else True,
    ]

    if is_active is not None:
        filters.append(Item.is_active == is_active)

    if is_approved is not None:
        filters.append(Item.is_approved == is_approved)
    
    items = await session.execute(select(Item).filter(*filters))
    return items.scalars().all()

@router.get("/all", response_model=list[ItemResponse])
async def get_all_items(
    category: str = Query(None),
    sub_category: str = Query(None),
    session: AsyncSession = Depends(deps.get_session),
):

    # Query all items with optional category and sub_category filters
    items = await session.execute(
        select(Item).filter(
            Item.category == category if category else True,
            Item.sub_category == sub_category if sub_category else True,
        )
    )

    return items.scalars().all()


@router.get("/search/", response_model=list[ItemResponse])
async def search_items(
    query: str = Query(..., min_length=3),
    category: str = Query(None),
    sub_category: str = Query(None),
    session: AsyncSession = Depends(deps.get_session),  # Replace with your dependency
):
  #  try:
        # Query items based on the search parameters
        items = await session.execute(
            select(Item).filter(
                Item.name.ilike(f"%{query}%"),
                Item.category == category if category else True,
                Item.sub_category == sub_category if sub_category else True,
            )
        )
        
        # Convert the result to a list of ItemResponse
        search_results = [
            ItemResponse(
                id = Item.id,
                name=Item.name,
                category=Item.category,
                sub_category=Item.sub_category,
            )
            for Item in items.scalars().all()
        ]

        return search_results

    # except Exception as e:
    #     # Handle exceptions appropriately (e.g., log the error)
    #     raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@router.put("/updateItem/{item_id}", response_model=list[ItemResponse])
async def update_item_status(
    item_id: str,
    is_approved: bool = None,
    is_active: bool = None,
    session: AsyncSession = Depends(deps.get_session),
):
    # Retrieve the item from the database
    item = await session.execute(select(Item).filter(Item.id == item_id)).scalar()

    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    # Update the item status based on provided parameters
    if is_approved is not None:
        item.is_approved = is_approved

    if is_active is not None:
        item.is_active = is_active

    # Commit the changes to the database
    await session.commit()

    # Return the updated item
    return {"message": "Item status updated successfully", "item": item}