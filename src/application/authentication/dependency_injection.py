from datetime import datetime, timedelta, timezone
from typing import Annotated, Union

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import ValidationError

from src.config import settings
from src.domain.authentication import TokenPayload
from src.domain.users import UserFlat, UsersRepository
from src.infrastructure.application import AuthenticationError, BadRequestError
from src.infrastructure.database import transaction

__all__ = ("authenticate_user", "get_current_user", "get_current_active_user")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_oauth = OAuth2PasswordBearer(
    tokenUrl="/auth/openapi",
    scheme_name=settings.authentication.scheme,
)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def get_user(username: str):
    async with transaction() as session:
        user = await UsersRepository().get_by_username(username_=username)
    return user


async def authenticate_user(username: str, password: str):
    user = await get_user(username)
    if not user or not verify_password(password, user.password):
        return False
    return user


def create_access_token(
    data: dict, expires_delta: Union[timedelta, None] = None
):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.authentication.access_token.secret_key,
        algorithm=settings.authentication.algorithm,
    )
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_oauth)) -> UserFlat:
    try:
        payload = jwt.decode(
            token,
            settings.authentication.access_token.secret_key,
            algorithms=[settings.authentication.algorithm],
        )
        token_payload = TokenPayload(**payload)

        if datetime.fromtimestamp(token_payload.exp) < datetime.now():
            raise AuthenticationError
    except (JWTError, ValidationError):
        raise AuthenticationError

    async with transaction():
        user = await UsersRepository().get(id_=token_payload.sub)

    # TODO: Check if the token is in the blacklist

    return user


async def get_current_active_user(
    current_user: Annotated[UserFlat, Depends(get_current_user)]
):
    if current_user.disabled:
        raise BadRequestError(message="Inactive user")
    return current_user
