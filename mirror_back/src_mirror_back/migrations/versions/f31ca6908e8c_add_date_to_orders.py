"""add date to orders

Revision ID: f31ca6908e8c
Revises: 159438923edd
Create Date: 2024-04-19 03:40:04.191585

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'f31ca6908e8c'
down_revision = '159438923edd'
branch_labels = None
depends_on = None


def upgrade():
	# ### commands auto generated by Alembic - please adjust! ###
	op.add_column('orders', sa.Column('date', sa.Date(), nullable=True))
	op.create_index(op.f('ix_orders_date'), 'orders', ['date'], unique=False)
	# ### end Alembic commands ###


def downgrade():
	# ### commands auto generated by Alembic - please adjust! ###
	op.drop_index(op.f('ix_orders_date'), table_name='orders')
	op.drop_column('orders', 'date')
	# ### end Alembic commands ###
