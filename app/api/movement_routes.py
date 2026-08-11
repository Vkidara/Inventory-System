from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db

from app.schemas.movement import (
    MovementCreate,
    MovementResponse,
    TransferCreate
)

from app.services.movement_service import (
    create_incoming_movement,
    create_outgoing_movement,
    get_movements,
    transfer_product
)



router = APIRouter(
    prefix="/movements",
    tags=["Movements"]
)


@router.post(
    "/in",
    response_model=MovementResponse,
    status_code=201
)
def create_incoming_movement_route(
    movement: MovementCreate,
    db: Session = Depends(get_db)
):
    return create_incoming_movement(
        db,
        movement
    )


@router.post(
    "/out",
    response_model=MovementResponse,
    status_code=201
)
def create_outgoing_movement_route(
    movement: MovementCreate,
    db: Session = Depends(get_db)
):
    return create_outgoing_movement(
        db,
        movement
    )

@router.get(
    "/",
    response_model=list[MovementResponse]
)
def get_movements_route(
    product_id: int | None = None,
    db: Session = Depends(get_db)
):
    return get_movements(
        db,
        product_id
    )

@router.post("/transfer")
def transfer_product_route(
    transfer: TransferCreate,
    db: Session = Depends(get_db)
):
    return transfer_product(db, transfer)