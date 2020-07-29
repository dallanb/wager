from flask import g, request
from .response import ErrorResponse


class Auth:
    def __init__(self):
        self.logger = g.logger.getLogger(__name__)

    @classmethod
    def check_user(cls):
        g.user = request.headers.get('X-Consumer-Custom-ID')
        if not g.user:
            return ErrorResponse(code=400, msg='Missing user data'), 400
