from pydantic import Field

from src.infrastructure.application import PublicEntity


class _RegistryBase(PublicEntity):
    filename: str = Field(...)
    uuid: str = Field(...)
    extension: str = Field(...)
    type: str = Field(...)
    url: str = Field(...)


class RegistryCreateRequestBody(PublicEntity):
    """Registry create request body."""

    pass


class RegistryPublic(_RegistryBase):
    """The internal application representation."""

    id: int
