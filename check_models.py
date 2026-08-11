from app.db.database import Base

from app.models.product import Product
from app.models.warehouse import Warehouse
from app.models.product_movement import ProductMovement

print(Base.metadata.tables.keys())