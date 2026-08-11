from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime
)

from sqlalchemy import Enum as SqlEnum

from app.models.enums import MovementType

from sqlalchemy.orm import relationship

from datetime import datetime, UTC

from app.db.database import Base


class ProductMovement(Base):
    __tablename__ = "product_movements"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    product_id = Column(
        Integer,
        ForeignKey("products.id"),
        nullable=False
    )

    movement_type = Column(
        SqlEnum(MovementType),
        nullable=False
    )

    quantity = Column(
        Integer,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(UTC)
    )

    product = relationship(
        "Product",
        back_populates="movements"
    )