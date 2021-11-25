from flask import Flask, request
import logging
import requests
from utils import preprocess_data
import os

app = Flask(__name__)


@app.route('/ping')
def ping() -> str:
    return "pong"


@app.route('/ping-preprocessing')
def ping_preprocessing() -> str:
    path = "http://data-preprocessing:5000/ping"
    app.logger.info(f"calling: {path}")
    try:
        response = requests.get(path)
        return response.text
    except ConnectionRefusedError:
        return "Couldn't do it"
    except Exception:
        return "Something really went wrong"


@app.route('/get-anatomical-region', methods=["POST"])
def get_anatomical_region() -> str:
    """

    :return: will be one of the regions specified in x file, or an error
    """
    # data should be a dictionary
    data = dict(request.form)
    app.logger.info(f"data: {data}")

    # take data and send it to get preprocessed
    data = preprocess_data(data)
    app.logger.info(f"preprocessed data: {data}")
    try:
        return data["data"]
    except Exception:
        return "Internal Error"
    # # send it to model
    # result = perform_inference()
    #
    # return stringify_model_output(result)


if __name__ == "__main__":
    # os.environ['NO_PROXY'] = '127.0.0.1'
    logging.getLogger().setLevel(logging.INFO)
    app.run(host='0.0.0.0')
    app.logger.info("Starting up!")
