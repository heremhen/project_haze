import platform

import psutil
from fastapi import APIRouter

from src.config import settings
from src.domain.health.repository import HealthRepository
from src.infrastructure.database.services.transactions import transaction
from src.presentation.health.contracts import (
    DiskInfo,
    MemoryInfo,
    StatusResponse,
    SystemInfo,
)

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/", include_in_schema=False)
@router.get("", response_model=StatusResponse)
async def health():
    try:
        """Check if the database is responsive"""
        async with transaction():
            await HealthRepository().ping()
        db_status = "up"
    except Exception as e:
        db_status = str(e)

    """ Get system information """
    system_info = {
        "system": platform.system(),
        "processor": platform.processor(),
        "architecture": platform.architecture(),
        "memory": MemoryInfo(**psutil.virtual_memory()._asdict()),
        "disk": DiskInfo(**psutil.disk_usage("/")._asdict()),
    }

    return StatusResponse(
        **{
            "status": "development" if settings.debug else "active",
            "database": db_status,
            "system_info": SystemInfo(**system_info),
        }
    )
