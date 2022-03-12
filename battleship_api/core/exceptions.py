from fastapi import HTTPException, status
from pydantic import BaseModel as BaseSchema
import http


class BaseAPIException(HTTPException):
    """
    Base custom API exception

    Class fields:
        - code: HTTP response status code
        - message: Exception description and message
        - schema: Response schema
    """
    code: int = status.HTTP_400_BAD_REQUEST
    message: str | None = None
    schema: BaseSchema | None = None

    def __init__(self, exception_data: dict['str'] | None = None, **kwargs):
        """
        Initialize API exception instance with given data passed to response
        body schema constructor and pass `kwargs` to inherited HTTPException
        initializer.

        Args:
            - [Optional] exception_data: Dictionary of parameters passed to
                response schema constructor.
        """
        super().__init__(self.code, self.message, **kwargs)
        self.data = {'description': self.message}
        if self.schema is not None:
            if exception_data is None:
                exception_data = dict()
            self.data.update({'data': self.schema(**exception_data).dict()})

    def response(self):
        from fastapi.responses import JSONResponse
        return JSONResponse(
            content=self.data,
            status_code=self.code
        )

    @classmethod
    def get_response_schema(cls):
        """
        Generates schema of exception response body as dictionary.

        Returns:
            _type_: _description_
        """
        schema = {
            'description': cls.message or http.HTTPStatus(cls.code).phrase}
        if cls.schema is not None:
            schema.update({'model': cls.schema})
        return schema


def build_exceptions_dict(*exceptions: type[BaseAPIException]):
    """_summary_

    Returns:
        _type_: _description_
    """
    print({
        exception.code: exception.get_response_schema()
        for exception in exceptions})
    return {
        exception.code: exception.get_response_schema()
        for exception in exceptions}


def api_exceptions_handler(_, exception):
    if isinstance(exception, BaseAPIException):
        return exception.response()
