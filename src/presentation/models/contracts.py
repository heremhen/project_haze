from datetime import datetime
from typing import List, Optional

from pydantic import Field

from src.domain.models import PipelineTypeEnum, StatusType, TimeBudgetEnum
from src.infrastructure.application import PublicEntity


class _ModelsBase(PublicEntity):
    name: Optional[str] = Field(default="CH4NGE ME")
    description: Optional[str] = Field(default=None)
    target_attribute: str = Field(...)
    test_size_threshold: Optional[float] = Field(ge=0.1, le=0.9, default=0.2)
    time_budget: Optional[TimeBudgetEnum] = Field(
        default=TimeBudgetEnum.normal
    )
    pipeline_type: Optional[PipelineTypeEnum] = Field(
        default=PipelineTypeEnum.auto
    )
    version: Optional[float] = Field(default=1.0)
    dropped_columns: Optional[List[str]] = Field(default=[])
    registry_id: int = Field(...)
    inherited_from_id: Optional[int] = Field(default=None)
    horizon_id: int = Field(...)


class ModelsCreateRequestBody(_ModelsBase):
    """Models create request body."""

    pass


class ModelsPublic(_ModelsBase):
    """The internal application representation."""

    id: int
    status: Optional[StatusType]
    disabled: bool
    created_at: datetime
    updated_at: datetime
    css_background: Optional[str]
    prediction_input_fields: Optional[dict]


class ModelsPublicEssentials(PublicEntity):
    """The internal application representation only essentials."""

    id: int
    name: str
    description: Optional[str]
    pipeline_type: PipelineTypeEnum
    status: Optional[StatusType]
    version: Optional[float]
    css_background: Optional[str]
    horizon_id: int
    created_at: datetime
    updated_at: datetime
