import locale
import os
import pickle
import uuid
import warnings
from typing import Optional, Union

from flaml import AutoML
from sklearn.model_selection import train_test_split

from src.domain.models.entities import TimeBudgetEnum
from src.infrastructure.application.errors.entities import NotFoundError

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.simplefilter(action="ignore", category=FutureWarning)
warnings.simplefilter(action="ignore", category=UserWarning)

__all__ = (
    "save_model_pipeline",
    "auto_ml__",
    "predict_model_pipeline",
    "calculate_prediction_input_fields",
)


async def save_model_pipeline(automl) -> Union[str, None]:
    """Saves the dataset trained file in the storage."""
    # TODO: It's not recommended to save files locally like this

    directory = "static/pipelines"
    path = f"{directory}/{str(uuid.uuid4())}.pkl"

    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(path, "wb") as f:
        pickle.dump(automl, f, pickle.HIGHEST_PROTOCOL)

    return path[len("static/") :]


async def auto_ml__(
    train_data,
    target: str,
    pipeline_type: str,
    threshold: float,
    time_budget: Optional[TimeBudgetEnum] = TimeBudgetEnum.normal,
) -> str:
    """Trains model based on the dataset."""

    X = train_data.drop([target], axis=1)
    y = train_data[target]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=threshold, random_state=42
    )
    automl = AutoML()
    if pipeline_type == "regression":
        automl_settings = {
            "time_budget": time_budget,
            "metric": "r2",
            "task": "regression",
        }
    else:
        automl_settings = {
            "time_budget": time_budget,
            "metric": "accuracy",
            "task": "classification",
            "estimator_list": ["xgboost", "catboost", "lgbm", "rf"],
        }
    automl.fit(
        X_train=X_train,
        y_train=y_train,
        mlflow_logging=False,
        **automl_settings,
    )
    path = await save_model_pipeline(automl)
    return path


def calculate_prediction_input_fields(data, target) -> dict:
    prediction_input_fields_info = {}
    for column in data.columns:
        if column == target:
            continue
        most_frequent_value = data[column].mode()[0]
        data_type = str(data[column].dtype)

        if data_type not in ["int64", "float64"]:
            non_nan_values = data[column].dropna().astype(str).unique()
            unique_values = sorted(non_nan_values.tolist(), key=locale.strxfrm)
        else:
            unique_values = None

        prediction_input_fields_info[column] = {
            "most_frequent_value": str(most_frequent_value),
            "data_type": data_type,
            "fields": unique_values,
        }

    sorted_fields = sorted(
        prediction_input_fields_info.items(),
        key=lambda item: locale.strxfrm(item[0]),
    )
    prediction_input_fields_info = {item[0]: item[1] for item in sorted_fields}

    return prediction_input_fields_info


async def predict_model_pipeline(new_data, path: str) -> list:
    """Predicts from from trained model using input datasets."""

    try:
        automl = pickle.load(open(f"static/{path}", "rb"))
        y_pred = automl.predict(new_data)
        return y_pred.tolist()
    except FileNotFoundError:
        raise NotFoundError(message="Model doesn't exist.")
    except Exception as e:
        print(f"An error occurred: {e}")
