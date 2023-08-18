"""Add content column to posts table

Revision ID: 533319f5b84a
Revises: e5a5df290b8a
Create Date: 2023-08-08 17:09:42.069803

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '533319f5b84a'
down_revision: Union[str, None] = 'e5a5df290b8a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column('content', sa.String, nullable=False))
    pass



def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
