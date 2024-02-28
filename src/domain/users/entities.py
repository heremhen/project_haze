from typing import Optional, Union

from src.infrastructure.application import InternalEntity

__all__ = ("UserUncommited", "UserFlat", "UserWithoutPassword")


class UserUncommited(InternalEntity):
    """This schema is used for creating instance in the database."""

    username: str
    password: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserFlat(UserUncommited):
    """Existed user representation."""

    id: int


class UserWithoutPassword(UserFlat):
    """User representation without password."""

    password: Optional[str] = None
