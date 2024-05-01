from datetime import datetime
from typing import Optional

from src.infrastructure.application import InternalEntity

__all__ = ("ModelsReportFlat", "ModelsReportUncommited")


class _ModelsReportBase(InternalEntity):
    analysis: Optional[dict | list | str] = None
    time_index_analysis: Optional[dict | list | str] = None
    table: Optional[dict | list | str] = None
    variables: Optional[dict | list | str] = None
    scatter: Optional[dict | list | str] = None
    correlations: Optional[dict | list | str] = None
    missing: Optional[dict | list | str] = None
    alerts: Optional[dict | list | str] = None
    sample: Optional[dict | list | str] = None
    duplicates: Optional[dict | list | str] = None
    report_route: Optional[str] = None
    registry_id: int
    user_id: int
    models_id: Optional[int] = None
    disabled: Optional[bool] = False


class ModelsReportUncommited(_ModelsReportBase):
    """This schema is used for creating instance in the database."""

    pass


class ModelsReportFlat(_ModelsReportBase):
    """Existed model representation."""

    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
