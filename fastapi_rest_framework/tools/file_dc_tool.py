#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：LiShun
@File    ：file_dc_tool.py
@Time    ：2022/4/20 16:26
@Desc    ：文件压缩解压缩工具
"""
import shutil

import rarfile
import tarfile


class RarUtil:
    def __init__(self, s_path, d_path):
        self.s_path = s_path
        self.d_path = d_path

    def decompress(self):
        """
        解压
        :return:
        """
        r = rarfile.RarFile(self.s_path)
        r.extractall(self.d_path)
        return self.d_path

    def compress(self):
        """
        压缩
        :return:
        """
        return self.d_path


class ZipUtil:
    def __init__(self, s_path, d_path):
        self.s_path = s_path
        self.d_path = d_path

    def decompress(self):
        """
        解压
        :return:
        """
        shutil.unpack_archive(self.s_path, extract_dir=self.d_path, format="zip")
        return self.d_path

    def compress(self):
        """
        压缩
        :return:
        """
        ret = shutil.make_archive(self.d_path, "zip", self.s_path)
        return self.d_path


class GzUtil:
    def __init__(self, s_path, d_path):
        self.s_path = s_path
        self.d_path = d_path

    def decompress(self):
        """
        解压
        :return:
        """
        t = tarfile.open(self.s_path)
        t.extractall(self.d_path)
        return self.d_path

    def compress(self):
        """
        压缩
        :return:
        """
        return self.d_path


def main(_type):
    index = {
        "rar": RarUtil,
        "zip": ZipUtil,
        "gz": GzUtil,
    }
    return index.get(_type)
