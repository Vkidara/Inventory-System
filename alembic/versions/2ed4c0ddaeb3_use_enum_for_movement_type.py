"""use enum for movement type

Revision ID: 2ed4c0ddaeb3
Revises: 41bb4aebbbda
Create Date: 2026-08-11 12:51:55.283684

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2ed4c0ddaeb3'
down_revision: Union[str, Sequence[str], None] = '41bb4aebbbda'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    movement_type = sa.Enum(
        'IN',
        'OUT',
        name='movementtype'
    )

    movement_type.create(
        op.get_bind(),
        checkfirst=True
    )

    op.alter_column(
        'product_movements',
        'movement_type',
        existing_type=sa.VARCHAR(),
        type_=movement_type,
        existing_nullable=False,
        postgresql_using='movement_type::movementtype'
    )


def downgrade() -> None:
    op.alter_column(
        'product_movements',
        'movement_type',
        existing_type=sa.Enum(
            'IN',
            'OUT',
            name='movementtype'
        ),
        type_=sa.VARCHAR(),
        existing_nullable=False,
        postgresql_using='movement_type::text'
    )

    sa.Enum(
        'IN',
        'OUT',
        name='movementtype'
    ).drop(
        op.get_bind(),
        checkfirst=True
    )