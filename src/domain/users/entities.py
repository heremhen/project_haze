from typing import Optional

from pydantic import Field

from src.infrastructure.application import InternalEntity

__all__ = ("UserUncommited", "UserFlat", "UserWithoutPassword")


class UserUncommited(InternalEntity):
    """This schema is used for creating instance in the database."""

    username: str
    password: str
    email: Optional[str]
    full_name: Optional[str]
    disabled: Optional[bool]


class UserFlat(UserUncommited):
    """Existed user representation."""

    id: int


class UserWithoutPassword(UserFlat):
    """User representation without password."""

    password: Optional[str] = None
