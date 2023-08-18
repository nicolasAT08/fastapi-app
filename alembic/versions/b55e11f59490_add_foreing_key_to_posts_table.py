"""Add foreing-key to posts table

Revision ID: b55e11f59490
Revises: d2990a96d30e
Create Date: 2023-08-18 11:46:17.080872

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b55e11f59490'
down_revision: Union[str, None] = 'd2990a96d30e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("owner_id", sa.Integer, nullable=False))
    op.create_foreign_key("posts_users_fk", source_table="posts", referent_table="users", local_cols=["owner_id"], remote_cols=["id"], ondelete="CASCADE") # (arbitrary_fk_name)
    pass

def downgrade() -> None:
    op.drop_constraint("posts_users_fk",table_name="posts")
    op.drop_column("posts", "owner_id")