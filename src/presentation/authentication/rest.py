from datetime import timedelta

from fastapi import APIRouter, status
from jose import JWTError, jwt

from src.application.authentication.dependency_injection import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
    get_user,
)
from src.config import settings
from src.domain.authentication.entities import TokenPayload
from src.domain.users.entities import UserFlat
from src.infrastructure.application import AuthenticationError, Response
from src.infrastructure.application.errors.entities import NotFoundError

from .contracts import (
    RefreshAccessTokenRequestBody,
    RefreshTokenClaimPublic,
    TokenClaimPublic,
    TokenClaimRequestBody,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/token",
    status_code=status.HTTP_201_CREATED,
)
async def token_claim(
    schema: TokenClaimRequestBody,
) -> Response[TokenClaimPublic]:
    """Claim for access and refresh tokens."""

    try:
        user: UserFlat = await authenticate_user(schema.login, schema.password)
        if not user:
            raise AuthenticationError(message="Incorrect username or password")
        refresh_token_expires = timedelta(days=7)
        refresh_token = create_refresh_token(
            data={"sub": user.username},
            secret_key=settings.authentication.refresh_token.secret_key,
            expires_delta=refresh_token_expires,
        )
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"sub": user.username},
            expires_delta=access_token_expires,
        )
        _tokens = {
            "access": access_token,
            "refresh": refresh_token,
        }
    except NotFoundError:
        raise AuthenticationError(message="Incorrect username or password")

    _tokens_public = TokenClaimPublic.model_validate(_tokens)
    return Response[TokenClaimPublic](result=_tokens_public)


@router.post(
    "/token/refresh",
    status_code=status.HTTP_201_CREATED,
)
async def token_refresh(
    schema: RefreshAccessTokenRequestBody,
) -> Response[RefreshTokenClaimPublic]:
    """Refresh the access token."""

    try:
        payload = jwt.decode(
            schema.refresh,
            settings.authentication.access_token.secret_key,
            algorithms=[settings.authentication.algorithm],
        )
        username: str = payload.get("sub")
        if username is None:
            raise AuthenticationError(message="Could not validate credentials")
        token_data = TokenPayload(sub=username, exp=payload.get("exp"))
    except JWTError:
        raise AuthenticationError(message="Could not validate credentials")

    user = await get_user(username=token_data.sub)
    if user is None:
        raise AuthenticationError(message="Could not validate credentials")

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires,
    )

    _claim_public = RefreshTokenClaimPublic(access=access_token)
    return Response[RefreshTokenClaimPublic](result=_claim_public)
