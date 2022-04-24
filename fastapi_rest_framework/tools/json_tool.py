#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：LiShun
@File    ：json_tool.py
@Time    ：2022/4/20 15:55
@Desc    ：json读写
"""
import os
import json


def read_json_conf(file_path):
    """
    读取
    @param file_path: 文件位置
    @return: bool
    """
    try:
        with open(file_path, "r") as json_file:
            load_dict = json.load(json_file, encoding="utf-8")
        return load_dict
    except Exception as e:
        return False


def update_json_conf(file_path, json_data):
    """
    更新
    @param file_path: 文件位置
    @param json_data: json数据 <dict>
    @return: bool
    """
    try:
        with open(file_path, 'w') as json_file:
            json_file.write(json.dumps(json_data, indent=4, ensure_ascii=False))
        return True
    except Exception as e:
        return False
