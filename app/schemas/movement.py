from pydantic import BaseModel, Field
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

class MovementCreate(BaseModel):
    product_id: int = Field(
        gt=0
    )

    quantity: int = Field(
        gt=0
    )


class MovementResponse(BaseModel):
    id: int
    product_id: int
    movement_type: str
    quantity: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
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

class TransferCreate(BaseModel):
    product_id: int = Field(gt=0)

    to_warehouse_id: int = Field(gt=0)

    quantity: int = Field(gt=0)    