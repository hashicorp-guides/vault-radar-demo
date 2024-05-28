import requests
import base64


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r


class BasicAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = base64.b64encode(token.encode()).decode()

    def __call__(self, r):
        r.headers["authorization"] = "Basic " + self.token
        return r