from enum import IntEnum

from pydantic import Field

from src.infrastructure.application import PublicEntity

__all__ = ("TimeBudgetEnum", "ModelsFlat", "ModelsUncommited")


class TimeBudgetEnum(IntEnum):
    quick = 1
    normal = 100
    compact = 500


class _ModelsBase(PublicEntity):
    name: str = Field(...)
    description: str = Field(...)
    target_attribute: str = Field(...)
    test_size_threshold: float = Field(...)
    dropped_columns = Field(...)
    time_budget: int = Field(...)
    version: float = Field(...)
    registry_id: int = Field(...)
    inherited_from: int = Field(...)


class ModelsUncommited(_ModelsBase):
    """This schema is used for creating instance in the database."""

    pass


class ModelsFlat(_ModelsBase):
    """Existed model representation."""

    id: int
