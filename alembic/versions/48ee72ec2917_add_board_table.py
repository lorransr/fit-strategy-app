"""add board table

Revision ID: 48ee72ec2917
Revises: d4867f3a4c0a
Create Date: 2023-10-03 20:34:24.869475

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "48ee72ec2917"
down_revision = "d4867f3a4c0a"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "board",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("owner_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["owner_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_board_id"), "board", ["id"], unique=False)


def downgrade():
    op.drop_table("board")
    pass
