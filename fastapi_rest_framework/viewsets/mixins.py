#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：LiShun
@File    ：mixins.py
@Time    ：2022/3/8 3:22 下午
@Desc    ：通用操作Mixin类，因FastAPI通过参数形式校验传值，故需使用MakeMixin提供方法初始化函数
"""
from fastapi_rest_framework.viewsets import generics
from fastapi_rest_framework.viewsets.dynamic_methods import MakeMixin
from fastapi_rest_framework.viewsets.helper import is_method_overloaded


class CreateModelMixin:
    """
    Create a model instance.
    """

    def __init_subclass__(cls: generics.GenericAPIMixin, **kwargs):
        super().__init_subclass__(**kwargs)
        if not is_method_overloaded(cls, 'create') and cls.model:
            cls.create = classmethod(
                MakeMixin.make_create(
                    check_body=cls.get_schema('create')
                )
            )


class ListModelMixin:
    """
    List a queryset.
    """

    def __init_subclass__(cls: generics.GenericAPIMixin, **kwargs):
        super().__init_subclass__(**kwargs)
        if not is_method_overloaded(cls, 'list') and cls.model:
            cls.list = classmethod(
                MakeMixin.make_list(
                    cls.page,
                    cls.page_key,
                    cls.size,
                    cls.size_key,
                    **kwargs
                ),
            )


class RetrieveModelMixin:
    """
    Retrieve a model instance.
    """

    def __init_subclass__(cls: generics.GenericAPIMixin, **kwargs):
        super().__init_subclass__(**kwargs)
        if not is_method_overloaded(cls, 'retrieve') and cls.model:
            cls.retrieve = classmethod(
                MakeMixin.make_retrieve(
                    cls.lookup_field,
                    cls.lookup_type,
                    **kwargs
                ),
            )


class UpdateModelMixin:
    """
    Update a model instance.
    """

    def __init_subclass__(cls: generics.GenericAPIMixin, **kwargs):
        super().__init_subclass__(**kwargs)
        if not is_method_overloaded(cls, 'update') and cls.model:
            cls.update = classmethod(
                MakeMixin.make_update(
                    cls.lookup_field,
                    cls.lookup_type,
                    check_body=cls.get_schema('update')
                )
            )


class DestroyModelMixin:
    """
    Destroy a model instance.
    """

    def __init_subclass__(cls: generics.GenericAPIMixin, **kwargs):
        super().__init_subclass__(**kwargs)
        if not is_method_overloaded(cls, 'destroy') and cls.model:
            cls.destroy = classmethod(
                MakeMixin.make_destroy(
                    cls.lookup_field,
                    cls.lookup_type,
                )
            )
