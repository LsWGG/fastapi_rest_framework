#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：LiShun
@File    ：toroise_orm_demo.py
@Time    ：2022/3/9 4:07 下午
@Desc    ：
"""
from tortoise import Tortoise, run_async, fields

from core.setting import settings
from apps.models.books_model import BooksModel, HeroModel


# class BookSchema(BaseModel):
#     id: int
#     b_title: str = Field(max_length=32)
#     b_author: str = Field("", max_length=32)
#     b_description: str
#     b_pub_time: str
#     creator: str
#     mender: str
#     create_time: str
#     update_time: str
#
#     class Config:
#         orm_mode = True

async def main():
    await Tortoise.init(settings.get_orm_base_conf())

    data = await BooksModel.filter(id=3).update()
    print(data)


run_async(main())
