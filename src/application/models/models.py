from typing import Optional

from loguru import logger
from pydantic import ValidationError

from src.application import report
from src.application.models.colorful_util import generate_css
from src.application.models.pipeline_utils import (
    auto_ml__,
    calculate_prediction_input_fields,
    generate_report,
    generate_unique_path,
    load_dataset,
)
from src.domain.models import (
    ModelsFlat,
    ModelsRepository,
    ModelsUncommited,
    ModelsUncommitedOptional,
)
from src.domain.models.aggregates import Model_
from src.domain.models.entities import AutoMLDeps, StatusType
from src.domain.registry import RegistryFlat, RegistryRepository
from src.domain.report import ModelsReportRepository, ModelsReportUncommited
from src.domain.users import UserFlat
from src.infrastructure.application import (
    AuthorizationError,
    BadRequestError,
    DatabaseError,
    NotFoundError,
    UnprocessableError,
)
from src.infrastructure.database import transaction


async def get(model_id: int, user_id: int) -> ModelsFlat:
    """Get a model from the database."""

    try:
        async with transaction():
            _model = await ModelsRepository().get(id_=model_id)
            if _model.user_id != user_id:
                raise AuthorizationError(message="Access denied.")
            return _model
    except (DatabaseError, NotFoundError):
        raise NotFoundError(message="Model not found.")


async def get_all(
    user_id: int,
    horizon_id: Optional[int] = None,
    limit: Optional[int] = None,
    status: Optional[str] = None,
) -> list[ModelsFlat]:
    """Get all models from the database."""

    async with transaction():
        return [
            model
            async for model in ModelsRepository().all_by_user(
                user_id=user_id,
                limit=limit,
                status=status,
                horizon_id=horizon_id,
            )
        ]


async def create(
    payload: dict,
    user: UserFlat,
) -> Model_:
    """Create a database record for the model."""

    payload.update(user_id=user.id)
    model_dir: str = generate_unique_path()
    async with transaction():
        data: RegistryFlat = await RegistryRepository().get(
            id_=payload["registry_id"],
        )
        if data.extension != ".csv":
            raise UnprocessableError(
                message="The process only supports `.csv` files."
            )
        try:
            automl_deps = AutoMLDeps(
                dataset_url=data.url,
                target=payload["target_attribute"],
                threshold=payload["test_size_threshold"],
                time_budget=payload["time_budget"],
                pipeline_type=payload["pipeline_type"],
                pipeline_route=model_dir,
            )
        except ValidationError as e:
            raise UnprocessableError(
                message=f"Invalid payload for AutoML: {e}"
            )
        prediction_inputs = calculate_prediction_input_fields(
            data.url, payload["target_attribute"]
        )
        try:
            repository = ModelsRepository()
            model_flat: ModelsFlat = await repository.create(
                ModelsUncommited(
                    **payload,
                    prediction_input_fields=prediction_inputs,
                    pipeline_route=model_dir,
                    css_background=generate_css(),
                    status=StatusType.pending,
                ),
            )
            rich_model: Model_ = await repository.get(model_flat.id)
            train_data = load_dataset(data.url)
            report_schema = await generate_report(
                payload["name"],
                train_data,
                payload["registry_id"],
                rich_model.id,
            )
            schema_final = ModelsReportUncommited(
                **report_schema, user_id=user.id
            )
            repo = ModelsReportRepository()
            report = await repo.create(schema_final)
            auto_ml__.delay(
                deps_dict=automl_deps.model_dump(), model_id=model_flat.id
            )
        except DatabaseError as e:
            raise UnprocessableError(message=f"Could not create model: {e}")

    return rich_model


async def update(
    model_id: int,
    user: UserFlat,
    payload: dict,
) -> Model_:
    """Update a database record for the model."""

    async with transaction():
        try:
            # Fetch the model to be updated
            _model = await ModelsRepository().get(id_=model_id)
            if _model.user_id != user.id:
                raise AuthorizationError(message="Access denied.")

            # Validate payload
            try:
                validated_payload = ModelsUncommitedOptional(**payload)
            except ValidationError as e:
                raise UnprocessableError(
                    message=f"Invalid payload for AutoML: {e}"
                )

            # Update the model
            model_flat: ModelsFlat = await ModelsRepository().update(
                key="id", value=model_id, payload=validated_payload
            )

            # Fetch the updated model
            rich_model: Model_ = await ModelsRepository().get(model_flat.id)

            return rich_model
        except DatabaseError as e:
            raise UnprocessableError(message=f"Could not update model: {e}")
