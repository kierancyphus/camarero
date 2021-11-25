import requests
import os


if __name__ == "__main__":
    os.environ['NO_PROXY'] = '127.0.0.1'
    response = requests.get("http://localhost:5000/ping")
    print(response.text)

    url = "http://127.0.0.1:5000/get-anatomical-region"
    data = {'model_name': 'test', 'data': 'here'}

    response = requests.post(url, data)
    print(response.text)