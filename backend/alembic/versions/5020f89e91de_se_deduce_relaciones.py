"""se deduce relaciones

Revision ID: 5020f89e91de
Revises: b0b9a6f1d8c3
Create Date: 2023-08-04 18:41:12.593704

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5020f89e91de'
down_revision = 'b0b9a6f1d8c3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('flora_relocation_rescue_zone_id_fkey', 'flora_relocation', type_='foreignkey')
    op.drop_column('flora_relocation', 'rescue_zone_id')
    op.drop_constraint('plant_nursery_relocation_zone_id_fkey', 'plant_nursery', type_='foreignkey')
    op.drop_constraint('plant_nursery_specie_id_fkey', 'plant_nursery', type_='foreignkey')
    op.drop_constraint('plant_nursery_rescue_zone_id_fkey', 'plant_nursery', type_='foreignkey')
    op.drop_column('plant_nursery', 'specie_id')
    op.drop_column('plant_nursery', 'relocation_zone_id')
    op.drop_column('plant_nursery', 'rescue_zone_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('plant_nursery', sa.Column('rescue_zone_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('plant_nursery', sa.Column('relocation_zone_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('plant_nursery', sa.Column('specie_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('plant_nursery_rescue_zone_id_fkey', 'plant_nursery', 'flora_rescue_zone', ['rescue_zone_id'], ['id'])
    op.create_foreign_key('plant_nursery_specie_id_fkey', 'plant_nursery', 'species', ['specie_id'], ['id'])
    op.create_foreign_key('plant_nursery_relocation_zone_id_fkey', 'plant_nursery', 'flora_relocation_zone', ['relocation_zone_id'], ['id'])
    op.add_column('flora_relocation', sa.Column('rescue_zone_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('flora_relocation_rescue_zone_id_fkey', 'flora_relocation', 'flora_rescue_zone', ['rescue_zone_id'], ['id'])
    # ### end Alembic commands ###