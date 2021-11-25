from flask import Flask, request
from flask_restful import Api, Resource
from typing import Optional, Dict, Tuple
import numpy as np
import json
import logging


class PreprocessingService(Resource):
    def post(self):
        return self.preprocess_data(dict(request.form))

    def preprocess_data(self, request: Dict[str, str]) -> Tuple[Dict[str, str], int]:
        """
        :param request: {data: ..., model_name: ...}, model_name specifies the kind of transformation
                        that should be performed
        :return: {data: tf_tensor, model_name: ...}
        """
        try:
            np_array = np.array(json.loads(request["data"]))
        except Exception as err:
            app.logger.info("Error: could not process the request")
            app.logger.debug(err)
            return dict(), 500

        # TODO perform some sort of preprocessing (should come from utils and be mapped to modelname)
        # np_array = some_transformation(np_array)

        # convert array to be able to send
        np_array = json.dumps(np_array.tolist())
        return {"data": np_array}, 200


class Ping(Resource):
    def get(self) -> Tuple[str, int]:
        return "pong", 200


if __name__ == "__main__":
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(PreprocessingService, '/preprocess-data')
    api.add_resource(Ping, '/ping')

    logging.getLogger().setLevel(logging.INFO)
    app.run(host='0.0.0.0')
    app.logger.info("Starting up!")
