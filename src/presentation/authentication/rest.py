from datetime import timedelta
from fastapi import APIRouter, Request, status

from src.application.authentication.dependency_injection import (
    authenticate_user,
    create_access_token,
)
from src.infrastructure.application import Response, AuthenticationError
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
    request: Request,
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
    request: Request,
    schema: RefreshAccessTokenRequestBody,
) -> Response[TokenClaimPublic]:
    """Refresh the access token."""

    # 🔗 https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
    raise NotImplementedError


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
