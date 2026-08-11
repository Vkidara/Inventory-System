from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base


class Warehouse(Base):
    __tablename__ = "warehouses"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    city = Column(String, nullable=False)

    products = relationship(
        "Product",
        back_populates="warehouse"
    )