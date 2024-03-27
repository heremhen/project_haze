from datetime import datetime
from enum import Enum, IntEnum
from typing import List, Optional

from src.infrastructure.application import InternalEntity

__all__ = (
    "TimeBudgetEnum",
    "ModelsFlat",
    "ModelsUncommited",
    "StatusType",
    "PipelineTypeEnum",
    "AutoMLDeps",
    "ModelsUncommitedOptional",
)


class TimeBudgetEnum(IntEnum):
    """Train time by seconds."""

    quick = 1
    normal = 100
    compact = 500


class PipelineTypeEnum(str, Enum):
    """Train types."""

    classification = "classification"
    regression = "regression"


class StatusType(str, Enum):
    """Status types."""

    pending = "PENDING"
    failed = "FAILED"
    success = "SUCCESS"


class _ModelsBase(InternalEntity):
    name: Optional[str]
    description: Optional[str]
    target_attribute: str
    test_size_threshold: Optional[float]
    time_budget: Optional[TimeBudgetEnum]
    pipeline_type: PipelineTypeEnum
    pipeline_route: Optional[str] = None
    css_background: Optional[str]
    version: Optional[float]
    dropped_columns: Optional[List[str]]
    status: Optional[StatusType] = None
    prediction_input_fields: Optional[dict]
    registry_id: int
    inherited_from_id: Optional[int]
    user_id: int
    horizon_id: int
    disabled: Optional[bool] = False


class ModelsUncommited(_ModelsBase):
    """This schema is used for creating instance in the database."""

    pass


class ModelsUncommitedOptional(_ModelsBase):
    """This schema is used for creating instance in the database."""

    target_attribute: Optional[str]
    pipeline_type: Optional[PipelineTypeEnum]
    pipeline_route: Optional[str]
    status: Optional[StatusType]
    registry_id: Optional[int]
    user_id: Optional[int]
    horizon_id: Optional[int]
    disabled: Optional[bool]


class ModelsFlat(_ModelsBase):
    """Existed model representation."""

    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class AutoMLDeps(InternalEntity):
    dataset_url: str
    target: str
    pipeline_type: str
    threshold: float
    time_budget: Optional[TimeBudgetEnum] = TimeBudgetEnum.normal
    pipeline_route: str
