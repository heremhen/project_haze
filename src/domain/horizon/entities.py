from datetime import datetime
from typing import Optional

from src.infrastructure.application import InternalEntity

__all__ = ("HorizonUncommited", "HorizonFlat")


class _HorizonBase(InternalEntity):
    icon: Optional[str]
    name: Optional[str]
    shared: Optional[bool]
    user_id: int
    disabled: Optional[bool] = False


class HorizonUncommited(_HorizonBase):
    """This schema is used for creating instance in the database."""

    pass


class HorizonFlat(_HorizonBase):
    """Existed horizon representation."""

    id: int
    user_id: Optional[int]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]