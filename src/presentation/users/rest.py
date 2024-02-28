from fastapi import APIRouter, Request, status

from src.application.authentication.dependency_injection import (
    get_password_hash,
)
from src.domain.users import UserFlat
from src.domain.users.entities import UserUncommited
from src.domain.users.repository import UsersRepository
from src.infrastructure.application import Response
from src.infrastructure.application.errors.entities import (
    BadRequestError,
    DatabaseError,
)

from .contracts import UserCreateRequestBody, UserPublic

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def user_registration(
    schema: UserCreateRequestBody,
) -> Response[UserPublic]:
    """Create a new user."""

    try:
        schema_dict = schema.model_dump()
        plain_password = schema_dict.pop("password")
        hashed_password = get_password_hash(plain_password)
        _user: UserFlat = await UsersRepository().create(
            UserUncommited(password=hashed_password, **schema_dict)
        )
    except DatabaseError:
        raise BadRequestError(message="Username or email has already taken.")

    _user_public = UserPublic.model_validate(_user)
    return Response[UserPublic](result=_user_public)
