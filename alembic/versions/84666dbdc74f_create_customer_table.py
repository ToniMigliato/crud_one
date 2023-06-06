"""create customer table

Revision ID: 84666dbdc74f
Revises: ec97f2446fb5
Create Date: 2023-06-06 11:22:25.219667

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '84666dbdc74f'
down_revision = 'ec97f2446fb5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('customers',
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('customer_name', sa.String(), nullable=False),
    sa.Column('customer_email', sa.String(), nullable=False),
    sa.Column('customer_created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('user_id_fk', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id_fk'], ['users.user_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('customer_id'),
    sa.UniqueConstraint('customer_email')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('customers')
    # ### end Alembic commands ###