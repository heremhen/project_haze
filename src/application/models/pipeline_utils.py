import asyncio
import locale
import os
import pickle
import uuid
import warnings

import pandas as pd
from bs4 import BeautifulSoup
from flaml import AutoML
from loguru import logger
from sklearn.model_selection import train_test_split
from ydata_profiling import ProfileReport

from src.celery.app import celery_app
from src.config import settings
from src.domain.models import (
    AutoMLDeps,
    ModelsFlat,
    ModelsRepository,
    StatusType,
)
from src.domain.models.aggregates import Model_
from src.infrastructure.application import (
    BadRequestError,
    DatabaseError,
    NotFoundError,
    UnprocessableError,
)
from src.infrastructure.database import transaction

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

codecs = ["utf-8", "latin1", "iso-8859-1"]


def load_dataset(data_url) -> pd.DataFrame:
    for encoding in codecs:
        try:
            dataset = pd.read_csv(
                f"{settings.root_dir}/static/datasets/{data_url}",
                encoding=encoding,
            )
            return dataset
        except UnicodeDecodeError:
            continue
    raise UnprocessableError(
        message="Unable to decode the CSV file using supported encodings."
    )


def replace_a_tag_with_text(html_file, new_text):
    with open(html_file, "r") as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, "html.parser")
    a_tags = soup.find_all("a")

    for a_tag in a_tags:
        if "href" in a_tag.attrs:
            if (
                a_tag["href"] == "https://github.com/ydataai/ydata-profiling"
                or a_tag["href"].startswith(
                    "data:text/plain;charset=utf-8,%7B"
                )
                or a_tag["href"].startswith("https://ydata.ai/")
            ):
                a_tag.string.replace_with(new_text)
                a_tag["href"] = "#"
                del a_tag["target"]

    with open(html_file, "w") as file:
        file.write(str(soup))


async def generate_report(
    title: str,
    df: pd.DataFrame,
    registry_id: int,
    model_id: int,
):
    report_ = ProfileReport(
        df,
        title=f"{title} Report",
        minimal=True,
        explorative=True,
        # config_file=f"{settings.root_dir}/static/config_min.yaml",
    )
    folder_id = str(uuid.uuid4())
    directory = f"{settings.root_dir}/static/report/{folder_id}"
    if not os.path.exists(directory):
        os.makedirs(directory)
    # report_.to_file(f"{directory}/report.json")
    report_.config.html.minify_html = False
    report_.to_file(f"{directory}/report.html")
    replace_a_tag_with_text(
        f"{directory}/report.html",
        "Hazel Haze",
    )
    schema = {
        "models_id": model_id,
        "registry_id": registry_id,
        "report_route": f"static/report/{folder_id}/report.html",
    }
    return schema


def generate_unique_path() -> str:
    """Generates a unique path for saving the model."""

    directory = f"{settings.root_dir}/static/pipelines"
    if not os.path.exists(directory):
        os.makedirs(directory)
    path = f"{directory}/{str(uuid.uuid4())}.pkl"
    return path


def save_model_to_path(automl, path: str):
    """Saves the dataset trained file in the storage."""

    with open(path, "wb") as f:
        pickle.dump(automl, f, pickle.HIGHEST_PROTOCOL)


async def update_model_status(model_id, status):
    """Update the status of the model in the database."""

    async with transaction():
        try:
            model_flat: ModelsFlat = await ModelsRepository().update(
                key="id", value=model_id, payload={"status": status}
            )
            rich_model: Model_ = await ModelsRepository().get(model_flat.id)
        except DatabaseError as e:
            raise UnprocessableError(
                message=f"Could not update model status: {e}"
            )


def get_automl_settings(deps: AutoMLDeps, data_type: str) -> dict:
    task = "classification"
    if data_type in ["int64", "float64"]:
        task = "regression"
    # metric_constraints = [("train_loss", "<=", 0.1), ("val_loss", "<=", 0.1)]
    automl_settings = {
        "task": task,
        "metric": "auto",
        # "max_iter": 100,
        # "train_time_limit": 9,
        # "metric_constraints": metric_constraints,
        # "pred_time_limit": 1e-3,
    }
    return automl_settings


def get_automl_settings_with_pipeline(
    automl_settings: dict, pipeline_type: str
) -> dict:
    logger.info(pipeline_type)
    match pipeline_type:
        case "classification":
            automl_settings["estimator_list"] = [
                "xgboost",
                "catboost",
                "lgbm",
                "rf",
            ]
        case "regression":
            pass
        case "auto":
            pass
        case _:
            raise BadRequestError(
                message="Pipeline type is under construction..."
            )
    return automl_settings


def convert_column_to_numeric(column: pd.Series) -> pd.Series:
    try:
        return pd.to_numeric(column)
    except ValueError:
        pass

    try:
        column = column.str.replace(",", ".")
        return pd.to_numeric(column)
    except ValueError:
        pass

    return column


@celery_app.task(name="auto_ml__")
def auto_ml__(deps_dict: dict, model_id: int):
    """Trains model based on the dataset."""

    def on_success(model_id):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            update_model_status(model_id, StatusType.success)
        )

    def on_failure(exc, model_id):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            update_model_status(model_id, StatusType.failed)
        )

    try:
        deps = AutoMLDeps(**deps_dict)
        train_data = load_dataset(deps.dataset_url)
        train_data.columns = train_data.columns.str.strip()
        try:
            X = train_data.drop([deps.target], axis=1)
            train_data[deps.target] = convert_column_to_numeric(
                train_data[deps.target]
            )
            data_type = str(train_data[deps.target].dtype)
            logger.critical(f"The data type of {deps.target} is {data_type}")
        except KeyError:
            raise NotFoundError(message=f"{deps.target} not found in axis")
        y = train_data[deps.target]
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=deps.threshold, random_state=42
        )
        automl_settings = get_automl_settings(deps, data_type)
        automl_settings = get_automl_settings_with_pipeline(
            automl_settings, deps.pipeline_type
        )
        automl = AutoML()
        automl.fit(
            X_train=X_train,
            y_train=y_train,
            time_budget=deps.time_budget,
            **automl_settings,
        )
        save_model_to_path(automl, deps.pipeline_route)
        on_success(model_id)
    except Exception as e:
        on_failure(e, model_id)


def calculate_prediction_input_fields(dataset_url, target) -> dict:
    """Generate prediction inputs from a dataset for web."""

    data = load_dataset(dataset_url)
    data.columns = data.columns.str.strip()
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


async def predict_model_pipeline(new_data: pd.DataFrame, path: str) -> list:
    """Predicts from from trained model using input datasets."""

    try:
        automl = pickle.load(open(f"{path}", "rb"))
        y_pred = automl.predict(new_data)
        return y_pred.tolist()
    except FileNotFoundError:
        raise NotFoundError(message="Model doesn't exist.")
    except Exception as e:
        raise UnprocessableError(message=str(e))
