from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    quantity = Column(Integer, default=0)

    warehouse_id = Column(
        Integer,
        ForeignKey("warehouses.id"),
        nullable=False
    )

    warehouse = relationship(
        "Warehouse",
        back_populates="products"
    )

    movements = relationship(
    "ProductMovement",
    back_populates="product"
)