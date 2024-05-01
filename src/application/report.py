from typing import Optional

from src.domain.report import (
    ModelsReportFlat,
    ModelsReportRepository,
    ModelsReportUncommited,
)
from src.domain.users.entities import UserFlat
from src.infrastructure.application import AuthorizationError
from src.infrastructure.database import transaction


async def create(schema: dict, user_id: int) -> ModelsReportFlat:
    schema_final = ModelsReportUncommited(**schema, user_id=user_id)
    async with transaction():
        repo = ModelsReportRepository()
        report = await repo.create(schema_final)
        return report


async def get(
    report_id: int,
    user_id: int,
) -> ModelsReportFlat:
    async with transaction():
        repo = ModelsReportRepository()
        report = await repo.get(report_id)
        if report.user_id != user_id:
            raise AuthorizationError(message="Access denied.")
        return report


async def get_all(
    user_id: int, limit: Optional[int] = None
) -> list[ModelsReportFlat]:
    async with transaction():
        repo = ModelsReportRepository()
        reports = [report async for report in repo.all_by_user(user_id, limit)]
        return reports
