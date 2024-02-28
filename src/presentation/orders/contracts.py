from pydantic import Field

from src.infrastructure.application import PublicEntity


class _OrderBase(PublicEntity):
    amount: int = Field(...)
    product_id: int = Field(...)


class OrderCreateRequestBody(_OrderBase):
    """Order create request body."""

    pass


class OrderPublic(_OrderBase):
    """The internal application representation."""

    id: int
