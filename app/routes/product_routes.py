from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.models import Product, User
from app.schemas import ProductCreate, ProductResponse
from app.database import get_db
from app.auth import get_current_user

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/", response_model=ProductResponse)
async def create_product(
        product: ProductCreate,
        current_user: str = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == current_user).first()
    db_product = Product(**product.dict(), owner_id=user.id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@router.get("/", response_model=List[ProductResponse])
async def list_products(
        current_user: str = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == current_user).first()
    if user.is_admin:
        return db.query(Product).all()
    return db.query(Product).filter(Product.owner_id == user.id).all()


@router.delete("/{product_id}")
async def delete_product(
        product_id: int,
        current_user: str = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == current_user).first()
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if not user.is_admin and product.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Not enough privileges")

    db.delete(product)
    db.commit()
    return {"message": "Product deleted"}


@router.patch("/{product_id}", response_model=ProductResponse)
async def update_product(
        product_id: int,
        product: ProductCreate,
        current_user: str = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == current_user).first()
    db_product = db.query(Product).filter(Product.id == product_id).first()

    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    if not user.is_admin and db_product.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Not enough privileges")

    for key, value in product.dict().items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)
    return db_product