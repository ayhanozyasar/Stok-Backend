import stripe
from fastapi import APIRouter, Request
from sqlalchemy.orm import Session

from ..db import SessionLocal
from ..models import Company
from ..utils.limits import apply_plan_limits
from ..utils.invoice import generate_invoice

router = APIRouter(prefix="/webhook")

stripe.api_key = "sk_test_xxx"
ENDPOINT_SECRET = "whsec_xxx"


@router.post("/stripe")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    event = stripe.Webhook.construct_event(
        payload, sig_header, ENDPOINT_SECRET
    )

    db = SessionLocal()

    # ✅ ödeme başarılı
    if event["type"] == "invoice.payment_succeeded":
        data = event["data"]["object"]

        company_id = int(data["metadata"].get("company_id"))

        company = db.query(Company).filter(Company.id == company_id).first()

        company.subscription_active = True
        company.subscription_status = "active"
        company.plan = "pro"
        generate_invoice(company_id, data["amount_paid"] / 100)

        apply_plan_limits(company)

    # ❌ ödeme başarısız (retry başlar)
    if event["type"] == "invoice.payment_failed":
        data = event["data"]["object"]

        company_id = int(data["metadata"].get("company_id"))

        company = db.query(Company).filter(Company.id == company_id).first()

        company.subscription_status = "past_due"

    # ❌ tamamen iptal
    if event["type"] == "customer.subscription.deleted":
        sub = event["data"]["object"]

        company_id = int(sub["metadata"].get("company_id"))

        company = db.query(Company).filter(Company.id == company_id).first()

        company.subscription_active = False
        company.subscription_status = "canceled"
        company.plan = "free"

        apply_plan_limits(company)

    db.commit()

    return {"status": "ok"}