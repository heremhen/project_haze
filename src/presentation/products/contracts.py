from pydantic import Field

from src.infrastructure.application import PublicEntity


class _ProductBase(PublicEntity):
    name: str = Field(...)
    price: int = Field(...)


class ProductCreateRequestBody(_ProductBase):
    """Product create request body."""

    pass


class ProductPublic(_ProductBase):
    """The internal application representation."""

    id: int
