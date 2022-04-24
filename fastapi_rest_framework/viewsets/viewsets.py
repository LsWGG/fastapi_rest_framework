#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：LiShun
@File    ：router.py
@Time    ：2022/3/9 9:19 上午
@Desc    ：
"""
from fastapi import APIRouter

from fastapi_rest_framework.viewsets import mixins
from fastapi_rest_framework.viewsets import generics


class GenericViewSet(generics.GenericAPIMixin):
    """
    The GenericViewSet class does not provide any actions by default,
    but does include the base set of generic view behavior, such as
    the `get_object` and `get_queryset` methods.
    todo: .as_view()与动态添加类方法为路由冲突，先不继承ViewSetMixin。
    """
    pass


class ReadOnlyModelViewSet(mixins.RetrieveModelMixin,
                           mixins.ListModelMixin,
                           GenericViewSet):
    """
    A viewset that provides default `list()` and `retrieve()` actions.
    """
    pass


class ModelViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   GenericViewSet):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `destroy()` and `list()` actions.
    """
    pass
