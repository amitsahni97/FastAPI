"""create age column

Revision ID: a296d4748be3
Revises: 
Create Date: 2023-10-26 09:48:56.038217

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a296d4748be3'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass
    # op.add_column('users', sa.Column('phone_num', sa.String(), nullable=True))


def downgrade() -> None:
    pass
    # op.drop_column('users', 'phone_num')
