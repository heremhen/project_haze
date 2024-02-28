from fastapi import APIRouter, status

from src.application import users
from src.application.authentication.dependency_injection import (
    get_password_hash,
)
from src.domain.users import UserFlat, UserUncommited
from src.infrastructure.application import Response

from .contracts import UserCreateRequestBody, UserPublic

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def user_registration(
    schema: UserCreateRequestBody,
) -> Response[UserPublic]:
    """Create a new user."""

    schema_dict = schema.model_dump()
    plain_password = schema_dict.pop("password")
    hashed_password = get_password_hash(plain_password)
    _user: UserFlat = await users.create(
        UserUncommited(password=hashed_password, **schema_dict)
    )

    _user_public = UserPublic.model_validate(_user)
    return Response[UserPublic](result=_user_public)
