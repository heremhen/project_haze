from typing import Optional

from src.domain.report import (
    ModelsReport_,
    ModelsReportFlat,
    ModelsReportRepository,
    ModelsReportUncommited,
)
from src.domain.registry import RegistryRepository
from src.domain.models import ModelsRepository
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


async def get_all(user_id: int, limit: Optional[int] = None) -> list[dict]:
    async with transaction():
        report_repo = ModelsReportRepository()
        registry_repo = RegistryRepository()
        models_repo = ModelsRepository()

        reports = []
        async for report in report_repo.all_by_user(user_id, limit):
            model = await models_repo.get(report.models_id)
            registry = await registry_repo.get(report.registry_id)

            report_dict = report.__dict__
            report_dict.update(
                {"model_name": model.name, "registry_name": registry.filename}
            )
            reports.append(report_dict)

        return reports
