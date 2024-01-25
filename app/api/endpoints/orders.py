from fastapi import APIRouter, Depends, HTTPException, Query 
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi.logger import logger

from app.models import Order, User, Chef, Item
from app.api import deps
from  app.schemas.requests  import OrderCreateRequest
from  app.schemas.responses import OrderResponse

router = APIRouter()

@router.post("/create", response_model=OrderResponse)
async def create_order(
    order_create: OrderCreateRequest,
    session: AsyncSession = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
):
  try:
    # Validate chef_id and items_ids
    chef = await session.execute(select(Chef).where(Chef.id == order_create.chef_id))
    if not chef.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Chef not found")

 
    new_order = Order(
        user_id=current_user.id,
        chef_id=order_create.chef_id,
        total_price=order_create.total_price,
        final_price=order_create.final_price,
        delivery_cost=order_create.delivery_cost,
        tax_service=order_create.tax_service,
        items_ids=order_create.items_ids,
        quantities=order_create.quantities,
        
        is_chef_recieved=False,
        is_chef_accepted=False,
        is_delivery_recieved=False,
        is_delivery_accepted=False,
        is_paid=False,
        #payment_method=order_create.payment_method,
        status="pending",
        # Add any other fields you need to populate for Order model
    )

    # Add the order to the database
    session.add(new_order)
    await session.commit()

    return new_order
  except HTTPException as e:
        logger.error(f"Bad Request: {e.detail}")
        raise e  # Re-raise the exception to maintain FastAPI's default error response

  except Exception as e:
        logger.error(f"Internal Server Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")



@router.get("/orders-by-chef/{chef_id}", response_model=list[OrderResponse])
async def get_orders_by_chef(
    chef_id: str,
    is_chef_recieved: bool = Query(None),
    is_chef_accepted: bool = Query(None),
    is_chef_prepared: bool = Query(None),
    is_delivery_recieved: bool = Query(None),
    is_delivery_accepted: bool = Query(None),
    is_delivery_delivered: bool = Query(None),
    is_paid: bool = Query(None),
    session: AsyncSession = Depends(deps.get_session),
):

    filters = [
        Order.chef_id == chef_id,
        Order.is_chef_recieved == is_chef_recieved if is_chef_recieved is not None else True,
        Order.is_chef_accepted == is_chef_accepted if is_chef_accepted is not None else True,
        Order.is_chef_prepared == is_chef_prepared if is_chef_prepared is not None else True,
        Order.is_delivery_recieved == is_delivery_recieved if is_delivery_recieved is not None else True,
        Order.is_delivery_accepted == is_delivery_accepted if is_delivery_accepted is not None else True,
        Order.is_delivery_delivered == is_delivery_delivered if is_delivery_delivered is not None else True,
        Order.is_paid == is_paid if is_paid is not None else True,
    ]

    orders = await session.execute(select(Order).filter(*filters))
    return orders.scalars().all()