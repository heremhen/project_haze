import pandas as pd

from src.application.models.colorful_util import generate_css
from src.application.models.pipeline_utils import (
    auto_ml__,
    calculate_prediction_input_fields,
)
from src.domain.models import ModelsFlat, ModelsRepository, ModelsUncommited
from src.domain.models.aggregates import Model_
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

    async with transaction():
        data: RegistryFlat = await RegistryRepository().get(
            id_=payload["registry_id"],
        )
        if data.extension == ".csv":
            dataset = pd.read_csv(f"static/{data.url}")
        else:
            raise UnprocessableError(
                message="The process only supports `.csv` files."
            )
        pipeline_route = await auto_ml__(
            train_data=dataset,
            target=payload["target_attribute"],
            threshold=payload["test_size_threshold"],
            time_budget=payload["time_budget"],
            pipeline_type=payload["pipeline_type"],
        )
        prediction_inputs = calculate_prediction_input_fields(
            dataset, payload["target_attribute"]
        )

        repository = ModelsRepository()
        model_flat: ModelsFlat = await repository.create(
            ModelsUncommited(
                **payload,
                prediction_input_fields=prediction_inputs,
                pipeline_route=pipeline_route,
                css_background=generate_css(),
            ),
        )
        rich_model: Model_ = await repository.get(model_flat.id)

    return rich_model
