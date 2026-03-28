from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from .utils.security import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    return decode_token(token)


def admin_required(user=Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(403, "Admin only")
    return user