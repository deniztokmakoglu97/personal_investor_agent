from typing import Annotated

from fastapi import Depends, Path
from sqlalchemy.orm import Session

from personal_investor_agent.database import get_database_session

DatabaseSession = Annotated[
    Session,
    Depends(get_database_session),
]

ProfileKey = Annotated[
    str,
    Path(
        min_length=1,
        max_length=100,
        pattern=r"^[a-z0-9_-]+$",
        examples=["default"],
    ),
]
