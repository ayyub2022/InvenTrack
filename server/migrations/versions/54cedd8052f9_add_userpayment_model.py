"""Add UserPayment model

Revision ID: 54cedd8052f9
Revises: a41d40e6120d
Create Date: 2024-08-13 11:42:01.383245

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '54cedd8052f9'
down_revision = 'a41d40e6120d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_payment')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_payment',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.Column('property_id', sa.INTEGER(), nullable=False),
    sa.Column('amount', sa.FLOAT(), nullable=False),
    sa.Column('currency', sa.VARCHAR(length=3), nullable=True),
    sa.Column('payment_method', sa.VARCHAR(length=50), nullable=True),
    sa.Column('payment_status', sa.VARCHAR(length=20), nullable=True),
    sa.Column('transaction_id', sa.VARCHAR(length=255), nullable=True),
    sa.Column('created_at', sa.DATETIME(), nullable=True),
    sa.Column('installment_amount', sa.FLOAT(), nullable=True),
    sa.Column('total_installments', sa.INTEGER(), nullable=True),
    sa.Column('paid_installments', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['property_id'], ['properties.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
