import stripe
from fastapi import APIRouter, Depends
from ..dependencies import get_current_user

router = APIRouter(prefix="/billing")

stripe.api_key = "sk_test_xxx"

PRICE_ID = "price_xxx"


@router.post("/subscribe")
def subscribe(user=Depends(get_current_user)):
    session = stripe.checkout.Session.create(
    payment_method_types=["card"],
    mode="subscription",
    line_items=[{
        "price": "price_xxx",
        "quantity": 1,
    }],
    success_url="http://localhost:3000/success",
    cancel_url="http://localhost:3000/cancel",

    client_reference_id=str(user["company_id"]),

    subscription_data={
        "metadata": {
            "company_id": str(user["company_id"])
        }
    }
)

    return {"url": session.url}