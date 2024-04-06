from datetime import datetime
from typing import List, Optional

from src.infrastructure.application import InternalEntity

__all__ = ("PredictFlat", "PredictUncommited", "PredictUncommitedOptional")


class _PredictBase(InternalEntity):
    results: Optional[List]
    user_id: int
    models_id: int
    disabled: Optional[bool] = False


class PredictUncommited(_PredictBase):
    """This schema is used for creating instance in the database."""

    pass


class PredictUncommitedOptional(_PredictBase):
    """This schema is used for creating instance in the database."""

    user_id: Optional[int]
    models_id: Optional[int]
    disabled: Optional[bool]


class PredictFlat(_PredictBase):
    """Existed model representation."""

    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
