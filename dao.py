import requests


class DeviceDAO:
    def __init__(self, url: str = 'http://127.0.0.1:8000/data/device/'):
        self._url = url

    def get(self):
        # Making a get request
        response = requests.get(self._url)

        # Convert json into dictionary
        response_dict = response.json()

        return response_dict
