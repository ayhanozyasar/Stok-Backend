from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import SessionLocal
from ..models import User, Company
from ..schemas import RegisterSchema, LoginSchema
from ..utils.security import hash_password, verify_password, create_token
from ..utils.limits import apply_plan_limits
from ..utils.email import send_email
from ..utils.security_extra import generate_token

router = APIRouter(prefix="/auth")


def get_db():
    db = SessionLocal()
    yield db
    db.close()


@router.post("/register")
def register(data: RegisterSchema, db: Session = Depends(get_db)):
    company = Company(name=data.company_name)
    apply_plan_limits(company)

    db.add(company)
    db.commit()
    db.refresh(company)

    verify_token = generate_token()

    user = User(
        email=data.email,
        password=hash_password(data.password),
        company_id=company.id,
        reset_token=verify_token
    )

    db.add(user)
    db.commit()

    send_email(data.email, "Verify", f"/verify/{verify_token}")

    return {"msg": "check email"}


@router.get("/verify/{token}")
def verify(token: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.reset_token == token).first()

    user.is_verified = True
    user.reset_token = None

    db.commit()

    return {"msg": "verified"}


@router.post("/login")
def login(data: LoginSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()

    if not user or not verify_password(data.password, user.password):
        return {"error": "wrong credentials"}

    if not user.is_verified:
        return {"error": "verify email"}

    token = create_token({
        "user_id": user.id,
        "company_id": user.company_id,
        "role": user.role
    })

    return {"access_token": token}


@router.post("/forgot")
def forgot(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()

    token = generate_token()
    user.reset_token = token
    db.commit()

    send_email(email, "Reset", f"/reset/{token}")

    return {"msg": "mail sent"}


@router.post("/reset")
def reset(token: str, new_password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.reset_token == token).first()

    user.password = hash_password(new_password)
    user.reset_token = None

    db.commit()

    return {"msg": "password updated"}