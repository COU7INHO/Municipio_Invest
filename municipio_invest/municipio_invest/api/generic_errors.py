
class APIRequestError(Exception):
    def __init__(self, status_code, message="API request failed"):
        super().__init__(f"{message} (Status Code: {status_code})")
        self.status_code = status_code