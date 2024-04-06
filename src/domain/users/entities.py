from datetime import datetime
from typing import Optional

from pydantic import Field

from src.infrastructure.application import InternalEntity

__all__ = ("UserUncommited", "UserFlat")


class UserUncommited(InternalEntity):
    """This schema is used for creating instance in the database."""

    username: str
    password: str
    email: str
    full_name: Optional[str]
    disabled: Optional[bool] = False


class UserFlat(UserUncommited):
    """Existed user representation."""

    id: int
    password: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
