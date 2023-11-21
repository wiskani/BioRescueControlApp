"""mejorando vivero

Revision ID: aec14d025695
Revises: f17b05f2937e
Create Date: 2023-11-21 00:51:14.972878

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'aec14d025695'
down_revision = 'f17b05f2937e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('plant_nursery', 'health_status_epiphyte',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('plant_nursery', 'vegetative_state',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('plant_nursery', 'flowering_date',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               nullable=True)
    op.alter_column('plant_nursery', 'treatment_product',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('plant_nursery', 'substrate',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('plant_nursery', 'departure_date',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('plant_nursery', 'departure_date',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               nullable=False)
    op.alter_column('plant_nursery', 'substrate',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('plant_nursery', 'treatment_product',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('plant_nursery', 'flowering_date',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               nullable=False)
    op.alter_column('plant_nursery', 'vegetative_state',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('plant_nursery', 'health_status_epiphyte',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###