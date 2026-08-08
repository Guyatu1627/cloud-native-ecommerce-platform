from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.db.models import User
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from app.crud import crud_product
from app.core.cache import get_cache, set_cache, invalidate_cache_pattern

router = APIRouter()

@router.get("/", response_model=List[ProductResponse])
def list_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    cache_key = f"products:skip={skip}:limit={limit}"
    cached_products = get_cache(cache_key)
    if cached_products:
        return cached_products

    products = crud_product.get_products(db, skip=skip, limit=limit)
    # Serialize objects for JSON caching
    product_data = [ProductResponse.model_validate(p).model_dump(mode="json") for p in products]
    set_cache(cache_key, product_data, expire=300)
    return products

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    product_in: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_product = crud_product.create_product(db=db, product_in=product_in)
    invalidate_cache_pattern("products:*")
    return new_product

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_in: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product = crud_product.get_product(db, product_id=product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    updated = crud_product.update_product(db=db, db_product=product, product_in=product_in)
    invalidate_cache_pattern("products:*")
    return updated

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product = crud_product.get_product(db, product_id=product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    crud_product.delete_product(db=db, product_id=product_id)
    invalidate_cache_pattern("products:*")
    return None