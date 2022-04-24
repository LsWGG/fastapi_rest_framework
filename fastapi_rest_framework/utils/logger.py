#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：LiShun
@File    ：logger.py
@Time    ：2022/3/8 2:57 下午
@Desc    ：
"""
import os
import logging

# 是否将日志打印到控制台
LOG_INFO = os.getenv("LOG_INFO", True)
# 默认为当前路径的上两成目录，fastapi_rest_framework路径下
BASE_DIR = os.getenv("BASE_DIR", os.path.abspath(os.path.dirname(os.getcwd())))


def get_logger(logfile, app_name=""):
    # 创建logger，如果参数为空则返回root logger
    logger = logging.getLogger(logfile)
    logger.setLevel(logging.DEBUG)  # 设置logger日志等级

    # 这里进行判断，如果logger.handlers列表为空，则添加，否则，直接去写日志
    if not logger.handlers:
        # 创建handler
        if app_name:
            log_path = os.path.join(BASE_DIR, "apps", app_name, "logs")
        else:
            log_path = os.path.join(BASE_DIR, "logs")

        if not os.path.exists(log_path):
            os.makedirs(log_path)

        # 设置输出日志格式
        formatter = logging.Formatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %X"
        )

        fh = logging.FileHandler(os.path.join(log_path, logfile), encoding="utf-8")
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        # 只有在开发环境才输出到控制台
        if LOG_INFO:
            ch = logging.StreamHandler()
            ch.setFormatter(formatter)
            logger.addHandler(ch)

    return logger
