#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：LiShun
@File    ：book_schemas.py
@Time    ：2022/3/7 3:35 下午
@Desc    ：
"""
from apps.models import BooksModel

from apps.schemas.base_schemas import GenericSerializerSchemas


class BookSchema(GenericSerializerSchemas):
    class Meta:
        model = BooksModel
        exclude = ("create_time", "update_time", "creator", "mender")


class ListBookSchema(GenericSerializerSchemas):
    class Meta:
        many = True
        model = BooksModel
        exclude = ("create_time", "update_time", "creator", "mender", "hero")


class CreateOrUpdateBookSchema(GenericSerializerSchemas):
    class Meta:
        model = BooksModel
        exclude = ("id", "create_time", "update_time", "creator", "mender", "hero")
