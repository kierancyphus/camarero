from flask import Flask, request
from flask_restful import Api, Resource
import logging
import requests
from utils import preprocess_data, perform_inference, stringify_model_output
import os
import pickle


class Ping(Resource):
    def get(self) -> str:
        return [{'label': 'smelly', 'index': 'engineers'}, {'something': 'else'}]


class HealthCheck(Resource):
    def get(self):
        path = "http://data-preprocessing:5000/ping"
        app.logger.info(f"calling: {path}")
        try:
            response = requests.get(path)
            return response.text
        except ConnectionRefusedError:
            return "Couldn't do it", 500
        except Exception:
            return "Something really went wrong", 500


class EvaluateModel(Resource):
    def post(self):
        """

        :return: will be one of the regions specified in x file, or an error
        """
        # request_data should be a dictionary
        request_data = dict(request.form)
        if "data" not in request_data:
            return "Error: please ensure you have attached data", 400
        if "model_name" not in request_data:
            return "Error: please include a model_name", 400
        if request_data["model_name"] not in model_names:
            return "Error: please ensure you are including a valid model name.", 404

        app.logger.info(f"data: {request_data}")

        # take data and send it to get preprocessed
        request_data = preprocess_data(request_data)
        app.logger.info(f"preprocessed data: {request_data}")

        if not request_data:
            return "Could not preprocess the data", 500

        # send it to model
        result = perform_inference(request_data)

        return stringify_model_output(result)


if __name__ == "__main__":
    app = Flask(__name__)
    # Note: usually a global variable here is normally terrible because it is not thread safe. That being said,
    # these are going to be single threaded anyway and I will require the server to restart if we want to add
    # a new model.
    model_names = set(os.listdir('/usr/src/models'))

    # create api
    api = Api(app)
    api.add_resource(Ping, '/ping')
    api.add_resource(HealthCheck, '/health-check')
    api.add_resource(EvaluateModel, '/evaluate-model')

    # start app and make sure it accepts requests from all ports
    logging.getLogger().setLevel(logging.INFO)
    app.run(host='0.0.0.0')
    app.logger.info("Starting up!")
