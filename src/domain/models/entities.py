from enum import Enum, IntEnum
from typing import List, Optional

from pandas import DataFrame

from src.infrastructure.application import InternalEntity

__all__ = ("TimeBudgetEnum", "ModelsFlat", "ModelsUncommited")


class TimeBudgetEnum(IntEnum):
    """Train time by seconds."""

    quick = 1
    normal = 100
    compact = 500


class PipelineTypeEnum(str, Enum):
    """Train types."""

    classification = "classification"
    regression = "regression"


class _ModelsBase(InternalEntity):
    name: Optional[str]
    description: Optional[str]
    target_attribute: str
    test_size_threshold: Optional[float]
    time_budget: Optional[TimeBudgetEnum]
    pipeline_type: Optional[PipelineTypeEnum]
    version: Optional[float]
    dropped_columns: Optional[List[str]]
    registry_id: int
    inherited_from_id: Optional[int]
    user_id: int


class ModelsUncommited(_ModelsBase):
    """This schema is used for creating instance in the database."""

    pass


class ModelsFlat(_ModelsBase):
    """Existed model representation."""

    id: int

# class AutoMLDeps(InternalEntity):
#     url: str
#     target_attribute: str
#     pipeline_type: str
#     test_size_threshold: float
#     time_budget: Optional[TimeBudgetEnum] = TimeBudgetEnum.normal