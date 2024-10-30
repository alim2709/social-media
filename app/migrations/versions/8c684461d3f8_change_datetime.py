"""change_datetime

Revision ID: 8c684461d3f8
Revises: b8c289d1a5ec
Create Date: 2024-10-30 15:03:42.623640

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8c684461d3f8'
down_revision: Union[str, None] = 'b8c289d1a5ec'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Update `created_at` default for posts and comments tables to use UTC
    op.alter_column(
        "posts",
        "created_at",
        server_default=sa.text("(CURRENT_TIMESTAMP AT TIME ZONE 'UTC')"),
        existing_nullable=False,
    )
    op.alter_column(
        "comments",
        "created_at",
        server_default=sa.text("(CURRENT_TIMESTAMP AT TIME ZONE 'UTC')"),
        existing_nullable=False,
    )

def downgrade() -> None:
    # Downgrade by removing the server default
    op.alter_column("posts", "created_at", server_default=None, existing_nullable=False)
    op.alter_column("comments", "created_at", server_default=None, existing_nullable=False)
