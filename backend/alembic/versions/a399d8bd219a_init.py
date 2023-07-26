"""init

Revision ID: a399d8bd219a
Revises: 
Create Date: 2023-07-26 15:15:32.717548

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a399d8bd219a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('flora_rescue', sa.Column('substrate', sa.String(), nullable=True))
    op.create_index(op.f('ix_flora_rescue_substrate'), 'flora_rescue', ['substrate'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_flora_rescue_substrate'), table_name='flora_rescue')
    op.drop_column('flora_rescue', 'substrate')
    # ### end Alembic commands ###
