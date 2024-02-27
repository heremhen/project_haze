from typing import List

from src.infrastructure.application import PublicEntity


class MemoryInfo(PublicEntity):
    """The system's memory information."""

    total: int
    available: int
    percent: float
    used: int
    free: int


class DiskInfo(PublicEntity):
    """The system's disk drive information."""

    total: int
    used: int
    free: int
    percent: float


class SystemInfo(PublicEntity):
    """Servers general system information."""

    system: str
    processor: str
    architecture: List[str]
    memory: MemoryInfo
    disk: DiskInfo


class StatusResponse(PublicEntity):
    """Health status of up and running system."""

    status: str
    database: str
    system_info: SystemInfo
