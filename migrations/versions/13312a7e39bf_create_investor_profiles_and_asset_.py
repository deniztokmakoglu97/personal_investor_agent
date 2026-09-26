"""create investor profiles and asset snapshots

Revision ID: 13312a7e39bf
Revises:
Create Date: 2026-09-27 00:45:31.709815

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "13312a7e39bf"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create investor profile and historical asset snapshot tables."""

    op.create_table(
        "investor_profiles",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("profile_key", sa.String(length=100), nullable=False),
        sa.Column("base_currency", sa.String(length=3), nullable=False),
        sa.Column(
            "primary_objective",
            sa.String(length=100),
            nullable=False,
        ),
        sa.Column(
            "investment_style",
            sa.String(length=100),
            nullable=False,
        ),
        sa.Column(
            "risk_tolerance",
            sa.String(length=50),
            nullable=False,
        ),
        sa.Column("horizon_min_months", sa.Integer(), nullable=False),
        sa.Column("horizon_max_months", sa.Integer(), nullable=False),
        sa.Column(
            "minimum_cash_buffer_pct",
            sa.Numeric(precision=5, scale=2),
            nullable=False,
        ),
        sa.Column(
            "maximum_single_position_pct",
            sa.Numeric(precision=5, scale=2),
            nullable=False,
        ),
        sa.Column(
            "maximum_sector_exposure_pct",
            sa.Numeric(precision=5, scale=2),
            nullable=False,
        ),
        sa.Column(
            "minimum_candidates_screened",
            sa.Integer(),
            server_default=sa.text("10"),
            nullable=False,
        ),
        sa.Column(
            "daily_monitor_enabled",
            sa.Boolean(),
            server_default=sa.text("true"),
            nullable=False,
        ),
        sa.Column(
            "exceptional_alert_min_score",
            sa.Numeric(precision=5, scale=2),
            nullable=False,
        ),
        sa.Column(
            "human_approval_required",
            sa.Boolean(),
            server_default=sa.text("true"),
            nullable=False,
        ),
        sa.Column(
            "automatic_trading_allowed",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.CheckConstraint(
            "horizon_min_months > 0",
            name="ck_investor_profiles_positive_horizon_minimum",
        ),
        sa.CheckConstraint(
            "horizon_max_months >= horizon_min_months",
            name="ck_investor_profiles_valid_horizon_range",
        ),
        sa.CheckConstraint(
            "minimum_cash_buffer_pct BETWEEN 0 AND 100",
            name="ck_investor_profiles_valid_cash_buffer_percentage",
        ),
        sa.CheckConstraint(
            "maximum_single_position_pct BETWEEN 0 AND 100",
            name="ck_investor_profiles_valid_single_position_percentage",
        ),
        sa.CheckConstraint(
            "maximum_sector_exposure_pct BETWEEN 0 AND 100",
            name="ck_investor_profiles_valid_sector_exposure_percentage",
        ),
        sa.CheckConstraint(
            "minimum_candidates_screened >= 10",
            name="ck_investor_profiles_minimum_candidate_count",
        ),
        sa.CheckConstraint(
            "human_approval_required = true",
            name="ck_investor_profiles_human_approval_is_required",
        ),
        sa.CheckConstraint(
            "automatic_trading_allowed = false",
            name="ck_investor_profiles_automatic_trading_is_forbidden",
        ),
        sa.PrimaryKeyConstraint(
            "id",
            name="pk_investor_profiles",
        ),
    )

    op.create_index(
        "ix_investor_profiles_profile_key",
        "investor_profiles",
        ["profile_key"],
        unique=True,
    )

    op.create_table(
        "asset_snapshots",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("profile_id", sa.Uuid(), nullable=False),
        sa.Column(
            "total_net_worth",
            sa.Numeric(precision=20, scale=2),
            nullable=False,
        ),
        sa.Column(
            "investable_assets",
            sa.Numeric(precision=20, scale=2),
            nullable=False,
        ),
        sa.Column(
            "cash_available",
            sa.Numeric(precision=20, scale=2),
            nullable=False,
        ),
        sa.Column("base_currency", sa.String(length=3), nullable=False),
        sa.Column(
            "as_of",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.CheckConstraint(
            "investable_assets >= 0",
            name="ck_asset_snapshots_nonnegative_investable_assets",
        ),
        sa.CheckConstraint(
            "cash_available >= 0",
            name="ck_asset_snapshots_nonnegative_cash_available",
        ),
        sa.CheckConstraint(
            "cash_available <= investable_assets",
            name="ck_asset_snapshots_cash_not_above_investable_assets",
        ),
        sa.ForeignKeyConstraint(
            ["profile_id"],
            ["investor_profiles.id"],
            name="fk_asset_snapshots_profile_id_investor_profiles",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint(
            "id",
            name="pk_asset_snapshots",
        ),
    )

    op.create_index(
        "ix_asset_snapshots_profile_as_of",
        "asset_snapshots",
        ["profile_id", "as_of"],
        unique=False,
    )


def downgrade() -> None:
    """Remove asset snapshot and investor profile tables."""

    op.drop_index(
        "ix_asset_snapshots_profile_as_of",
        table_name="asset_snapshots",
    )
    op.drop_table("asset_snapshots")

    op.drop_index(
        "ix_investor_profiles_profile_key",
        table_name="investor_profiles",
    )
    op.drop_table("investor_profiles")
