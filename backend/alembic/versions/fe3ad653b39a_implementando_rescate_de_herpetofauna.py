"""Implementando rescate de herpetofauna

Revision ID: fe3ad653b39a
Revises: 385a2342ad9d
Create Date: 2023-10-13 12:57:31.037645

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'fe3ad653b39a'
down_revision = '385a2342ad9d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('towers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('number', sa.Integer(), nullable=False),
    sa.Column('latitude', sa.Float(), nullable=False),
    sa.Column('longitude', sa.Float(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('number')
    )
    op.create_index(op.f('ix_towers_id'), 'towers', ['id'], unique=False)
    op.create_index(op.f('ix_towers_latitude'), 'towers', ['latitude'], unique=False)
    op.create_index(op.f('ix_towers_longitude'), 'towers', ['longitude'], unique=False)
    op.create_table('clear_flora',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('is_clear', sa.Boolean(), nullable=False),
    sa.Column('tower_id', sa.Integer(), nullable=False),
    sa.Column('clear_at', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['tower_id'], ['towers.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('tower_id')
    )
    op.create_index(op.f('ix_clear_flora_id'), 'clear_flora', ['id'], unique=False)
    op.create_table('clear_herpetofauna',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('is_clear', sa.Boolean(), nullable=False),
    sa.Column('tower_id', sa.Integer(), nullable=False),
    sa.Column('clear_at', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['tower_id'], ['towers.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('tower_id')
    )
    op.create_index(op.f('ix_clear_herpetofauna_id'), 'clear_herpetofauna', ['id'], unique=False)
    op.create_table('clear_mammals',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('is_clear', sa.Boolean(), nullable=False),
    sa.Column('tower_id', sa.Integer(), nullable=False),
    sa.Column('clear_at', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['tower_id'], ['towers.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('tower_id')
    )
    op.create_index(op.f('ix_clear_mammals_id'), 'clear_mammals', ['id'], unique=False)
    op.create_table('transect_herpetofauna',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('number', sa.Integer(), nullable=False),
    sa.Column('date_in', sa.DateTime(), nullable=False),
    sa.Column('date_out', sa.DateTime(), nullable=False),
    sa.Column('latitude_in', sa.Float(), nullable=False),
    sa.Column('longitude_in', sa.Float(), nullable=False),
    sa.Column('altitude_in', sa.Integer(), nullable=False),
    sa.Column('latitude_out', sa.Float(), nullable=False),
    sa.Column('longitude_out', sa.Float(), nullable=False),
    sa.Column('altitude_out', sa.Integer(), nullable=False),
    sa.Column('tower_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['tower_id'], ['towers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_transect_herpetofauna_id'), 'transect_herpetofauna', ['id'], unique=False)
    op.create_table('mark_herpetofauna',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('number', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(length=50), nullable=True),
    sa.Column('gender', sa.Boolean(), nullable=True),
    sa.Column('LHC', sa.Float(), nullable=True),
    sa.Column('weight', sa.Float(), nullable=True),
    sa.Column('is_photo_mark', sa.Boolean(), nullable=False),
    sa.Column('is_elastomer_mark', sa.Boolean(), nullable=False),
    sa.Column('tower_id', sa.Integer(), nullable=False),
    sa.Column('species_id', sa.Integer(), nullable=False),
    sa.Column('age_group_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['age_group_id'], ['age_group.id'], ),
    sa.ForeignKeyConstraint(['species_id'], ['species.id'], ),
    sa.ForeignKeyConstraint(['tower_id'], ['towers.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('code'),
    sa.UniqueConstraint('number')
    )
    op.create_index(op.f('ix_mark_herpetofauna_id'), 'mark_herpetofauna', ['id'], unique=False)
    op.drop_index('ix_rescue_herpetofauna_id', table_name='rescue_herpetofauna')
    op.drop_table('rescue_herpetofauna')
    op.drop_index('ix_genus_genus_full_name', table_name='genus')
    op.drop_column('genus', 'genus_full_name')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('genus', sa.Column('genus_full_name', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.create_index('ix_genus_genus_full_name', 'genus', ['genus_full_name'], unique=False)
    op.create_table('rescue_herpetofauna',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('number', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('rescue_date_in', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('rescue_date_out', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('latitude', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('longitude', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('altitude', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('individual_count', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('gender', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('age_group_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('specie_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['age_group_id'], ['age_group.id'], name='rescue_herpetofauna_age_group_id_fkey'),
    sa.ForeignKeyConstraint(['specie_id'], ['species.id'], name='rescue_herpetofauna_specie_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='rescue_herpetofauna_pkey')
    )
    op.create_index('ix_rescue_herpetofauna_id', 'rescue_herpetofauna', ['id'], unique=False)
    op.drop_index(op.f('ix_mark_herpetofauna_id'), table_name='mark_herpetofauna')
    op.drop_table('mark_herpetofauna')
    op.drop_index(op.f('ix_transect_herpetofauna_id'), table_name='transect_herpetofauna')
    op.drop_table('transect_herpetofauna')
    op.drop_index(op.f('ix_clear_mammals_id'), table_name='clear_mammals')
    op.drop_table('clear_mammals')
    op.drop_index(op.f('ix_clear_herpetofauna_id'), table_name='clear_herpetofauna')
    op.drop_table('clear_herpetofauna')
    op.drop_index(op.f('ix_clear_flora_id'), table_name='clear_flora')
    op.drop_table('clear_flora')
    op.drop_index(op.f('ix_towers_longitude'), table_name='towers')
    op.drop_index(op.f('ix_towers_latitude'), table_name='towers')
    op.drop_index(op.f('ix_towers_id'), table_name='towers')
    op.drop_table('towers')
    # ### end Alembic commands ###
