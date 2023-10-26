"""create table

Revision ID: b512bac454f4
Revises: a296d4748be3
Create Date: 2023-10-26 10:31:20.506707

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b512bac454f4'
down_revision: Union[str, None] = 'a296d4748be3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
