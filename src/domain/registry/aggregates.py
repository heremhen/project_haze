from src.domain.users import UserFlat

from .entities import RegistryFlat

__all__ = ("Registry",)


class Registry(RegistryFlat):
    """This data model aggregates information of an order
    and nested data models from other domains.
    """

    registry: RegistryFlat
    user: UserFlat
