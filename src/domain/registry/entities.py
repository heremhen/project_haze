from datetime import datetime
from typing import Optional

from pydantic import Field

from src.infrastructure.application import InternalEntity

__all__ = ("RegistryUncommited", "RegistryFlat")


# Internal models
# ------------------------------------------------------
class _RegistryBase(InternalEntity):
    filename: str
    uuid: str
    extension: str
    type: str
    url: str
    user_id: int
    disabled: Optional[bool] = False


class RegistryUncommited(_RegistryBase):
    """This schema is used for creating instance in the database."""

    pass


class RegistryFlat(_RegistryBase):
    """Database record representation."""

    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
