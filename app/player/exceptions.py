from rest_framework import status
from rest_framework.exceptions import APIException


APP_LOGIC_ERROR = 'Application_logic_error'


class AppLogicError(APIException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY

    def __init__(self, detail=None, code=None):
        detail = {APP_LOGIC_ERROR: detail}
        super().__init__(detail, code)
