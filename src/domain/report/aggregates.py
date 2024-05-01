from typing import Optional

from src.domain.models import ModelsFlat
from src.domain.registry import RegistryFlat
from src.domain.users import UserFlat

from .entities import ModelsReportFlat

__all__ = ("ModelsReport_",)


class ModelsReport_(ModelsReportFlat):
    """This data model aggregates information of an report
    and nested data report from other domains.
    """

    report: ModelsReportFlat
    model: Optional[ModelsFlat]
    registry: RegistryFlat
    user: UserFlat
