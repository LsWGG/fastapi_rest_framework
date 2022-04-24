#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：LiShun
@File    ：books_manage.py
@Time    ：2022/3/7 10:07 上午
@Desc    ：
"""
from apps.schemas import book_schemas
from apps.models.books_model import BooksModel

from fastapi_rest_framework.viewsets import ModelViewSet


class BookViewSet(ModelViewSet):
    model = BooksModel
    schema_class = book_schemas.BookSchema

    list_schema_class = book_schemas.ListBookSchema
    create_schema_class = book_schemas.CreateOrUpdateBookSchema
    update_schema_class = book_schemas.CreateOrUpdateBookSchema
