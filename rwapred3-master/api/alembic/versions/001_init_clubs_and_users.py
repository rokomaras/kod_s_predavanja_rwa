"""init clubs and users

Revision ID: 001
Revises:
Create Date: 2026-03-02

Prva migracija — kreira tablice clubs i users.

Što radi upgrade():
  1. Kreira tablicu "clubs" s UNIQUE constraintom na name
  2. Kreira tablicu "users" s FK prema clubs i UNIQUE na email

Što radi downgrade():
  Briše obje tablice obrnutim redoslijedom (users prvo jer ima FK).

NAPOMENA: Uvijek pročitaj migraciju prije pokretanja "alembic upgrade"!
Autogenerate može pogriješiti (npr. rename → drop+create).
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # -- clubs tablica --
    op.create_table(
        "clubs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("city", sa.String(length=80), nullable=False),
        sa.UniqueConstraint("name"),
    )

    # -- users tablica --
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=20), nullable=False),
        sa.Column("club_id", sa.Integer(), sa.ForeignKey("clubs.id"), nullable=True),
        sa.UniqueConstraint("email"),
    )


def downgrade() -> None:
    # Obrnut redoslijed: prvo users (ima FK prema clubs), pa clubs.
    op.drop_table("users")
    op.drop_table("clubs")

