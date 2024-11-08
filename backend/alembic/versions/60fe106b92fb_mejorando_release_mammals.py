"""mejorando release mammals

Revision ID: 60fe106b92fb
Revises: c1af6cd0eab2
Create Date: 2023-11-25 22:05:24.352631

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '60fe106b92fb'
down_revision = 'c1af6cd0eab2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('release_mammals', 'longitude',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=True)
    op.alter_column('release_mammals', 'latitude',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=True)
    op.alter_column('release_mammals', 'altitude',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('release_mammals', 'altitude',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('release_mammals', 'latitude',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=False)
    op.alter_column('release_mammals', 'longitude',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=False)
    # ### end Alembic commands ###
