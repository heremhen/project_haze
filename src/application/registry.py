import os
import shutil
import uuid

from src.domain.registry import (
    RegistryFlat,
    RegistryRepository,
    RegistryUncommited,
)
from src.domain.registry.aggregates import Registry
from src.infrastructure.database import transaction


async def get_all(user_id: int) -> list[RegistryFlat]:
    """Get all registries from the database."""

    async with transaction():
        return [
            registry
            async for registry in RegistryRepository().all_by_user(
                user_id=user_id
            )
        ]


async def create(
    path: str, upload_files: list, user_id: int
) -> list[Registry]:
    """Create a database record for the registry."""

    responses = []
    async with transaction():
        for upload_file in upload_files:
            original_filename, original_extension = os.path.splitext(
                upload_file.filename
            )
            uid = str(uuid.uuid4())
            new_file = f"{uid}{original_extension}"
            save_path = f"static/{path}"
            os.makedirs(save_path, exist_ok=True)
            save_path = os.path.join(save_path, new_file)
            with open(save_path, "w+b") as buffer:
                shutil.copyfileobj(upload_file.file, buffer)
            _registry_dict = {
                "filename": original_filename,
                "uuid": uid,
                "extension": original_extension,
                "type": upload_file.content_type,
                "url": f"{path}{new_file}",
                "user_id": user_id,
            }
            _registry: Registry = await RegistryRepository().create(
                RegistryUncommited(**_registry_dict)
            )
            responses.append(_registry)
    return responses
