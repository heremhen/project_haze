import os
import shutil
import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, File, UploadFile, status
from fastapi.responses import FileResponse

from src.application import authentication, registry
from src.domain.registry.entities import RegistryFlat, RegistryUncommited
from src.domain.users import UserFlat
from src.infrastructure.application import Response, ResponseMulti
from src.infrastructure.application.errors.entities import NotFoundError
from src.presentation.registry.contracts import RegistryPublic

router = APIRouter(prefix="/r", tags=["Registry"])


@router.get("/cdn/{name}", response_class=FileResponse)
def get_file(
    name: str,
    user: UserFlat = Depends(authentication.get_current_user),
):
    path = f"static/public/{name}"
    if not os.path.exists(path):
        raise NotFoundError(message="File not found")
    return FileResponse(path)


@router.post("/lines", include_in_schema=False)
def get_lines(
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

    _registry: list[RegistryFlat] = await registry.create(
        path, upload_files, user.id
    )

    return ResponseMulti[RegistryPublic](result=_registry)
