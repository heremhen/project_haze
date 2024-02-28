from typing import Optional

from pydantic.config import ConfigDict

from src.infrastructure.application import PublicEntity


class _UserBase(PublicEntity):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None


class UserCreateRequestBody(_UserBase):
    """User create request body."""

    password: str
    model_config = ConfigDict(extra="forbid")


class UserPublic(_UserBase):
    """The internal application representation."""

    id: int
    model_config = ConfigDict(extra="forbid")
