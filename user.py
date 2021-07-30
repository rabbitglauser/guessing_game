from flask import request


class InvalidAPIUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


def checkUserLoggedIn():
    user_id = request.headers.get("user_name")
    if not user_id:
        raise InvalidAPIUsage("No user id provided!")
    else:
        return user_id
