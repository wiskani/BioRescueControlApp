"""add mark_id on translocation

Revision ID: 69f084f34077
Revises: 9f6abb9e336d
Create Date: 2023-11-06 02:11:54.843339

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '69f084f34077'
down_revision = '9f6abb9e336d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('translocation_herpetofauna', sa.Column('mark_herpetofauna_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'translocation_herpetofauna', 'mark_herpetofauna', ['mark_herpetofauna_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'translocation_herpetofauna', type_='foreignkey')
    op.drop_column('translocation_herpetofauna', 'mark_herpetofauna_id')
    # ### end Alembic commands ###