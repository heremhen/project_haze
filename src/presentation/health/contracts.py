from typing import List

from src.infrastructure.application import PublicEntity


class MemoryInfo(PublicEntity):
    total: int
    available: int
    percent: float
    used: int
    free: int


class DiskInfo(PublicEntity):
    total: int
    used: int
    free: int
    percent: float


class SystemInfo(PublicEntity):
    system: str
    processor: str
    architecture: List[str]
    memory: MemoryInfo
    disk: DiskInfo


class StatusResponse(PublicEntity):
    status: str
    database: str
    system_info: SystemInfo
