class BaseError(Exception):
    def __init__(self, msg, code):
        super().__init__(msg)
        self.code = code
        self.msg = msg


class NotFoundError(BaseError):
    def __init__(self, msg):
        self.code = 404
        self.msg = msg
        super().__init__(self.msg, self.code)


class ValidationError(BaseError):
    def __init__(self, msg):
        self.code = 422
        self.msg = msg
        super().__init__(self.msg, self.code)
