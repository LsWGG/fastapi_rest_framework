#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：LiShun
@File    ：base_schemas.py
@Time    ：2022/4/21 00:07
@Desc    ：
"""
from core.setting import settings
from fastapi_rest_framework.schemas import ModelSerializerSchemas


class GenericSerializerSchemas(ModelSerializerSchemas):
    __doc__ = "用于初始化Model，维护关联关系"

    @classmethod
    def get_models_paths(cls):
        orm_conf = settings.get_orm_base_conf()
        return orm_conf.get("apps", dict()).get("models", dict()).get("models", list())
