from datetime import UTC, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    computed_field,
    model_validator,
)


def current_utc_time() -> datetime:
    return datetime.now(UTC)


class AssetSnapshotInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    total_assets: Decimal = Field(ge=0)
    total_liabilities: Decimal = Field(ge=0)
    investable_assets: Decimal = Field(ge=0)
    cash_available: Decimal = Field(ge=0)

    as_of: datetime = Field(default_factory=current_utc_time)
    notes: str | None = Field(default=None, max_length=2000)

    @model_validator(mode="after")
    def validate_financial_relationships(self) -> "AssetSnapshotInput":
        if self.investable_assets > self.total_assets:
            raise ValueError("investable_assets cannot exceed total_assets")

        if self.cash_available > self.investable_assets:
            raise ValueError("cash_available cannot exceed investable_assets")

        return self


class AssetSnapshotResponse(AssetSnapshotInput):
    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
    )

    id: UUID
    profile_id: UUID
    base_currency: str
    created_at: datetime

    @computed_field
    @property
    def net_worth(self) -> Decimal:
        return self.total_assets - self.total_liabilities
