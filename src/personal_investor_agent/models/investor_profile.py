from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    Integer,
    Numeric,
    String,
    Uuid,
    func,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from personal_investor_agent.models.base import Base


class InvestorProfile(Base):
    __tablename__ = "investor_profiles"
    __table_args__ = (
        CheckConstraint(
            "horizon_min_months > 0",
            name="positive_horizon_minimum",
        ),
        CheckConstraint(
            "horizon_max_months >= horizon_min_months",
            name="valid_horizon_range",
        ),
        CheckConstraint(
            "minimum_cash_buffer_pct BETWEEN 0 AND 100",
            name="valid_cash_buffer_percentage",
        ),
        CheckConstraint(
            "maximum_single_position_pct BETWEEN 0 AND 100",
            name="valid_single_position_percentage",
        ),
        CheckConstraint(
            "maximum_sector_exposure_pct BETWEEN 0 AND 100",
            name="valid_sector_exposure_percentage",
        ),
        CheckConstraint(
            "minimum_candidates_screened >= 10",
            name="minimum_candidate_count",
        ),
        CheckConstraint(
            "human_approval_required = true",
            name="human_approval_is_required",
        ),
        CheckConstraint(
            "automatic_trading_allowed = false",
            name="automatic_trading_is_forbidden",
        ),
    )

    id: Mapped[UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid4,
    )

    profile_key: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
    )

    base_currency: Mapped[str] = mapped_column(String(3))
    primary_objective: Mapped[str] = mapped_column(String(100))
    investment_style: Mapped[str] = mapped_column(String(100))
    risk_tolerance: Mapped[str] = mapped_column(String(50))

    horizon_min_months: Mapped[int] = mapped_column(Integer)
    horizon_max_months: Mapped[int] = mapped_column(Integer)

    minimum_cash_buffer_pct: Mapped[Decimal] = mapped_column(Numeric(5, 2))
    maximum_single_position_pct: Mapped[Decimal] = mapped_column(Numeric(5, 2))
    maximum_sector_exposure_pct: Mapped[Decimal] = mapped_column(Numeric(5, 2))

    minimum_candidates_screened: Mapped[int] = mapped_column(
        Integer,
        default=10,
        server_default=text("10"),
    )

    daily_monitor_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        server_default=text("true"),
    )

    exceptional_alert_min_score: Mapped[Decimal] = mapped_column(Numeric(5, 2))

    human_approval_required: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        server_default=text("true"),
    )

    automatic_trading_allowed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default=text("false"),
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
