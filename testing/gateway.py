import requests
import os
import pickle

if __name__ == "__main__":
    os.environ['NO_PROXY'] = '127.0.0.1'
    response = requests.get("http://localhost:5000/ping")
    print(response.text)
    print(response.content)
    print(response.json()[0])
    responses = pickle.loads(response.content)
    print(responses)

    # url = "http://127.0.0.1:5000/evaluate-model"
    # data = {'model_name': 'test', 'data': 'here'}
    #
    # response = requests.post(url, data)
    # print(response.text)