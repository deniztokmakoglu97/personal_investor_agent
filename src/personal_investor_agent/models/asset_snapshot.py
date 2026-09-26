from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Numeric,
    String,
    Text,
    Uuid,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from personal_investor_agent.models.base import Base


class AssetSnapshot(Base):
    __tablename__ = "asset_snapshots"
    __table_args__ = (
        CheckConstraint(
            "total_assets >= 0",
            name="nonnegative_total_assets",
        ),
        CheckConstraint(
            "total_liabilities >= 0",
            name="nonnegative_total_liabilities",
        ),
        CheckConstraint(
            "investable_assets >= 0",
            name="nonnegative_investable_assets",
        ),
        CheckConstraint(
            "investable_assets <= total_assets",
            name="investable_assets_not_above_total_assets",
        ),
        CheckConstraint(
            "cash_available >= 0",
            name="nonnegative_cash_available",
        ),
        CheckConstraint(
            "cash_available <= investable_assets",
            name="cash_not_above_investable_assets",
        ),
        Index(
            "ix_asset_snapshots_profile_as_of",
            "profile_id",
            "as_of",
        ),
    )

    id: Mapped[UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid4,
    )

    profile_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey(
            "investor_profiles.id",
            ondelete="RESTRICT",
        ),
    )

    total_assets: Mapped[Decimal] = mapped_column(Numeric(20, 2))

    total_liabilities: Mapped[Decimal] = mapped_column(Numeric(20, 2))

    investable_assets: Mapped[Decimal] = mapped_column(Numeric(20, 2))

    cash_available: Mapped[Decimal] = mapped_column(Numeric(20, 2))

    base_currency: Mapped[str] = mapped_column(String(3))

    as_of: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
