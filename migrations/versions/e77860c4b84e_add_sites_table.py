"""Migration to add 'Sites' table.

Revision ID: e77860c4b84e
Revises:
Create Date: 2023-04-24 10:53:46.696208

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "e77860c4b84e"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Gererate the 'Sites' table."""
    op.create_table(
        "sites",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=True),
        sa.Column("slug", sa.String(length=20), nullable=True),
        sa.Column("email", sa.String(length=100), nullable=True),
        sa.Column("redirect_url", sa.String(length=100), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("slug"),
    )


def downgrade() -> None:
    """Undo the 'Sites' table migration."""
    op.drop_table("sites")
