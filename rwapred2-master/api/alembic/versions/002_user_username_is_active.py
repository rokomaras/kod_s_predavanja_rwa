"""rename User.email to User.username, add is_active

Revision ID: 002
Revises: 001
Create Date: 2026-03-15

Promjene:
  - users.email (String 255) → users.username (String 50)
  - Dodano users.is_active (Boolean, default True)
  - Unique constraint preimenovan
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "002"
down_revision: Union[str, None] = "001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Preименуј email → username i smanji duljinu
    op.alter_column(
        "users",
        "email",
        new_column_name="username",
        type_=sa.String(50),
        existing_type=sa.String(255),
        existing_nullable=False,
    )

    # Dodaj is_active s default True
    op.add_column(
        "users",
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
    )


def downgrade() -> None:
    op.drop_column("users", "is_active")

    op.alter_column(
        "users",
        "username",
        new_column_name="email",
        type_=sa.String(255),
        existing_type=sa.String(50),
        existing_nullable=False,
    )
