from pydantic import ValidationError

from src.application.models.colorful_util import generate_css
from src.application.models.pipeline_utils import (
    auto_ml__,
    calculate_prediction_input_fields,
    generate_unique_path,
)
from src.domain.models import ModelsFlat, ModelsRepository, ModelsUncommited
from src.domain.models.aggregates import Model_
from src.domain.models.entities import AutoMLDeps
from src.domain.registry import RegistryFlat, RegistryRepository
from src.domain.users import UserFlat
from src.infrastructure.application.errors.entities import UnprocessableError
from src.infrastructure.database import transaction


async def get_all() -> list[ModelsFlat]:
    """Get all models from the database."""

    async with transaction():
        return [model async for model in ModelsRepository().all()]


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
        auto_ml_task = auto_ml__.delay(deps_dict=automl_deps.model_dump())
        prediction_inputs = calculate_prediction_input_fields(
            data.url, payload["target_attribute"]
        )
        repository = ModelsRepository()
        model_flat: ModelsFlat = await repository.create(
            ModelsUncommited(
                **payload,
                prediction_input_fields=prediction_inputs,
                pipeline_route=model_dir,
                css_background=generate_css(),
            ),
        )
        rich_model: Model_ = await repository.get(model_flat.id)

    return rich_model
