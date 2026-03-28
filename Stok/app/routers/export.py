from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from io import BytesIO
from openpyxl import Workbook

from ..db import SessionLocal
from ..models import Product
from ..dependencies import get_current_user

router = APIRouter(prefix="/export")


def get_db():
    db = SessionLocal()
    yield db
    db.close()


@router.get("/products")
def export_products(user=Depends(get_current_user), db: Session = Depends(get_db)):
    products = db.query(Product).filter(
        Product.company_id == user["company_id"]
    ).all()

    wb = Workbook()
    ws = wb.active

    ws.append(["ID", "Name", "Stock", "Min Stock", "Unit"])

    for p in products:
        ws.append([p.id, p.name, p.stock_quantity, p.min_stock, p.unit])

    stream = BytesIO()
    wb.save(stream)
    stream.seek(0)

    return StreamingResponse(
        stream,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=products.xlsx"}
    )