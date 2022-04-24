#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：LiShun
@File    ：books_model.py
@Time    ：2022/3/7 2:03 下午
@Desc    ：
"""
from tortoise import fields

from apps.models.base_model import AutoModel


class BooksModel(AutoModel):
    b_title = fields.CharField(max_length=32, description="书名")
    b_author = fields.CharField(max_length=32, description="作者")
    b_description = fields.TextField(description="描述信息")
    b_pub_time = fields.DatetimeField(auto_now=True, description="发布日期")
    hero = fields.ReverseRelation["HeroModel"]

    class Meta:
        table = "tb_books"
        ordering = ["id"]
        table_description = "书籍表"

    def __str__(self):
        return self.b_title


class HeroModel(AutoModel):
    h_name = fields.CharField(max_length=32, description="人物")
    h_gender = fields.CharField(max_length=8, description="性别")
    h_comment = fields.TextField(description="描述信息")
    h_book = fields.ForeignKeyField("models.BooksModel", related_name="hero")

    class Meta:
        table = "tb_hero"
        table_description = "人物信息表"

    def __str__(self):
        return self.h_name
