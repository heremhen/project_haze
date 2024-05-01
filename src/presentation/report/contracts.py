from datetime import datetime
from typing import Optional

from pydantic import Field

from src.infrastructure.application import PublicEntity


class _ModelsReportBase(PublicEntity):
    analysis: Optional[dict | list | str] = Field(default={})
    time_index_analysis: Optional[dict | list | str] = Field(default="None")
    table: Optional[dict | list | str] = Field(default={})
    variables: Optional[dict | list | str] = Field(default={})
    scatter: Optional[dict | list | str] = Field(default={})
    correlations: Optional[dict | list | str] = Field(default={})
    missing: Optional[dict | list | str] = Field(default={})
    alerts: Optional[dict | list | str] = Field(default=[])
    sample: Optional[dict | list | str] = Field(default=[])
    duplicates: Optional[dict | list | str] = Field(default="None")
    report_route: Optional[str] = Field(default=None)
    models_id: Optional[int]
    registry_id: int


class ModelsReportCreateRequestBody(_ModelsReportBase):
    """Report create request body."""

    pass


class ModelsReportPublic(_ModelsReportBase):
    """The internal application representation."""

    id: int
    disabled: bool
    created_at: datetime
    updated_at: datetime


class ModelsReportPublicEssentials(PublicEntity):
    """The internal application representation only essentials."""

    id: int
    report_route: Optional[str]
    models_id: Optional[int]
    registry_id: int
    model_name: Optional[str]
    registry_name: Optional[str]
    disabled: bool
    created_at: datetime
    updated_at: datetime
