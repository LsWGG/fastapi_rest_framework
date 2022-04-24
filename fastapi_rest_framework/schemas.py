#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：LiShun
@File    ：schemas_pro.py
@Time    ：2022/3/8 10:13 上午
@Desc    ：
"""
import traceback

from typing import Type
from pydantic import BaseModel
from tortoise import Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator

from fastapi_rest_framework.fields import Empty

LIST_SERIALIZER_KWARGS = (
    'exclude', 'include', 'sort_alphabetically', 'many'
)


class BaseSerializerSchemas(BaseModel):
    def __init__(self, instance=None, data=Empty, **kwargs):
        self.instance = instance
        if data is not Empty:
            self.initial_data = data
        # kwargs.pop('many', None)
        super().__init__(**kwargs)

    def __new__(cls, *args, **kwargs):
        # We override this method in order to automatically create
        # `ListSerializer` classes instead when `many=True` is set.
        # todo: Meta和自定义字段待合并
        if hasattr(cls, 'Meta') and getattr(getattr(cls, 'Meta'), 'model'):
            meta = getattr(cls, 'Meta', None)
            model_class = getattr(meta, 'model')
            # Model init, maintenance relationships
            cls.model_init()
            parameter = cls.get_tortoise_parameter(meta)
            if parameter.pop('many', False):
                return cls.many_init(model_class, **parameter)
            else:
                return cls.single_init(model_class, **parameter)
        else:
            return cls

    #
    # # Allow type checkers to make serializers generic.
    # def __class_getitem__(cls, *args, **kwargs):
    #     return cls

    @classmethod
    def model_init(cls):
        if hasattr(cls, 'get_models_paths'):
            return Tortoise.init_models(cls.get_models_paths(), "models")
        else:
            return Tortoise.init_models(["__main__"], "models")

    @classmethod
    def many_init(cls, model_class, **kwargs):
        # todo: pydantic_queryset_creator传入name会引发KeyError，暂未排查原因
        kwargs.pop("name", None)
        return pydantic_queryset_creator(model_class, **kwargs)

    @classmethod
    def single_init(cls, model_class, **kwargs):
        return pydantic_model_creator(model_class, **kwargs)

    @classmethod
    def get_tortoise_parameter(cls, meta):
        par_kwargs = {"name": cls.__name__}
        par_kwargs.update({
            key: getattr(meta, key) for key in LIST_SERIALIZER_KWARGS if hasattr(meta, key)
        })
        return par_kwargs

    # def to_internal_value(self, data):
    #     raise NotImplementedError('`to_internal_value()` must be implemented.')
    #
    # def to_representation(self, instance):
    #     raise NotImplementedError('`to_representation()` must be implemented.')

    def update(self, instance, validated_data):
        raise NotImplementedError('`update()` must be implemented.')

    def create(self, validated_data):
        raise NotImplementedError('`create()` must be implemented.')

    def save(self, **kwargs):
        assert hasattr(self, '_errors'), (
            'You must call `.is_valid()` before calling `.save()`.'
        )

        assert not self.errors, (
            'You cannot call `.save()` on a serializer with invalid data.'
        )

        # Guard against incorrect use of `serializer.save(commit=False)`
        assert 'commit' not in kwargs, (
            "'commit' is not a valid keyword argument to the 'save()' method. "
            "If you need to access data before committing to the database then "
            "inspect 'serializer.validated_data' instead. "
            "You can also pass additional keyword arguments to 'save()' if you "
            "need to set extra attributes on the saved model instance. "
            "For example: 'serializer.save(owner=request.user)'.'"
        )

        assert not hasattr(self, '_data'), (
            "You cannot call `.save()` after accessing `serializer.data`."
            "If you need to access data before committing to the database then "
            "inspect 'serializer.validated_data' instead. "
        )

        validated_data = {**self.validated_data, **kwargs}

        if self.instance is not None:
            self.instance = self.update(self.instance, validated_data)
            assert self.instance is not None, (
                '`update()` did not return an object instance.'
            )
        else:
            self.instance = self.create(validated_data)
            assert self.instance is not None, (
                '`create()` did not return an object instance.'
            )

        return self.instance

    @property
    def errors(self):
        if hasattr(self, '_errors'):
            return self._errors
        else:
            msg = 'You must call `.is_valid()` before accessing `.errors`.'
            raise AssertionError(msg)

    @property
    def validated_data(self):
        if hasattr(self, '_validated_data'):
            return self._validated_data
        else:
            msg = 'You must call `.is_valid()` before accessing `.validated_data`.'
            raise AssertionError(msg)


class ModelSerializerSchemas(BaseSerializerSchemas):
    class Meta:
        model = None

    # def to_representation(self, instance):
    #     pass
    #
    # def to_internal_value(self, data):
    #     pass

    def create(self, validated_data):
        model_class = self.Meta.model
        try:
            instance = model_class.create(**validated_data)
        except TypeError:
            e = traceback.format_exc()
            msg = f"{model_class.__name__} >> {self.__class__.__name__} >> {e}"
            raise msg
        return instance

    def update(self, instance, validated_data):
        instance.update(**validated_data)
        return instance
