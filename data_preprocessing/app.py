from flask import Flask, request
import logging
import os

app = Flask(__name__)


@app.route('/ping')
def ping() -> str:
    return "pong"


if __name__ == "__main__":
    # os.environ['NO_PROXY'] = '127.0.0.1'
    logging.getLogger().setLevel(logging.INFO)
    app.run(host='0.0.0.0')
    app.logger.info("Starting up!")
