from fastapi import FastAPI, HTTPException
from sqlalchemy.exc import SQLAlchemyError

from personal_investor_agent.database import check_database_connection
from personal_investor_agent.routers.asset_snapshots import (
    router as asset_snapshots_router,
)
from personal_investor_agent.routers.investor_profiles import (
    router as investor_profiles_router,
)

app = FastAPI(
    title="Personal Investor Agent API",
    version="0.1.0",
)
app.include_router(investor_profiles_router)
app.include_router(asset_snapshots_router)


@app.get("/health", tags=["system"])
def health_check() -> dict[str, str]:
    return {"status": "healthy"}


@app.get("/ready", tags=["system"])
def readiness_check() -> dict[str, str]:
    try:
        check_database_connection()
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=503,
            detail="Database unavailable",
        ) from error

    return {
        "status": "ready",
        "database": "connected",
    }
