from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db

from app.schemas.warehouse import (
    WarehouseCreate,
    WarehouseResponse
)

from app.services.warehouse_service import (
    create_warehouse,
    get_all_warehouses
)


router = APIRouter(
    prefix="/warehouses",
    tags=["Warehouses"]
)


@router.post("/", status_code=201)
def create_warehouse_route(
    warehouse: WarehouseCreate,
    db: Session = Depends(get_db)
):
    return create_warehouse(
        db,
        warehouse
    )


@router.get(
    "/",
    response_model=list[WarehouseResponse]
)
def get_warehouses_route(
    db: Session = Depends(get_db)
):
    return get_all_warehouses(db)