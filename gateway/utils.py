from typing import Dict
import requests


def preprocess_data(data: Dict[str, str]) -> Dict[str, str]:
    url = "http://data-preprocessing:5000/preprocess-data"
    response = requests.post(url, data)
    try:
        return dict(response.text)
    except ValueError:
        return dict()
