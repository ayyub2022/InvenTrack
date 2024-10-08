"""empty message

Revision ID: 7a64ce4015a5
Revises: c85c4c378d8e
Create Date: 2024-08-14 11:59:13.237690

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7a64ce4015a5'
down_revision = 'c85c4c378d8e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('payment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('phone_number', sa.String(length=15), nullable=False),
    sa.Column('transaction_id', sa.String(length=100), nullable=False),
    sa.Column('status', sa.String(length=50), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('payments')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('payments',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('inventory_id', sa.INTEGER(), nullable=False),
    sa.Column('amount', sa.NUMERIC(), nullable=False),
    sa.Column('payment_date', sa.DATETIME(), nullable=True),
    sa.Column('currency', sa.VARCHAR(length=3), nullable=True),
    sa.Column('payment_method', sa.VARCHAR(length=50), nullable=True),
    sa.Column('payment_status', sa.VARCHAR(length=20), nullable=True),
    sa.Column('transaction_id', sa.VARCHAR(length=255), nullable=True),
    sa.ForeignKeyConstraint(['inventory_id'], ['inventory.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('payment')
    # ### end Alembic commands ###
