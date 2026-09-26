from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from personal_investor_agent.dependencies import DatabaseSession, ProfileKey
from personal_investor_agent.models.investor_profile import InvestorProfile
from personal_investor_agent.schemas.investor_profile import (
    InvestorProfileInput,
    InvestorProfileResponse,
)

router = APIRouter(
    prefix="/profiles",
    tags=["profiles"],
)


@router.put(
    "/{profile_key}",
    response_model=InvestorProfileResponse,
    status_code=status.HTTP_200_OK,
)
def upsert_profile(
    profile_key: ProfileKey,
    payload: InvestorProfileInput,
    session: DatabaseSession,
) -> InvestorProfile:
    profile = session.scalar(
        select(InvestorProfile).where(InvestorProfile.profile_key == profile_key)
    )

    values = payload.model_dump()

    if profile is None:
        profile = InvestorProfile(
            profile_key=profile_key,
            **values,
        )
    else:
        for field_name, value in values.items():
            setattr(profile, field_name, value)

    session.add(profile)

    try:
        session.commit()
        session.refresh(profile)
    except SQLAlchemyError as error:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not save investor profile",
        ) from error

    return profile


@router.get(
    "/{profile_key}",
    response_model=InvestorProfileResponse,
)
def get_profile(
    profile_key: ProfileKey,
    session: DatabaseSession,
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
