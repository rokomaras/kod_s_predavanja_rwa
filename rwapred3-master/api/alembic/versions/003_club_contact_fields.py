"""add contact_email and contact_phone to Club

Revision ID: 003
Revises: 002
Create Date: 2026-03-15

Dodaje kontakt podatke klubu — oba polja su opcionalna (nullable).
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "003"
down_revision: Union[str, None] = "002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("clubs", sa.Column("contact_email", sa.String(255), nullable=True))
    op.add_column("clubs", sa.Column("contact_phone", sa.String(50), nullable=True))


def downgrade() -> None:
    op.drop_column("clubs", "contact_phone")
    op.drop_column("clubs", "contact_email")
