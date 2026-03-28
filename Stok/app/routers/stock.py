from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from datetime import datetime
from ..db import SessionLocal
from ..models import Product, StockMovement
from ..schemas import StockSchema
from ..dependencies import get_current_user

router = APIRouter(prefix="/stock")


def get_db():
    db = SessionLocal()
    yield db
    db.close()


@router.post("/in")
def stock_in(data: StockSchema, request: Request, user=Depends(get_current_user), db: Session = Depends(get_db)):
    product = db.query(Product).filter(
        Product.id == data.product_id,
        Product.company_id == user["company_id"]
    ).first()

    product.stock_quantity += data.quantity

    db.add(StockMovement(
        product_id=product.id,
        type="IN",
        quantity=data.quantity,
        company_id=user["company_id"],
        user_id=user["user_id"],
        ip_address=request.client.host
    ))

    db.commit()
    return {"msg": "ok"}


@router.post("/out")
def stock_out(data: StockSchema, request: Request, user=Depends(get_current_user), db: Session = Depends(get_db)):
    product = db.query(Product).filter(
        Product.id == data.product_id,
        Product.company_id == user["company_id"]
    ).first()

    if product.stock_quantity < data.quantity:
        raise HTTPException(400, "not enough stock")

    product.stock_quantity -= data.quantity

    db.add(StockMovement(
        product_id=product.id,
        type="OUT",
        quantity=data.quantity,
        company_id=user["company_id"],
        user_id=user["user_id"],
        ip_address=request.client.host
    ))

    db.commit()
    return {"msg": "ok"}


@router.get("/movements")
def movements(start: str = None, end: str = None, user=Depends(get_current_user), db: Session = Depends(get_db)):
    query = db.query(StockMovement).filter(
        StockMovement.company_id == user["company_id"]
    )

    if start:
        query = query.filter(StockMovement.created_at >= datetime.fromisoformat(start))

    if end:
        query = query.filter(StockMovement.created_at <= datetime.fromisoformat(end))

    return query.all()


@router.get("/low")
def low_stock(user=Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Product).filter(
        Product.company_id == user["company_id"],
        Product.stock_quantity <= Product.min_stock
    ).all()