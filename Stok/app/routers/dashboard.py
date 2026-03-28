from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import SessionLocal
from ..models import Product
from ..dependencies import get_current_user

router = APIRouter(prefix="/dashboard")


def get_db():
    db = SessionLocal()
    yield db
    db.close()


@router.get("")
def dashboard(user=Depends(get_current_user), db: Session = Depends(get_db)):
    total = db.query(Product).filter(Product.company_id == user["company_id"]).count()

    low = db.query(Product).filter(
        Product.company_id == user["company_id"],
        Product.stock_quantity <= Product.min_stock
    ).count()

    return {
        "total_products": total,
        "low_stock": low
    }