# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routes import user_routes, product_routes

app = FastAPI(
    title="Ürün Takip Uygulaması",
    description="Kullanıcı ve ürün yönetimi için CRUD API'leri.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:32459",
        "http://localhost:30129",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_routes.router)
app.include_router(product_routes.router)

# Create tables
@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)
