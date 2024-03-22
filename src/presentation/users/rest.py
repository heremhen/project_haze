from fastapi import APIRouter, Depends, status

from src.application import authentication, users
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


@router.get("", status_code=status.HTTP_200_OK)
async def read_user(user: UserFlat = Depends(authentication.get_current_user)):
    raise NotImplementedError()


@router.put("", status_code=status.HTTP_200_OK)
async def update_user(
    user: UserFlat = Depends(authentication.get_current_user),
):
    raise NotImplementedError()


@router.patch("/change/password", status_code=status.HTTP_200_OK)
async def change_password(
    user: UserFlat = Depends(authentication.get_current_user),
):
    raise NotImplementedError()


@router.patch("/change/username", status_code=status.HTTP_200_OK)
async def change_username(
    user: UserFlat = Depends(authentication.get_current_user),
):
    raise NotImplementedError()


@router.patch("/change/email", status_code=status.HTTP_200_OK)
async def change_email(
    user: UserFlat = Depends(authentication.get_current_user),
):
    raise NotImplementedError()


@router.patch("/change/fullname", status_code=status.HTTP_200_OK)
async def change_fullname(
    user: UserFlat = Depends(authentication.get_current_user),
):
    raise NotImplementedError()


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def remove_account(
    user: UserFlat = Depends(authentication.get_current_user),
):
    raise NotImplementedError()
