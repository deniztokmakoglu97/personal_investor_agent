from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator


class InvestorProfileInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    base_currency: str = Field(
        min_length=3,
        max_length=3,
        pattern=r"^[A-Z]{3}$",
        examples=["USD"],
    )
    primary_objective: str = Field(min_length=1, max_length=100)
    investment_style: str = Field(min_length=1, max_length=100)
    risk_tolerance: str = Field(min_length=1, max_length=50)

    horizon_min_months: int = Field(gt=0)
    horizon_max_months: int = Field(gt=0)

    minimum_cash_buffer_pct: Decimal = Field(ge=0, le=100)
    maximum_single_position_pct: Decimal = Field(ge=0, le=100)
    maximum_sector_exposure_pct: Decimal = Field(ge=0, le=100)

    minimum_candidates_screened: int = Field(default=10, ge=10)
    daily_monitor_enabled: bool = True
    exceptional_alert_min_score: Decimal = Field(ge=0, le=100)

    @model_validator(mode="after")
    def validate_horizon(self) -> "InvestorProfileInput":
        if self.horizon_max_months < self.horizon_min_months:
            raise ValueError(
                "horizon_max_months must be greater than or equal to horizon_min_months"
            )
        return self


class InvestorProfileResponse(InvestorProfileInput):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    profile_key: str
    human_approval_required: bool
    automatic_trading_allowed: bool
    created_at: datetime
    updated_at: datetime
