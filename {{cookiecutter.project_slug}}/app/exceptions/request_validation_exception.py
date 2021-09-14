from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


def request_validation_exception_handler(_: Request, exception: RequestValidationError):
    print(str(exception))
    return JSONResponse(status_code=422, content={'detail': exception.errors()})

