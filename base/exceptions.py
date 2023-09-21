from rest_framework.exceptions import APIException
from rest_framework.status import HTTP_400_BAD_REQUEST


class SeazoneAPIException(APIException):
    def __init__(self, detail, codigo, status_code=HTTP_400_BAD_REQUEST):
        self.detail = detail
        self.codigo = codigo
        self.status_code = status_code
        super().__init__(detail=detail)

    def __str__(self):
        return f"{self.codigo}: {self.detail}"
