from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import SessionLocal
from ..models import User, Company
from ..utils.security import hash_password
from ..dependencies import admin_required

router = APIRouter(prefix="/users")


def get_db():
    db = SessionLocal()
    yield db
    db.close()


@router.post("")
def create_user(email: str, password: str, user=Depends(admin_required), db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.id == user["company_id"]).first()

    count = db.query(User).filter(User.company_id == company.id).count()

    if count >= company.max_users:
        raise HTTPException(403, "user limit reached")

    new_user = User(
        email=email,
        password=hash_password(password),
        company_id=company.id,
        role="employee",
        is_verified=True
    )

    db.add(new_user)
    db.commit()

    return {"msg": "user created"}