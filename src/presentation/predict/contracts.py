from datetime import datetime
from typing import List, Optional

from pydantic import Field

from src.infrastructure.application import PublicEntity


class _PredictBase(PublicEntity):
    pass


class PredictCreateRequestBody(_PredictBase):
    """Predict create request body."""

    data: List[dict]


class PredictPublic(_PredictBase):
    """The internal application representation."""

    id: int
    disabled: bool
    created_at: datetime
    updated_at: datetime
    results: Optional[List] = Field(...)
