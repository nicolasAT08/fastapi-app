"""Add las few columns to posts table

Revision ID: 7438c108e551
Revises: b55e11f59490
Create Date: 2023-08-18 11:57:08.316611

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7438c108e551'
down_revision: Union[str, None] = 'b55e11f59490'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",
                  sa.Column("published", sa.Boolean, nullable=False, server_default="TRUE"),
                  )
    op.add_column("posts",
                  sa.Column("created_at",sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),
                  )
    pass


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
