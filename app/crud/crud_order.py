from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.db.models import Order, Product
from app.schemas.order import OrderCreate

def create_order(db: Session, order_in: OrderCreate, user_id: int) -> Order:
    total_amount = 0.0
    
    # Start atomic stock check and calculation
    for item in order_in.items:
        product = db.query(Product).filter(Product.id == item.product_id).with_for_update().first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with ID {item.product_id} not found"
            )
        if product.stock < item.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient stock for product '{product.title}'. Requested: {item.quantity}, Available: {product.stock}"
            )
        
        product.stock -= item.quantity
        total_amount += product.price * item.quantity

    db_order = Order(
        user_id=user_id,
        total_amount=total_amount,
        status="completed"
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_user_orders(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Order]:
    return db.query(Order).filter(Order.user_id == user_id).offset(skip).limit(limit).all()

def get_order_by_id(db: Session, order_id: int, user_id: int) -> Optional[Order]:
    return db.query(Order).filter(Order.id == order_id, Order.user_id == user_id).first()