from pydantic import BaseModel, Field
from pydantic import BaseModel, Field, ConfigDict

class WarehouseCreate(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=100
    )

    city: str = Field(
        min_length=2,
        max_length=100
    )


class WarehouseResponse(BaseModel):
    id: int
    name: str
    city: str
    
    model_config = ConfigDict(
        from_attributes=True
)