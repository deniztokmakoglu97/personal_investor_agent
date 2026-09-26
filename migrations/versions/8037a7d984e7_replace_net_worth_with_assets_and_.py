"""replace net worth with assets and liabilities

Revision ID: 8037a7d984e7
Revises: 13312a7e39bf
Create Date: 2026-09-27 01:17:38.795058

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "8037a7d984e7"
down_revision: str | Sequence[str] | None = "13312a7e39bf"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Store assets and liabilities instead of a manually entered net worth."""

    op.alter_column(
        "asset_snapshots",
        "total_net_worth",
        new_column_name="total_assets",
        existing_type=sa.Numeric(precision=20, scale=2),
        existing_nullable=False,
    )

    op.add_column(
        "asset_snapshots",
        sa.Column(
            "total_liabilities",
            sa.Numeric(precision=20, scale=2),
            server_default=sa.text("0"),
            nullable=False,
        ),
    )

    op.alter_column(
        "asset_snapshots",
        "total_liabilities",
        server_default=None,
    )

    op.create_check_constraint(
        "ck_asset_snapshots_nonnegative_total_assets",
        "asset_snapshots",
        "total_assets >= 0",
    )

    op.create_check_constraint(
        "ck_asset_snapshots_nonnegative_total_liabilities",
        "asset_snapshots",
        "total_liabilities >= 0",
    )

    op.create_check_constraint(
        "ck_asset_snapshots_investable_assets_not_above_total_assets",
        "asset_snapshots",
        "investable_assets <= total_assets",
    )


def downgrade() -> None:
    """Restore the earlier net-worth-only representation."""

    op.drop_constraint(
        "ck_asset_snapshots_investable_assets_not_above_total_assets",
        "asset_snapshots",
        type_="check",
    )

    op.drop_constraint(
        "ck_asset_snapshots_nonnegative_total_liabilities",
        "asset_snapshots",
        type_="check",
    )

    op.drop_constraint(
        "ck_asset_snapshots_nonnegative_total_assets",
        "asset_snapshots",
        type_="check",
    )

    op.drop_column(
        "asset_snapshots",
        "total_liabilities",
    )

    op.alter_column(
        "asset_snapshots",
        "total_assets",
        new_column_name="total_net_worth",
        existing_type=sa.Numeric(precision=20, scale=2),
        existing_nullable=False,
    )
