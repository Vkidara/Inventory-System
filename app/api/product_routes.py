from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.schemas.product import (
    ProductCreate,
    ProductResponse,
    ProductListResponse
)

from app.services.product_service import (
    create_product,
    get_all_products,
    get_product_by_id,
    delete_product
)


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.post("/", status_code=201)
def create_product_route(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    return create_product(db, product)


@router.get(
    "/",
    response_model=ProductListResponse
)
def get_products_route(
    name: str | None = None,
    warehouse_id: int | None = None,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    return get_all_products(
        db=db,
        name=name,
        warehouse_id=warehouse_id,
        limit=limit,
        offset=offset
    )

@router.get(
    "/{product_id}",
    response_model=ProductResponse
)
def get_product_by_id_route(
    product_id: int,
    db: Session = Depends(get_db)
):
    return get_product_by_id(db, product_id)


@router.delete(
    "/{product_id}"
)
def delete_product_route(
    product_id: int,
    db: Session = Depends(get_db)
):
    return delete_product(db, product_id)