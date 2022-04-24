#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：LiShun
@File    ：file_dispose_tool.py
@Time    ：2022/4/20 16:22
@Desc    ：
"""
import os
import abc
import time

import pandas as pd


class FileUtil:
    def __init__(self, s_path):
        self.s_path = s_path
        self.chunk_size = 100000
        self.suffix = os.path.splitext(s_path)[1][1:]

    @staticmethod
    def init_path(path):
        if not os.path.exists(path):
            os.makedirs(path)

    def get_size(self):
        return os.path.getsize(self.s_path)

    def is_size(self):
        if self.get_size() < 10000000:
            return True
        else:
            return False

    def res_info(self, rows):
        return f"{os.path.basename(self.s_path)} has load {rows} data"

    @abc.abstractmethod
    def dataframe(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def get_shape(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def write(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def to_file(self, *args, **kwargs):
        pass


class PdUtil(FileUtil):

    def dataframe(self, *args, **kwargs):
        read_obj = getattr(pd, "read_" + self.suffix)
        if self.is_size():
            df = read_obj(self.s_path, *args, **kwargs)
            yield df
        else:
            reader = read_obj(self.s_path, chunksize=self.chunk_size, *args, **kwargs)
            for item in reader:
                yield item

    def get_shape(self, *args, **kwargs):
        rows = 0
        columns = 0
        df = self.dataframe(*args, **kwargs)
        for d in df:
            row, column = d.shape
            rows += row
            columns = column
        return rows, columns

    def write(self, *args, **kwargs):
        pass

    def to_file(self, d_path, to_suffix, *args, **kwargs):
        df = self.dataframe()
        for d in df:
            row, column = d.shape
            d_path = os.path.splitext(os.path.basename(d_path))[0] + f"_{row}_{str(int(time.time()))}.csv"
            to_obj = getattr(df, "to_" + to_suffix)
            to_obj(d_path, *args, **kwargs)
        return d_path


def main(path, custom_index=None, read_action=None):
    """pd版文件转换工具入口
    :param path: 需要操作的源文件路径
    :param custom_index: 可扩展的工具集映射
        {
            "txt": <type: class>,
            "ldif": <type: class>,
        }
    :param read_action: 指定pd读取方式
    """
    suffix = os.path.splitext(path)[1][1:]
    if custom_index:
        assert issubclass(dict, custom_index), (
            "custom_index must is dict"
        )
        return custom_index.get(suffix)

    elif read_action:
        assert hasattr(pd, read_action), (
            "read_action is invalid"
        )
        return getattr(pd, read_action)

    elif hasattr(pd, "read_" + suffix):
        return PdUtil(path)

    else:
        raise Exception("暂未支持的文件")
