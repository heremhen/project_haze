import os
from typing import List, Optional

from fastapi import APIRouter, Depends, File, UploadFile, status
from fastapi.responses import FileResponse

from src.application import authentication, registry
from src.domain.registry.aggregates import Registry
from src.domain.registry.entities import RegistryFlat
from src.domain.users import UserFlat
from src.infrastructure.application import ResponseMulti
from src.infrastructure.application.errors.entities import NotFoundError
from src.presentation.registry.contracts import RegistryPublic

router = APIRouter(prefix="/r", tags=["Files"])


@router.get("/cdn/{dir}", response_class=FileResponse)
async def get_file(name: str):
    """Get a file."""
    path = f"static/public/{name}"
    if not os.path.exists(path):
        raise NotFoundError(message="File not found")
    return FileResponse(path)


@router.get("/my/files")
async def get_own_files(
    user: UserFlat = Depends(authentication.get_current_user),
) -> ResponseMulti[RegistryPublic]:
    """Get user files."""

    _registry: list[RegistryFlat] = await registry.get_all(
        user_id=user.id,
    )

    return ResponseMulti[RegistryPublic](result=_registry)


@router.post("/lines", include_in_schema=False)
async def get_lines(
    file: bytes = File(description="Файл оруулж өгнө үү."),
    user: UserFlat = Depends(authentication.get_current_user),
):
    content = file.decode("utf-8")
    lines = content.split("\n")
    return {"lines": lines}


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def store_uploadfiles(
    path: Optional[str] = "",
    upload_files: List[UploadFile] = File(
        description="Нэг ба түүнээс олон файл оруулж өгнө үү."
    ),
    user: UserFlat = Depends(authentication.get_current_user),
) -> ResponseMulti[RegistryPublic]:
    """Store multiple files."""

    _registry: list[Registry] = await registry.create(
        path=path,
        upload_files=upload_files,
        user_id=user.id,
    )

    for item in _registry:
        RegistryFlat.model_validate(item)

    return ResponseMulti[RegistryPublic](result=_registry)


@router.put("/{registry_id}", status_code=status.HTTP_200_OK)
async def update_stored_files(
    user: UserFlat = Depends(authentication.get_current_user),
):
    raise NotImplementedError()


@router.delete("/{registry_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_files(
    user: UserFlat = Depends(authentication.get_current_user),
):
    raise NotImplementedError()
