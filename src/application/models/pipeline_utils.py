import locale
import os
import pickle
import uuid
import warnings

import numpy as np
import pandas as pd
from flaml import AutoML
from sklearn.model_selection import train_test_split

from src.celery.app import celery_app
from src.domain.models import AutoMLDeps, StatusType
from src.infrastructure.application import (
    BadRequestError,
    NotFoundError,
    UnprocessableError,
)

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.simplefilter(action="ignore", category=FutureWarning)
warnings.simplefilter(action="ignore", category=UserWarning)

__all__ = (
    "auto_ml__",
    "predict_model_pipeline",
    "calculate_prediction_input_fields",
    "load_dataset",
    "generate_unique_path",
    "save_model_to_path",
)


def load_dataset(data_url) -> pd.DataFrame:
    for encoding in ["utf-8", "latin1", "iso-8859-1"]:
        try:
            dataset = pd.read_csv(
                f"static/datasets/{data_url}", encoding=encoding
            )
            return dataset
        except UnicodeDecodeError:
            continue
    raise UnprocessableError(
        message="Unable to decode the CSV file using supported encodings."
    )


def generate_unique_path() -> str:
    """Generates a unique path for saving the model."""

    directory = "static/pipelines"
    if not os.path.exists(directory):
        os.makedirs(directory)
    path = f"{directory}/{str(uuid.uuid4())}.pkl"
    return path


def save_model_to_path(automl, path: str):
    """Saves the dataset trained file in the storage."""

    with open(path, "wb") as f:
        pickle.dump(automl, f, pickle.HIGHEST_PROTOCOL)


@celery_app.task(name="auto_ml__")
def auto_ml__(deps_dict: dict):
    """Trains model based on the dataset."""

    try:
        deps = AutoMLDeps(**deps_dict)
        train_data = load_dataset(deps.dataset_url)
        try:
            X = train_data.drop([deps.target], axis=1)
        except KeyError:
            raise NotFoundError(message=f"{deps.target} not found in axis")
        y = train_data[deps.target]
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=deps.threshold, random_state=42
        )
        automl = AutoML()
        match deps.pipeline_type:
            case "regression":
                automl_settings = {
                    "time_budget": deps.time_budget,
                    "metric": "r2",
                    "task": "regression",
                }
            case "classification":
                automl_settings = {
                    "time_budget": deps.time_budget,
                    "metric": "accuracy",
                    "task": "classification",
                    "estimator_list": ["xgboost", "catboost", "lgbm", "rf"],
                }
            # case "nlp":
            #     MAX_ITER = 20
            #     automl_settings = {
            #         "max_iter": MAX_ITER,
            #         "task": "seq-classification",
            #         "fit_kwargs_by_estimator": {
            #             "transformer": {
            #                 "output_dir": "static/pipelines/data/output/",
            #                 "model_path": "google/electra-small-discriminator",
            #             }
            #         },
            #         "gpu_per_trial": 1,
            #         "log_file_name": "seqclass.log",
            #         "log_type": "all",
            #         "use_ray": False,  # If parallel tuning, set "use_ray" to {"local_dir": "data/output/"}
            #         "n_concurrent_trials": 1,
            #         "keep_search_state": True,
            #         #  "fp16": False
            #     }
            #     X_train, X_validation, y_train, y_validation = train_test_split(
            #         X_train, y_train, test_size=deps.threshold, random_state=42
            #     )
            #     automl.fit(
            #         X_val=X_validation,
            #         y_val=y_validation,
            #     )
            case _:
                raise BadRequestError(
                    message="Pipeline type is under construction..."
                )
        automl.fit(
            X_train=X_train,
            y_train=y_train,
            **automl_settings,
        )
        save_model_to_path(automl, deps.pipeline_route)
        # Change ModelsTable's status to StatusType.success
    except Exception as e:
        # Change ModelsTable's status to StatusType.failed
        raise UnprocessableError(message=str(e))


def calculate_prediction_input_fields(dataset_url, target) -> dict:
    """Generate prediction inputs from a dataset for web."""

    data = load_dataset(dataset_url)
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
