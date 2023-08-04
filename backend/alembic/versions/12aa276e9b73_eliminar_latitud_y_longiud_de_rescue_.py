"""eliminar latitud y longiud de rescue zone

Revision ID: 12aa276e9b73
Revises: 2dca595e4de9
Create Date: 2023-07-28 15:17:25.091596

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '12aa276e9b73'
down_revision = '2dca595e4de9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_flora_rescue_zone_latitude', table_name='flora_rescue_zone')
    op.drop_index('ix_flora_rescue_zone_longitude', table_name='flora_rescue_zone')
    op.drop_column('flora_rescue_zone', 'latitude')
    op.drop_column('flora_rescue_zone', 'longitude')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('flora_rescue_zone', sa.Column('longitude', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.add_column('flora_rescue_zone', sa.Column('latitude', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.create_index('ix_flora_rescue_zone_longitude', 'flora_rescue_zone', ['longitude'], unique=False)
    op.create_index('ix_flora_rescue_zone_latitude', 'flora_rescue_zone', ['latitude'], unique=False)
    # ### end Alembic commands ###