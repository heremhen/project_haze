from typing import Optional

from pydantic import Field
from pydantic.config import ConfigDict

from src.infrastructure.application import InternalEntity


class _UserBase(InternalEntity):
    username: str
    email: str
    full_name: Optional[str] = Field(default=None)


class UserCreateRequestBody(_UserBase):
    """User create request body."""

    password: str
    model_config = ConfigDict(extra="forbid")


class UserPublic(_UserBase):
    """The internal application representation."""

    id: int
    model_config = ConfigDict(extra="forbid")
