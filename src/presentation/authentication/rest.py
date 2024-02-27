from datetime import timedelta

from fastapi import APIRouter, Request, status
from jose import JWTError, jwt

from src.application.authentication.dependency_injection import (
    authenticate_user,
    create_access_token,
    get_user,
)
from src.config import settings
from src.domain.authentication.entities import TokenPayload
from src.infrastructure.application import AuthenticationError, Response
from src.infrastructure.application.errors.entities import NotFoundError

from .contracts import (
    RefreshAccessTokenRequestBody,
    TokenClaimPublic,
    TokenClaimRequestBody,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/token",
    response_model=Response[TokenClaimPublic],
    status_code=status.HTTP_201_CREATED,
)
async def token_claim(
    schema: TokenClaimRequestBody,
) -> Response[TokenClaimPublic]:
    """Claim for access and refresh tokens."""

    try:
        user = await authenticate_user(schema.login, schema.password)
        if not user:
            raise AuthenticationError(message="Incorrect username or password")
        access_token_expires = timedelta(minutes=15)
        access_token = create_access_token(
            data={"sub": user.username},
            expires_delta=access_token_expires,
        )
    except NotFoundError:
        raise AuthenticationError(message="Incorrect username or password")
    return TokenClaimPublic(access_token=access_token, token_type="bearer")


@router.post(
    "/token/refresh",
    response_model=Response[TokenClaimPublic],
    status_code=status.HTTP_201_CREATED,
)
async def token_refresh(
    schema: RefreshAccessTokenRequestBody,
) -> Response[TokenClaimPublic]:
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

    user = await get_user(username=token_data.username)
    if user is None:
        raise AuthenticationError(message="Could not validate credentials")

    access_token_expires = timedelta(minutes=15)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires,
    )

    return TokenClaimPublic(access_token=access_token, token_type="bearer")


# @app.get("/users/me/", response_model=User)
# async def read_users_me(
#     current_user: Annotated[User, Depends(get_current_active_user)]
# ):
#     return current_user


# @app.get("/users/me/items/")
# async def read_own_items(
#     current_user: Annotated[User, Depends(get_current_active_user)]
# ):
#     return [{"item_id": "Foo", "owner": current_user.username}]
