class AppError(Exception):
    status_code = 500
    message = "Internal server error"

    def __init__(self, message=None):
        if message:
            self.message = message

    def to_dict(self):
        return {"error": self.message}


class BadRequestError(AppError):
    status_code = 400


class NotFoundError(AppError):
    status_code = 404
