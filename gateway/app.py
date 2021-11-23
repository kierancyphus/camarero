from flask import Flask, request
import logging
from utils import *

logging.getLogger().setLevel(logging.INFO)
app = Flask(__name__)


@app.route('/ping')
def ping() -> str:
    return "pong"


@app.route('/get-anatomical-region', methods=["POST"])
def get_anatomical_region() -> str:
    """

    :return: will be one of the regions specified in x file, or an error
    """
    # data should be a dictionary
    data = dict(request.form)
    app.logger.info(f"data: {data}")

    # take data and send it to get preprocessed
    data = preprocess_data()

    # send it to model
    result = perform_inference()

    return stringify_model_output(result)
