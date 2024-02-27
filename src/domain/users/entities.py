from typing import Union

from src.infrastructure.application import InternalEntity

__all__ = ("UserUncommited", "UserFlat")


class UserUncommited(InternalEntity):
    """This schema is used for creating instance in the database."""

    username: str
    password: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


class UserFlat(UserUncommited):
    """Existed product representation."""

    id: int
