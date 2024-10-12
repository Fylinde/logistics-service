"""Initial migration

Revision ID: 8c46a8ad2c41
Revises: 
Create Date: 2024-09-28 06:30:49.087962

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8c46a8ad2c41'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('warehouses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('location', sa.String(), nullable=False),
    sa.Column('capacity', sa.Float(), nullable=False),
    sa.Column('available_space', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_warehouses_id'), 'warehouses', ['id'], unique=False)
    op.create_index(op.f('ix_warehouses_name'), 'warehouses', ['name'], unique=False)
    op.create_table('stocks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('warehouse_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['warehouse_id'], ['warehouses.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_stocks_id'), 'stocks', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_stocks_id'), table_name='stocks')
    op.drop_table('stocks')
    op.drop_index(op.f('ix_warehouses_name'), table_name='warehouses')
    op.drop_index(op.f('ix_warehouses_id'), table_name='warehouses')
    op.drop_table('warehouses')
    # ### end Alembic commands ###
