"""update timestamp defaults to server side

Revision ID: fc2aec2ac737
Revises: 73e8f9a2b1c4
Create Date: 2025-11-04 21:08:51.945830+00:00

Note: Previously revised 048236ac54f8 (materialized views), which was removed
as part of personal-use simplification. Now revises 73e8f9a2b1c4 directly.

"""
from collections.abc import Sequence
from typing import Union

# revision identifiers, used by Alembic.
revision: str = 'fc2aec2ac737'
down_revision: Union[str, None] = '73e8f9a2b1c4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
