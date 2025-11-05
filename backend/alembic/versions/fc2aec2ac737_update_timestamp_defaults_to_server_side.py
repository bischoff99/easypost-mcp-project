"""update timestamp defaults to server side

Revision ID: fc2aec2ac737
Revises: 048236ac54f8
Create Date: 2025-11-04 21:08:51.945830+00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fc2aec2ac737'
down_revision: Union[str, None] = '048236ac54f8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
