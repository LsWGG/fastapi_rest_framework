#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：LiShun
@File    ：response.py
@Time    ：2022/3/24 9:58 上午
@Desc    ：统一返回格式
"""
from fastapi import status
from fastapi.responses import JSONResponse, Response


def response(data, message="ok", code=status.HTTP_200_OK) -> Response:
    return JSONResponse(
        status_code=code,
        content={
            "code": code,
            "message": message,
            "data": data
        }
    )
