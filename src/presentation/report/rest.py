from typing import Optional

from fastapi import APIRouter, Depends, status

from src.application import authentication, report
from src.domain.report import ModelsReport_, ModelsReportFlat
from src.domain.users import UserFlat
from src.infrastructure.application import Response, ResponseMulti

from .contracts import (
    ModelsReportCreateRequestBody,
    ModelsReportPublic,
    ModelsReportPublicEssentials,
)

router = APIRouter(prefix="/report", tags=["Report"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_report(
    schema: ModelsReportCreateRequestBody,
    user: UserFlat = Depends(authentication.get_current_user),
) -> Response[ModelsReportPublic]:
    """Create a new report."""

    _report: ModelsReportFlat = await report.create(
        schema=schema.model_dump(), user_id=user.id
    )
    _report_public = ModelsReportPublic.model_validate(_report)

    return Response[ModelsReportPublic](result=_report_public)


@router.get("/{report_id}", status_code=status.HTTP_200_OK)
async def read_report(
    report_id: int,
    user: UserFlat = Depends(authentication.get_current_user),
) -> Response[ModelsReportPublic]:
    """Read report."""

    _model: ModelsReportFlat = await report.get(
        report_id=report_id,
        user_id=user.id,
    )

    return Response[ModelsReportPublic](result=_model)


@router.get("", status_code=status.HTTP_200_OK)
async def read_all_reports(
    user: UserFlat = Depends(authentication.get_current_user),
    limit: Optional[int] = None,
) -> ResponseMulti[ModelsReportPublicEssentials]:
    """Read report."""

    _report: list[dict] = await report.get_all(
        user_id=user.id,
        limit=limit,
    )
    return ResponseMulti[ModelsReportPublicEssentials](result=_report)


@router.put("/{report_id}", status_code=status.HTTP_200_OK)
async def update_reports(
    report_id,
    user: UserFlat = Depends(authentication.get_current_user),
):
    """Update report."""

    raise NotImplementedError()


@router.delete("/{report_id}", status_code=status.HTTP_200_OK)
async def remove_reports(
    report_id,
    user: UserFlat = Depends(authentication.get_current_user),
):
    """Remove report."""

    raise NotImplementedError()
