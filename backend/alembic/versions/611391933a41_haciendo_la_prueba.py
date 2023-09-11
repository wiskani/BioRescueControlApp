"""haciendo la prueba

Revision ID: 611391933a41
Revises: e91436900878
Create Date: 2023-08-29 00:40:20.391035

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '611391933a41'
down_revision = 'e91436900878'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_clear_mammals_id', table_name='clear_mammals')
    op.drop_table('clear_mammals')
    op.drop_index('ix_clear_flora_id', table_name='clear_flora')
    op.drop_table('clear_flora')
    op.drop_index('ix_clear_herpetofauna_id', table_name='clear_herpetofauna')
    op.drop_table('clear_herpetofauna')
    op.drop_index('ix_towers_id', table_name='towers')
    op.drop_index('ix_towers_latitude', table_name='towers')
    op.drop_index('ix_towers_longitude', table_name='towers')
    op.drop_table('towers')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('towers',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('towers_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('number', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('latitude', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('longitude', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='towers_pkey'),
    sa.UniqueConstraint('number', name='towers_number_key'),
    postgresql_ignore_search_path=False
    )
    op.create_index('ix_towers_longitude', 'towers', ['longitude'], unique=False)
    op.create_index('ix_towers_latitude', 'towers', ['latitude'], unique=False)
    op.create_index('ix_towers_id', 'towers', ['id'], unique=False)
    op.create_table('clear_herpetofauna',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('is_clear', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('tower_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('clear_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['tower_id'], ['towers.id'], name='clear_herpetofauna_tower_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='clear_herpetofauna_pkey'),
    sa.UniqueConstraint('tower_id', name='clear_herpetofauna_tower_id_key')
    )
    op.create_index('ix_clear_herpetofauna_id', 'clear_herpetofauna', ['id'], unique=False)
    op.create_table('clear_flora',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('is_clear', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('tower_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('clear_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['tower_id'], ['towers.id'], name='clear_flora_tower_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='clear_flora_pkey'),
    sa.UniqueConstraint('tower_id', name='clear_flora_tower_id_key')
    )
    op.create_index('ix_clear_flora_id', 'clear_flora', ['id'], unique=False)
    op.create_table('clear_mammals',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('is_clear', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('tower_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('clear_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['tower_id'], ['towers.id'], name='clear_mammals_tower_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='clear_mammals_pkey'),
    sa.UniqueConstraint('tower_id', name='clear_mammals_tower_id_key')
    )
    op.create_index('ix_clear_mammals_id', 'clear_mammals', ['id'], unique=False)
    # ### end Alembic commands ###