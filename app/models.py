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
    date: Mapped[str] = mapped_column(Date,nullable=True)  # New date column for activity date
    start: Mapped[str] = mapped_column(Time,nullable=True)  # Adjusted to Time type
    end: Mapped[str] = mapped_column(Time,nullable=True)  # Adjusted to Time type
    activity: Mapped[str] = mapped_column(String(20),nullable=True)
    duration: Mapped[str] = mapped_column(Integer,nullable=True)
# class Item(Base):
#     __tablename__ = "item"

#     id: Mapped[str] = mapped_column(
#         UUID(as_uuid=False), primary_key=True, default=lambda _: str(uuid.uuid4())
#     )
#     name: Mapped[str] = mapped_column(String(50), nullable=True)
#     chef_id: Mapped[str] = mapped_column(
#         ForeignKey("chef.id", ondelete="CASCADE"),
#     )
#     chef : Mapped[Chef]= relationship('Chef', back_populates='items')
#     description: Mapped[str] = mapped_column(String(300), nullable=True)
#     ingredients: Mapped[str] = mapped_column(String(300), nullable=True)
#     image_url: Mapped[str] = mapped_column(String(200), nullable=True)
#     price: Mapped[str] = mapped_column(String(200), nullable=False)
#     category: Mapped[str] = mapped_column(String(200), nullable=True)
#     sub_category: Mapped[str] = mapped_column(String(200), nullable=True)
#     rating: Mapped[str]= mapped_column(String, nullable=True)
#     totalRatings: Mapped[str]= mapped_column(String, nullable=True)
#     reviews: Mapped[List[str]] = mapped_column(ARRAY(String), nullable=True)
#     extra_attributes: Mapped[JSON]= mapped_column(JSON, nullable=True)
#     is_approved: Mapped[bool] = mapped_column(Boolean, nullable=True)
#     is_active: Mapped[bool] = mapped_column(Boolean, nullable=True)



# class Order(Base):
#     __tablename__ = "orders"

#     id: Mapped[str] = mapped_column(
#         UUID(as_uuid=False), primary_key=True, default=lambda _: str(uuid.uuid4())
#     )
#     total_price: Mapped[str] = mapped_column(String(50), nullable=True)
#     final_price: Mapped[str] = mapped_column(String(50), nullable=True)
#     delivery_cost: Mapped[str] = mapped_column(String(50), nullable=True)
#     tax_service: Mapped[str] = mapped_column(String(50), nullable=True)
#     chef_id: Mapped[str] = mapped_column(
#         ForeignKey("chef.id", ondelete="CASCADE"),
#     )
#     user_id: Mapped[str] = mapped_column(
#         ForeignKey("users.id", ondelete="CASCADE"),
#     )
#     is_chef_recieved: Mapped[bool] = mapped_column(Boolean, nullable=True)
#     is_chef_accepted: Mapped[bool] = mapped_column(Boolean, nullable=True)
#     is_chef_prepared: Mapped[bool] = mapped_column(Boolean, nullable=True)
#     is_delivery_recieved: Mapped[bool] = mapped_column(Boolean, nullable=True)
#     is_delivery_accepted: Mapped[bool] = mapped_column(Boolean, nullable=True)
#     is_delivery_delivered: Mapped[bool] = mapped_column(Boolean, nullable=True)
#     is_paid: Mapped[bool] = mapped_column(Boolean, nullable=True)
#     payment_method: Mapped[str] = mapped_column(String(50), nullable=True)
#     status:  Mapped[str] = mapped_column(String(50), nullable=True)
#     oder_time:Mapped[str] = mapped_column(String(50), nullable=True)
#     ready_time:Mapped[str] = mapped_column(String(50), nullable=True)
#     delivery_time:Mapped[str] = mapped_column(String(50), nullable=True)
#     # items: Mapped[List['OrderItem']] = relationship('OrderItem', back_populates='order')
#     items_ids: Mapped[List[str]] = mapped_column(ARRAY(String), nullable=True)
#     quantities : Mapped[List[str]] = mapped_column(ARRAY(String), nullable=True)
    