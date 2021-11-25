from typing import Dict
import requests


def preprocess_data(data: Dict[str, str]) -> Dict[str, str]:
    url = "http://data-preprocessing:5000/preprocess-data"
    response = requests.post(url, data)
    try:
        return dict(response.text)
    except ValueError:
        return dict()


def perform_inference(request: Dict[str, str]) -> Dict[str, str]:
    """
    :param request: {data: ..., model_name: ...}, model_name points to the model to be used
    :return: {"predictions": ...} containts the prediction for the given input

    """
    try:
        # Note: we are only performing inference on one item for now
        payload = {
            "instances": [{"input_image": request["data"]}]
        }
        url = f"http://inference:8501/v1/models/{request['model_name']}:predict"
        response = requests.post(url, json=payload)
        return dict(response.text)
    except Exception:
        return {}


def stringify_model_output(output: Dict[str, str]) -> Dict[str, str]:
    """
    Converts model output (number) to a human readable output
    :param output:
    :return:
    """
    # TODO: implement this once I know the actual anatomical regions

    return {}