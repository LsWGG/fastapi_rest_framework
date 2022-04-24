#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：LiShun
@File    ：generics.py
@Time    ：2022/3/8 3:32 下午
@Desc    ：常用视图，待补充
"""
from tortoise.models import Model
from tortoise.queryset import QuerySet

from fastapi_rest_framework.viewsets.helper import get_object_or_404, get_model_foreignkey_field


class GenericAPIMixin:
    # 分页
    page = 1
    page_key = "page"
    size = 10
    size_key = "size"

    # 路径参数
    lookup_field = "id"
    lookup_type = int
    pk_param = None

    # 模型类
    model = None
    # 默认的Schema
    schema_class = None

    retrieve_function = get_object_or_404

    @classmethod
    def get_object(cls, is_query=False):
        assert cls.pk_param is not None, (
            f"{cls.__name__} should either include a `pk_param` attribute. "
        )

        filter_kwargs = {cls.lookup_field: cls.pk_param}
        obj = get_object_or_404(cls.get_queryset(), is_query, **filter_kwargs)
        return obj

    @classmethod
    def get_queryset(cls):
        assert cls.model is not None, (
            f"{cls.__name__} should either include a `model` attribute. "
        )
        # tortoise-orm为了性能，默认不查询关联表字段，需使用prefetch_related方法指定。
        # https://tortoise-orm.readthedocs.io/en/latest/query.html?highlight=prefetch_related#tortoise.queryset.QuerySet.prefetch_related
        # todo: 这里暂时查询时每次指定。
        related_field = get_model_foreignkey_field(cls.model)
        # Ensure queryset is re-evaluated on each request.
        queryset = cls.model.all().prefetch_related(*related_field)
        return queryset

    @classmethod
    def get_schema(cls, action):
        schema = cls.get_schema_class(action)
        return schema()

    @classmethod
    def get_schema_class(cls, action):
        assert cls.schema_class is not None, (
            f"{cls.__name__} should either include a `schema_class` attribute. "
        )

        if hasattr(cls, action + "_schema_class"):
            return getattr(cls, action + "_schema_class")
        else:
            return cls.schema_class
