from typing import Optional

import pandas as pd

from src.application.models import predict_model_pipeline
from src.domain.models import ModelsFlat, ModelsRepository
from src.domain.predict import (
    Predict_,
    PredictFlat,
    PredictRepository,
    PredictUncommited,
)
from src.domain.users.entities import UserFlat
from src.infrastructure.application import (
    AuthorizationError,
    BadRequestError,
    NotFoundError,
)
from src.infrastructure.database.services.transactions import transaction


async def create(
    payload: list,
    user: UserFlat,
    data_type: str,
    horizon_id: int,
    pipeline_id: int,
) -> Predict_:
    async with transaction():
        _model: ModelsFlat = await ModelsRepository().get(id_=pipeline_id)
        if _model.user_id != user.id:
            raise AuthorizationError(message="Access denied.")
        if _model.horizon_id != horizon_id:
            raise BadRequestError(message="Association didn't match.")
        if data_type not in ["json"]:
            raise BadRequestError(
                message=f"Can't do prediction from following type: {data_type}"
            )

        df_pred = pd.DataFrame(payload)
        if not df_pred.empty:
            new_data = df_pred.copy()
            _prediction = await predict_model_pipeline(
                new_data=new_data, path=_model.pipeline_route
            )
            if not _prediction:
                raise NotFoundError(
                    message="Prediction pipeline file not found"
                )
            merged_data_list = [
                {"inputs": input_dict, "output": output}
                for input_dict, output in zip(payload, _prediction)
            ]
            repository = PredictRepository()
            predict_flat: PredictFlat = await repository.create(
                PredictUncommited(
                    results=merged_data_list,
                    user_id=user.id,
                    models_id=pipeline_id,
                )
            )
            rich_predict: Predict_ = await repository.get(predict_flat.id)
    return rich_predict


async def get_all(
    user_id: int,
    limit: Optional[int] = None,
    models_id: Optional[int] = None,
) -> list[ModelsFlat]:
    """Get all models from the database."""

    async with transaction():
        return [
            model
            async for model in PredictRepository().all_by_user(
                user_id=user_id,
                limit=limit,
                models_id=models_id,
            )
        ]
