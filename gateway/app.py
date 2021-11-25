from flask import Flask, request
import logging
import requests
from utils import preprocess_data
import os

app = Flask(__name__)

# Note: usually a global variable here is normally terrible because it is not thread safe. That being said,
# these are going to be single threaded anyway and I will require the server to restart if we want to add
# a new model.
model_names = set(os.listdir('/usr/scr/models'))


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
    # request_data should be a dictionary
    request_data = dict(request.form)
    if "data" not in request_data:
        return "Error: please ensure you have attached data"
    if "model_name" not in request_data:
        return "Error: please include a model_name"
    if request_data["model_name"] not in model_names:
        return "Error: please ensure you are including a valid model name."

    app.logger.info(f"data: {request_data}")

    # take data and send it to get preprocessed
    request_data = preprocess_data(request_data)
    app.logger.info(f"preprocessed data: {request_data}")
    try:
        return request_data["data"]
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
