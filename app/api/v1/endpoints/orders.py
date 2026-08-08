from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.db.models import User
from app.schemas.order import OrderCreate, OrderResponse
from app.crud import crud_order

router = APIRouter()

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    order_in: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Protected endpoint to place a new order with atomic stock validation."""
    return crud_order.create_order(db=db, order_in=order_in, user_id=current_user.id)

@router.get("/", response_model=List[OrderResponse])
def list_my_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Protected endpoint to retrieve current user's order history."""
    return crud_order.get_user_orders(db=db, user_id=current_user.id, skip=skip, limit=limit)

@router.get("/{order_id}", response_model=OrderResponse)
def get_order_details(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Protected endpoint to fetch a specific order by ID."""
    order = crud_order.get_order_by_id(db=db, order_id=order_id, user_id=current_user.id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    return order