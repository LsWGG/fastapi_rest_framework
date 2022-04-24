#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：LiShun
@File    ：__init__.py.py
@Time    ：2022/3/7 10:06 上午
@Desc    ：
"""
from fastapi_rest_framework.router import MainRouter

books_router = MainRouter(prefix="/book", tags=["图书管理"])
