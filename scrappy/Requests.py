import requests

class Requester:
    def __init__(self) -> None:
        pass

    def get_request(self, url, timeout=6):
        return requests.get(url, timeout=timeout)
    