from typing import Optional

from pydantic import Field

from src.infrastructure.application import PublicEntity


class _HorizonBase(PublicEntity):
    icon: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default="My Horizon")
    shared: Optional[bool] = Field(default=False)


class HorizonCreateRequestBody(_HorizonBase):
    """Horizon create request body."""

    pass


class HorizonPublic(_HorizonBase):
    """The internal application representation."""

    id: int
