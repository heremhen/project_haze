from enum import IntEnum
from typing import List, Optional

from src.infrastructure.application import InternalEntity

__all__ = ("TimeBudgetEnum", "ModelsFlat", "ModelsUncommited")


class TimeBudgetEnum(IntEnum):
    """Train time by seconds."""

    quick = 1
    normal = 100
    compact = 500


class _ModelsBase(InternalEntity):
    name: Optional[str]
    description: Optional[str]
    target_attribute: str
    test_size_threshold: Optional[float]
    dropped_columns: Optional[List[str]]
    time_budget: Optional[TimeBudgetEnum]
    version: Optional[float]
    registry_id: int
    inherited_from_id: Optional[int]
    pipeline_type_id: int
    user_id: int


class ModelsUncommited(_ModelsBase):
    """This schema is used for creating instance in the database."""

    pass


class ModelsFlat(_ModelsBase):
    """Existed model representation."""

    id: int
