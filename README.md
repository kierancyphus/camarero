# Camarero
A simple docker network for handling requests, preprocessing data and serving tf ml models

## Structure
### There are a total of three services in the docker network:
- Request Handler: Handles incoming requests and makes appropriate calls to preprocessing routines and models. This acts as a gateway into the network.
- Preprocessor: Preprocesses data so it can be passed to the server.
- Server: Hosts all ML models and performs inference.

### Tech Stack:
- Request Handler: Is currently a single threaded Flask app. This is okay if we are only processing one request at a time, but for better performance it should use something more robust like `gunicorn` which allows for multiple instances
- Preprocessor: Also a Flask App - has the same limitations as above
- Server: docker image of tf-serving. We can't use the gpu version because it doesn't provide support for windows.

## Use
### To start the inference service
Make sure docker-compose is installed and then run
`docker-compose up`.

### To add a new model
Add a new directory under `./models` with the model name you want, add another `config` entry in `./models/models.config`
and then restart the service using `docker-compose up` to ensure that all services see the new model.
