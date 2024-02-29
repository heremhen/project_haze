from typing import Optional

from src.domain.registry import RegistryFlat
from src.domain.users import UserFlat

from .entities import ModelsFlat

__all__ = ("Model_",)


class Model_(ModelsFlat):
    """This data model aggregates information of an models
    and nested data models from other domains.
    """

    model: ModelsFlat
    registry: RegistryFlat
    inherited_from: Optional[RegistryFlat]
    user: UserFlat
