from typing import Dict, Optional
import numpy as np
import json
import requests
from flask_restful import Resource, Api
from flask import request, logging


class PreprocessingService(Resource):
    def get(self):
        return self.preprocess_data(dict(request.form))

    def preprocess_data(self, request: Dict[str, str]) -> Optional[Dict[str, str]]:
        try:
            np_array = np.array(json.loads(request["data"]))
        except KeyError:
            app.logger.info("Error: request did not contain data")
            return None
        except Exception as err:
            app.logger.info("Error: could not process the request")
            app.logger.debug(err)
            return None

        # TODO perform some sort of preprocessing

        # convert array to be able to send
        np_array = json.dumps(np_array.tolist())
        return {"data": np_array}

    def perform_inference(self, data: Dict[str, str]) -> str:
        """

        :param data: The preprocessed data to be sent out
        :return: model output
        """
        url = ""  # TODO: put in the final url

        try:
            requests.post(url, data=data)
        except Exception as e:
            self.logger.info("Error: was unable to get model output")
            self.logger.debug(e)

        return ""

    def stringify_model_output(self, result) -> str:
        """

        :param result:
        :return:
        """

        pass
