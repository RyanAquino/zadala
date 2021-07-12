from rest_framework.exceptions import APIException


class UnprocessableEntity(APIException):
    status_code = 422
    default_detail = "The request was well-formed but was unable to be followed due to semantic errors."
