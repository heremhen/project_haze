from typing import List, Optional

from pydantic import Field

from src.infrastructure.application import PublicEntity
from src.presentation.models.contracts import ModelsPublicEssentials


class _HorizonBase(PublicEntity):
    icon: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default="My Horizon")
    shared: Optional[bool] = Field(default=False)


class HorizonCreateRequestBody(_HorizonBase):
    """Horizon create request body."""

    pass


class HorizonsPublic(_HorizonBase):
    """The internal application representation."""

    id: int


class HorizonPublic(HorizonsPublic):
    """The internal application representation."""

    models: Optional[List[ModelsPublicEssentials]]
