"""tables for translocation herpetofauna

Revision ID: 9f6abb9e336d
Revises: 4f73bd58d31e
Create Date: 2023-11-05 01:53:23.824114

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f6abb9e336d'
down_revision = '4f73bd58d31e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('point_herpetofauna_translocation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cod', sa.String(), nullable=False),
    sa.Column('date', sa.DateTime(timezone=True), nullable=False),
    sa.Column('latitude', sa.Float(), nullable=False),
    sa.Column('longitude', sa.Float(), nullable=False),
    sa.Column('altitude', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('cod')
    )
    op.create_index(op.f('ix_point_herpetofauna_translocation_id'), 'point_herpetofauna_translocation', ['id'], unique=False)
    op.create_table('transect_herpetofauna_translocation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cod', sa.String(), nullable=False),
    sa.Column('date', sa.DateTime(timezone=True), nullable=False),
    sa.Column('latitude_in', sa.Float(), nullable=False),
    sa.Column('longitude_in', sa.Float(), nullable=False),
    sa.Column('altitude_in', sa.Integer(), nullable=False),
    sa.Column('latitude_out', sa.Float(), nullable=False),
    sa.Column('longitude_out', sa.Float(), nullable=False),
    sa.Column('altitude_out', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('cod')
    )
    op.create_index(op.f('ix_transect_herpetofauna_translocation_id'), 'transect_herpetofauna_translocation', ['id'], unique=False)
    op.create_table('translocation_herpetofauna',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cod', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('transect_herpetofauna_translocation_id', sa.Integer(), nullable=True),
    sa.Column('point_herpetofauna_translocation_id', sa.Integer(), nullable=True),
    sa.Column('specie_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['point_herpetofauna_translocation_id'], ['point_herpetofauna_translocation.id'], ),
    sa.ForeignKeyConstraint(['specie_id'], ['species.id'], ),
    sa.ForeignKeyConstraint(['transect_herpetofauna_translocation_id'], ['transect_herpetofauna_translocation.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('cod')
    )
    op.create_index(op.f('ix_translocation_herpetofauna_id'), 'translocation_herpetofauna', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_translocation_herpetofauna_id'), table_name='translocation_herpetofauna')
    op.drop_table('translocation_herpetofauna')
    op.drop_index(op.f('ix_transect_herpetofauna_translocation_id'), table_name='transect_herpetofauna_translocation')
    op.drop_table('transect_herpetofauna_translocation')
    op.drop_index(op.f('ix_point_herpetofauna_translocation_id'), table_name='point_herpetofauna_translocation')
    op.drop_table('point_herpetofauna_translocation')
    # ### end Alembic commands ###