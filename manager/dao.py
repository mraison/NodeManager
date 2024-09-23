import requests


class NodeDAO:
    def __init__(self, url: str = 'http://127.0.0.1:8001/config'):
        self._url = url
        self.headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    def get(self):
        # Making a get request
        response = requests.get(self._url)

        # Convert json into dictionary
        return response.json()

    def post(self, payload: dict):
        return requests.post(
            self._url,
            json=payload
        )
