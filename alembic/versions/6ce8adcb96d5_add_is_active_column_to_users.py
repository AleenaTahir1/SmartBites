"""add is_active column to users

Revision ID: 6ce8adcb96d5
Revises: 85b8f7bef767
Create Date: 2024-12-14 02:49:01.099963

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6ce8adcb96d5'
down_revision: Union[str, None] = '85b8f7bef767'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
