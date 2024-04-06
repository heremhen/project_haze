from src.domain.models.entities import ModelsFlat
from src.domain.users import UserFlat

from .entities import PredictFlat

__all__ = ("Predict_",)


class Predict_(PredictFlat):
    """This data predict aggregates information of an predict
    and nested data predict from other domains.
    """

    predict: PredictFlat
    model: ModelsFlat
    user: UserFlat
