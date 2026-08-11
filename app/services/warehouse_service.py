from sqlalchemy.orm import Session

from app.models.warehouse import Warehouse
from app.schemas.warehouse import WarehouseCreate


def create_warehouse(
    db: Session,
    warehouse_data: WarehouseCreate
):
    warehouse = Warehouse(
        name=warehouse_data.name,
        city=warehouse_data.city
    )

    db.add(warehouse)

    db.commit()

    db.refresh(warehouse)

    return warehouse


def get_all_warehouses(
    db: Session
):
    return db.query(Warehouse).all()