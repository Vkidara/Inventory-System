from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.product import Product
from app.schemas.product import ProductCreate
from app.models.warehouse import Warehouse
from sqlalchemy import func

def create_product(
    db: Session,
    product_data: ProductCreate
):
    warehouse = (
        db.query(Warehouse)
        .filter(
            Warehouse.id == product_data.warehouse_id
        )
        .first()
    )

    if not warehouse:
        raise HTTPException(
            status_code=404,
            detail="Warehouse not found"
        )

    product = Product(
        name=product_data.name,
        quantity=product_data.quantity,
        warehouse_id=product_data.warehouse_id
    )

    db.add(product)

    db.commit()

    db.refresh(product)

    return product

def get_product_by_id(
    db: Session,
    product_id: int
):
    product = (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product

def delete_product(
    db: Session,
    product_id: int
):
    product = (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    db.delete(product)

    db.commit()

    return {"message": "Product deleted"}


def get_all_products(
    db: Session,
    name: str | None = None,
    warehouse_id: int | None = None,
    limit: int = 20,
    offset: int = 0
):
    query = db.query(Product)

    if name:
        query = query.filter(
            func.lower(Product.name).contains(name.lower())
        )

    if warehouse_id:
        query = query.filter(
            Product.warehouse_id == warehouse_id
        )

    total = query.count()

    items = (
        query.order_by(Product.id)
        .limit(limit)
        .offset(offset)
        .all()
    )

    return {
        "items": items,
        "total": total,
        "limit": limit,
        "offset": offset
    }