from flask import Flask, request
from flask_restful import Api, Resource
from typing import Optional, Dict
import numpy as np
import json
import logging


class PreprocessingService(Resource):
    def post(self):
        return self.preprocess_data(dict(request.form))

    def preprocess_data(self, request: Dict[str, str]) -> Dict[str, str]:
        try:
            np_array = np.array(json.loads(request["data"]))
        except KeyError:
            app.logger.info("Error: request did not contain data")
            return dict()
        except Exception as err:
            app.logger.info("Error: could not process the request")
            app.logger.debug(err)
            return dict()

        # TODO perform some sort of preprocessing
        # np_array = some_transformation(np_array)

        # convert array to be able to send
        np_array = json.dumps(np_array.tolist())
        return {"data": np_array}


class Ping(Resource):
    def get(self) -> str:
        return "pong"


if __name__ == "__main__":
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(PreprocessingService, '/preprocess-data')
    api.add_resource(Ping, '/ping')

    logging.getLogger().setLevel(logging.INFO)
    app.run(host='0.0.0.0')
    app.logger.info("Starting up!")
