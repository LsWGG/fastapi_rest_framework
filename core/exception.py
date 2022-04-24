__all__ = [
    'register_exception',
]

import traceback
from typing import Any

from fastapi import FastAPI
from fastapi import Request, status
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse
from tortoise.validators import ValidationError

from apps.utils.define import StatusCode
from apps.utils.exceptions import BaseHTTPException


def log_message(request: Request, message: Any):
    """
    日志输出
    :param request:
    :param message:
    :return:
    """

    print('start error'.center(60, '*'))
    print(f'{request.method} {request.url}')
    print(f'error is {message}')
    print('end error'.center(60, '*'))


def register_exception(app: FastAPI):
    """
    捕获FastApi异常
    :param app:
    :return:
    """

    @app.exception_handler(BaseHTTPException)
    async def catch_c_http_exception(request: Request, exc: BaseHTTPException):
        """
        捕获自定义异常
        :param request:
        :param exc:
        :return:
        """

        log_message(request, exc.message)
        content = {'status_code': exc.code, 'message': exc.message, 'data': None}
        return JSONResponse(content=content, status_code=exc.status_code, headers=exc.headers)

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """
        FastAPI HTTPException 异常
        :param request:
        :param exc:
        :return:
        """

        log_message(request, exc.detail)
        content = {'status_code': StatusCode.bad_request, 'message': exc.detail, 'data': None}
        return JSONResponse(content=content, status_code=exc.status_code, headers=exc.headers)

    @app.exception_handler(AssertionError)
    async def assert_exception_handle(request: Request, exc: AssertionError):
        """
        Python AssertError 异常
        :param request:
        :param exc:
        :return:
        """

        exc_str = ''.join(exc.args)
        log_message(request, exc_str)
        content = {'status_code': StatusCode.validator_error, 'message': exc_str, 'data': None}
        return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

    @app.exception_handler(ValidationError)
    async def db_validation_exception_handle(request: Request, exc: ValidationError):
        """
        tortoise-orm ValidatorError 异常
        :param request:
        :param exc:
        :return:
        """

        exc_str = '|'.join(exc.args)
        log_message(request, exc_str)
        content = {'status_code': StatusCode.validator_error, 'message': exc_str, 'data': None}
        return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """
        FastAPI RequestValidationError 异常
        :param request:
        :param exc:
        :return:
        """

        exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
        log_message(request, exc_str)
        # content = exc.errors()
        content = {'status_code': StatusCode.validator_error, 'message': exc_str, 'data': None}
        return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

    @app.exception_handler(Exception)
    async def exception_handle(request: Request, exc: Exception):
        """
        其他异常
        :param request:
        :param exc:
        :return:
        """

        log_message(request, traceback.format_exc())
        content = {'status_code': StatusCode.server_error, 'message': str(exc), 'data': None}
        return JSONResponse(content=content, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
