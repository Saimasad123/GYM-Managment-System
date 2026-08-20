"""add expenses table

Revision ID: fbf1e50b59fb
Revises: 2d23ead04e5b
Create Date: 2026-08-17 16:50:52.430952

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "fbf1e50b59fb"
down_revision: Union[str, Sequence[str], None] = "2d23ead04e5b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add payment method with a temporary default
    # because existing expense records need a value.
    op.add_column(
        "expenses",
        sa.Column(
            "payment_method",
            sa.String(length=30),
            nullable=False,
            server_default="Cash",
        ),
    )

    # Add optional reference number
    op.add_column(
        "expenses",
        sa.Column(
            "reference_number",
            sa.String(length=100),
            nullable=True,
        ),
    )

    # Add optional notes
    op.add_column(
        "expenses",
        sa.Column(
            "notes",
            sa.String(length=500),
            nullable=True,
        ),
    )

    # Convert description from TEXT to VARCHAR(500)
    # and make it required.
    op.alter_column(
        "expenses",
        "description",
        existing_type=sa.Text(),
        type_=sa.String(length=500),
        nullable=False,
    )

    # Remove old title column.
    op.drop_column(
        "expenses",
        "title",
    )

    # Remove temporary default.
    op.alter_column(
        "expenses",
        "payment_method",
        server_default=None,
    )


def downgrade() -> None:
    # Restore title column.
    op.add_column(
        "expenses",
        sa.Column(
            "title",
            sa.String(length=150),
            nullable=True,
        ),
    )

    # Copy description into title before making title required.
    op.execute(
        "UPDATE expenses SET title = description WHERE title IS NULL"
    )

    op.alter_column(
        "expenses",
        "title",
        nullable=False,
    )

    # Restore description as nullable TEXT.
    op.alter_column(
        "expenses",
        "description",
        existing_type=sa.String(length=500),
        type_=sa.Text(),
        nullable=True,
    )

    op.drop_column("expenses", "notes")
    op.drop_column("expenses", "reference_number")
    op.drop_column("expenses", "payment_method")
