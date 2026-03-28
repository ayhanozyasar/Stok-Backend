from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db import SessionLocal
from ..models import User, Company, Product
from ..dependencies import admin_required

router = APIRouter(prefix="/admin")


def get_db():
    db = SessionLocal()
    yield db
    db.close()


@router.get("/users")
def get_users(user=Depends(admin_required), db: Session = Depends(get_db)):
    return db.query(User).all()


@router.get("/companies")
def get_companies(user=Depends(admin_required), db: Session = Depends(get_db)):
    return db.query(Company).all()


@router.get("/stats")
def stats(user=Depends(admin_required), db: Session = Depends(get_db)):
    return {
        "users": db.query(User).count(),
        "companies": db.query(Company).count(),
        "products": db.query(Product).count()
    }