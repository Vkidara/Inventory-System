from pydantic import BaseModel, Field
from pydantic import BaseModel, ConfigDict


class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    quantity: int
    warehouse_id: int

class ProductCreate(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=100
    )

    quantity: int = Field(
        ge=0
    )

    warehouse_id: int = Field(
        gt=0
    )


class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    quantity: int
    warehouse_id: int


class ProductListResponse(BaseModel):
    items: list[ProductResponse]
    total: int
    limit: int
    offset: int