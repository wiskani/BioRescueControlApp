"""mark_herpetofauna.code unique is false

Revision ID: 4f73bd58d31e
Revises: 96f587ee4c94
Create Date: 2023-11-03 01:34:35.828466

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4f73bd58d31e'
down_revision = '96f587ee4c94'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('mark_herpetofauna_code_key', 'mark_herpetofauna', type_='unique')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('mark_herpetofauna_code_key', 'mark_herpetofauna', ['code'])
    # ### end Alembic commands ###
