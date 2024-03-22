from src.domain.users import UserFlat

from .entities import HorizonFlat

__all__ = ("Horizon_",)


class Horizon_(HorizonFlat):
    """This data model aggregates information of an models
    and nested data models from other domains.
    """

    horizon: HorizonFlat
    user: UserFlat
