from fastapi import FastAPI
from database import engine, Base
from routers import items

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI CRUD App",
    description="A clean CRUD API with SQLAlchemy",
    version="1.0.0"
)

app.include_router(items.router, prefix="/items", tags=["Items"])

@app.get("/")
def root():
    return {"message": "FastAPI CRUD is running 🚀"}
