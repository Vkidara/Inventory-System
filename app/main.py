from fastapi import FastAPI

from app.api.product_routes import router as product_router
from app.api.warehouse_routes import router as warehouse_router

from app.db.database import Base, engine

import app.models

from app.api.movement_routes import router as movement_router

Base.metadata.create_all(bind=engine)


app = FastAPI()


app.include_router(product_router)
app.include_router(warehouse_router)
app.include_router(movement_router)

@app.get("/")
def root():
    return {
        "message": "Inventory System API"
    }