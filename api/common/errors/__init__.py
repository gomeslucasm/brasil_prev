class BaseError(Exception):
    def __init__(self, msg, code):
        super().__init__(msg)
        self.code = code


class NotFoundError(BaseError):
    def __init__(self, msg):
        self.code = 404
        super().__init__(msg, self.code)


class ValidationError(BaseError):
    def __init__(self, msg):
        self.code = 422
        super().__init__(msg, self.code)
