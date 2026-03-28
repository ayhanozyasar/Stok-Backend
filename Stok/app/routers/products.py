from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import SessionLocal
from ..models import Product, Company
from ..schemas import ProductSchema
from ..dependencies import get_current_user, admin_required

router = APIRouter(prefix="/products")


def get_db():
    db = SessionLocal()
    yield db
    db.close()


@router.get("")
def get_products(user=Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Product).filter(Product.company_id == user["company_id"]).all()


@router.post("")
def create_product(data: ProductSchema, user=Depends(get_current_user), db: Session = Depends(get_db)):
    count = db.query(Product).filter(
        Product.company_id == user["company_id"]
    ).count()

    company = db.query(Company).filter(
        Company.id == user["company_id"]
    ).first()

    if count >= company.max_products:
        raise HTTPException(403, "product limit reached")

    product = Product(**data.dict(), company_id=user["company_id"])

    db.add(product)
    db.commit()

    return product


@router.delete("/{id}")
def delete_product(id: int, user=Depends(admin_required), db: Session = Depends(get_db)):
    product = db.query(Product).filter(
        Product.id == id,
        Product.company_id == user["company_id"]
    ).first()

    if not product:
        raise HTTPException(404, "Not found")

    db.delete(product)
    db.commit()

    return {"msg": "deleted"}