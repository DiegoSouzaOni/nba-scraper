class BaseEndpoint:
    def __init__(self, endpoint: str, params: dict = None):
        self.endpoint = endpoint
        self.params = params or {}
