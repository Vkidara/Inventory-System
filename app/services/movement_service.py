from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.product import Product
from app.models.product_movement import ProductMovement
from app.models.warehouse import Warehouse
from app.models.enums import MovementType

from app.schemas.movement import (
    MovementCreate,
    TransferCreate
)


def _create_movement(
    db: Session,
    movement_data: MovementCreate,
    movement_type: MovementType
):
    product = (
        db.query(Product)
        .filter(Product.id == movement_data.product_id)
        .first()
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    if movement_type == MovementType.IN:
        product.quantity += movement_data.quantity

    elif movement_type == MovementType.OUT:

        if product.quantity < movement_data.quantity:
            raise HTTPException(
                status_code=400,
                detail="Not enough products in stock"
            )

        product.quantity -= movement_data.quantity

    movement = ProductMovement(
        product_id=product.id,
        movement_type=movement_type,
        quantity=movement_data.quantity
    )

    try:
        db.add(movement)
        db.commit()
        db.refresh(movement)
        return movement

    except Exception:
        db.rollback()
        raise


def create_incoming_movement(
    db: Session,
    movement_data: MovementCreate
):
    return _create_movement(
        db,
        movement_data,
        MovementType.IN
    )


def create_outgoing_movement(
    db: Session,
    movement_data: MovementCreate
):
    return _create_movement(
        db,
        movement_data,
        MovementType.OUT
    )


def get_movements(
    db: Session,
    product_id: int | None = None
):
    query = db.query(ProductMovement)

    if product_id is not None:
        query = query.filter(
            ProductMovement.product_id == product_id
        )

    query = query.order_by(
        ProductMovement.created_at.desc()
    )

    return query.all()


def transfer_product(
    db: Session,
    transfer_data: TransferCreate
):
    source_product = (
        db.query(Product)
        .filter(
            Product.id == transfer_data.product_id
        )
        .first()
    )

    if not source_product:
        raise HTTPException(
            status_code=404,
            detail="Source product not found"
        )

    if source_product.warehouse_id == transfer_data.to_warehouse_id:
        raise HTTPException(
            status_code=400,
            detail="Source and destination warehouses are the same"
        )

    destination_warehouse = (
        db.query(Warehouse)
        .filter(
            Warehouse.id == transfer_data.to_warehouse_id
        )
        .first()
    )

    if not destination_warehouse:
        raise HTTPException(
            status_code=404,
            detail="Destination warehouse not found"
        )

    if source_product.quantity < transfer_data.quantity:
        raise HTTPException(
            status_code=400,
            detail="Not enough products in stock"
        )

    try:
        destination_product = (
            db.query(Product)
            .filter(
                Product.name == source_product.name,
                Product.warehouse_id == transfer_data.to_warehouse_id
            )
            .first()
        )

        if not destination_product:
            destination_product = Product(
                name=source_product.name,
                quantity=0,
                warehouse_id=transfer_data.to_warehouse_id
            )

            db.add(destination_product)
            db.flush()

        source_product.quantity -= transfer_data.quantity
        destination_product.quantity += transfer_data.quantity

        movement_out = ProductMovement(
            product_id=source_product.id,
            movement_type=MovementType.OUT,
            quantity=transfer_data.quantity
        )

        movement_in = ProductMovement(
            product_id=destination_product.id,
            movement_type=MovementType.IN,
            quantity=transfer_data.quantity
        )

        db.add(movement_out)
        db.add(movement_in)

        db.commit()

        return {
            "message": "Transfer completed successfully"
        }

    except Exception:
        db.rollback()
        raise