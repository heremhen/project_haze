from typing import Optional, Union

from src.infrastructure.application import InternalEntity

__all__ = ("UserUncommited", "UserFlat")


class UserUncommited(InternalEntity):
    """This schema is used for creating instance in the database."""

    username: str
    password: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserFlat(UserUncommited):
    """Existed product representation."""

    id: int
