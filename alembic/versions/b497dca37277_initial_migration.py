"""initial migration

Revision ID: b497dca37277
Revises:
Create Date: 2026-06-01 12:59:58.347015

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b497dca37277"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "products",

        sa.Column(
            "id",
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            "name",
            sa.String(),
            nullable=False
        ),

        sa.Column(
            "quantity",
            sa.Integer(),
            nullable=True
        ),

        sa.PrimaryKeyConstraint("id")
    )

    op.create_index(
        op.f("ix_products_id"),
        "products",
        ["id"],
        unique=False
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(
        op.f("ix_products_id"),
        table_name="products"
    )

    op.drop_table("products")