from typing import List, Optional
from pydantic import Field
from src.domain.models.entities import TimeBudgetEnum

from src.infrastructure.application import InternalEntity


class _ModelsBase(InternalEntity):
    name: Optional[str] = Field(default="CH4NGE ME")
    description: Optional[str] = Field(default=None)
    target_attribute: str = Field(...)
    test_size_threshold: Optional[float] = Field(ge=0.1, le=0.9, default=0.3)
    dropped_columns: Optional[List[str]] = Field(default=[])
    time_budget: Optional[TimeBudgetEnum] = Field(default=TimeBudgetEnum.normal)
    version: Optional[float] = Field(default=1.0)
    registry_id: int = Field(...)
    inherited_from_id: Optional[int] = Field(default=None)
    pipeline_type_id: int = Field(...)


class ModelsCreateRequestBody(_ModelsBase):
    """Models create request body."""

    pass


class ModelsPublic(_ModelsBase):
    """The internal application representation."""

    id: int
