import requests


class DevicesDAO:
    def __init__(self, url: str = 'http://127.0.0.1:8000/data/device/'):
        self._url = url

    def get(self):
        # Making a get request
        response = requests.get(self._url)

        # Convert json into dictionary
        response_dict = response.json()

        return response_dict


class NodeDAO:

    _config_uri = 'config'

    def __init__(self, url: str = 'http://127.0.0.1:8001/'):
        self._url = url
        self.headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    def get(self):
        # Making a get request
        response = requests.get(f'{self._url}{self._config_uri}')

        # Convert json into dictionary
        return response.json()

    def post(self, payload: dict):
        return requests.post(
            f'{self._url}{self._config_uri}',
            json=payload
        )
