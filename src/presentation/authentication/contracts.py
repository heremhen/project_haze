from pydantic import Field

from src.infrastructure.application import PublicEntity


class TokenClaimRequestBody(PublicEntity):
    login: str = Field(...)
    password: str = Field(...)


class RefreshAccessTokenRequestBody(PublicEntity):
    refresh: str = Field(...)


class TokenClaimPublic(PublicEntity):
    access: str = Field(...)
    refresh: str = Field(...)


class RefreshTokenClaimPublic(PublicEntity):
    access: str = Field(...)
