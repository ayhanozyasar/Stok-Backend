from fastapi import APIRouter
import os

router = APIRouter(prefix="/invoice")


@router.get("/{filename}")
def get_invoice(filename: str):
    path = f"./{filename}"

    if not os.path.exists(path):
        return {"error": "not found"}

    return {"file": path}