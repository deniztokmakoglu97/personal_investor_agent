from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from personal_investor_agent.dependencies import DatabaseSession, ProfileKey
from personal_investor_agent.models.asset_snapshot import AssetSnapshot
from personal_investor_agent.models.investor_profile import InvestorProfile
from personal_investor_agent.schemas.asset_snapshot import (
    AssetSnapshotInput,
    AssetSnapshotResponse,
)

router = APIRouter(
    prefix="/profiles/{profile_key}/asset-snapshots",
    tags=["asset snapshots"],
)


def get_profile_or_404(
    profile_key: str,
    session: Session,
) -> InvestorProfile:
    profile = session.scalar(
        select(InvestorProfile).where(InvestorProfile.profile_key == profile_key)
    )

    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Investor profile not found",
        )

    return profile


@router.post(
    "",
    response_model=AssetSnapshotResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_asset_snapshot(
    profile_key: ProfileKey,
    payload: AssetSnapshotInput,
    session: DatabaseSession,
) -> AssetSnapshot:
    profile = get_profile_or_404(profile_key, session)

    snapshot = AssetSnapshot(
        profile_id=profile.id,
        base_currency=profile.base_currency,
        **payload.model_dump(),
    )

    session.add(snapshot)

    try:
        session.commit()
        session.refresh(snapshot)
    except SQLAlchemyError as error:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not save asset snapshot",
        ) from error

    return snapshot


@router.get(
    "/latest",
    response_model=AssetSnapshotResponse,
)
def get_latest_asset_snapshot(
    profile_key: ProfileKey,
    session: DatabaseSession,
) -> AssetSnapshot:
    profile = get_profile_or_404(profile_key, session)

    snapshot = session.scalar(
        select(AssetSnapshot)
        .where(AssetSnapshot.profile_id == profile.id)
        .order_by(
            AssetSnapshot.as_of.desc(),
            AssetSnapshot.created_at.desc(),
        )
        .limit(1)
    )

    if snapshot is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No asset snapshots found",
        )

    return snapshot
