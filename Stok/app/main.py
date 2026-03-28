from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .db import Base, engine
from .routers import invoice

from .routers import auth, products, stock, dashboard, export, billing, admin, webhook, user
from .middleware.rate_limit import rate_limiter

Base.metadata.create_all(bind=engine)

app = FastAPI(dependencies=[Depends(rate_limiter)])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(stock.router)
app.include_router(dashboard.router)
app.include_router(export.router)
app.include_router(billing.router)
app.include_router(admin.router)
app.include_router(webhook.router)
app.include_router(user.router)

app.include_router(invoice.router)