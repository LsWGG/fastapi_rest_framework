#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：LiShun
@File    ：dynamic_methods.py
@Time    ：2022/3/10 10:03 上午
@Desc    ：为Mixin提供具体的逻辑操作
"""
from pydantic import BaseModel

from fastapi import Depends, Path, Query, Request, Body

from fastapi_rest_framework.utils.response import response


class MakeMixin:
    @classmethod
    def make_list(cls, _page, page_key, _size, size_key, **kwargs):
        async def list(
                self,
                request: Request,
                page: int = Query(_page, alias=page_key),
                limit: int = Query(_size, alias=size_key),
        ):
            skip = (page - 1) * limit
            return await self.get_queryset().offset(skip).limit(limit).order_by("id").all()

        return list

    @classmethod
    def make_retrieve(cls, lookup_field, lookup_type, **kwargs):
        async def retrieve(
                self,
                request: Request,
                param: lookup_type = Path(..., alias=lookup_field)
        ):
            self.pk_param = param
            return await self.get_object()

        return retrieve

    @classmethod
    def make_create(cls, check_body: BaseModel):
        async def create(
                self,
                request: Request,
                validated_data: check_body = Body(...)
        ):
            return await self.model.create(**validated_data.dict())

        return create

    @classmethod
    def make_update(cls, lookup_field, lookup_type, check_body, **kwargs):
        async def update(
                self,
                request: Request,
                validated_data: check_body = Body(...),
                param: lookup_type = Path(..., alias=lookup_field),
        ):
            self.pk_param = param
            await self.get_object().update(**validated_data.dict())
            return await self.get_object()

        return update

    @classmethod
    def make_destroy(cls, lookup_field, lookup_type, **kwargs):
        async def destroy(
                self,
                request: Request,
                param: lookup_type = Path(..., alias=lookup_field),
        ):
            self.pk_param = param
            print(self.get_object())
            await self.get_object().delete()
            return response("删除成功")

        return destroy
