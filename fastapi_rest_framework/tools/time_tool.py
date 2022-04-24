#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：LiShun
@File    ：time_tool.py
@Time    ：2022/4/20 15:56
@Desc    ：时间相关工具集
"""
from __future__ import division

import time
import datetime
import calendar

from fastapi_rest_framework.lib.dateutil.relativedelta import relativedelta


def get_search_time(interval, strf_time="%Y-%m-%d %H:%M:%S", is_ms=False, is_zero=True, zone=False, is_this=False):
    """
    构造start_time & end_time
    interval:作为datetime.timedelta()参数，为当前时间向前推days, seconds,
                microseconds, milliseconds, minutes, hours, weeks
    strf_time:按给定格式以字符串形式返回
    is_ms:是否转为毫秒
    is_zero:是否取零点
    zone:时区
    """
    now = datetime.datetime.now()
    before_date = now - datetime.timedelta(**interval)
    ik = interval.keys()
    if is_zero and u"hours" not in ik and u"minutes" not in ik and u"milliseconds" not in ik and u"microseconds" not in ik and u"seconds" not in ik:
        before_date = before_date.replace(hour=0, minute=0, second=0, microsecond=0)

    # 本年、本月、本周
    if is_this and u"hours" not in interval.keys():
        year = now.year
        month = now.month
        if is_this == "year":
            before_date = datetime.date(year, 1, 1)
        elif is_this == "month":
            before_date = datetime.date(year, month, 1)
        elif is_this == "week":
            before_date = now - datetime.timedelta(days=now.weekday())
        else:
            pass

    start_time = int(time.mktime(before_date.timetuple()))
    end_time = int(time.time())

    if zone:
        start_time += 3600 * 8
        end_time += 3600 * 8
    if is_ms:
        start_time = start_time * 1000
        end_time = end_time * 1000
    elif strf_time:
        start_time = time.strftime(strf_time, time.localtime(start_time))
        end_time = time.strftime(strf_time, time.localtime(end_time))
    return start_time, end_time


def timestamp_to_strftime(timestamp, strf_time="%Y-%m-%d %H:%M:%S", zone=False):
    """
    将时间戳格式化为字符串
    """
    if not isinstance(timestamp, int):
        return timestamp

    if len(str(timestamp)) >= 13:
        timestamp = timestamp / 1000
    if zone:
        timestamp += 3600 * 8
    return time.strftime(strf_time, time.localtime(timestamp))


def datetime_to_strftime(_datetime, strf_time="%Y-%m-%d %H:%M:%S", zone=False):
    """
    将datetime格式化为字符串
    """
    if zone:
        _datetime += datetime.timedelta(hours=8)
    return _datetime.strftime(strf_time)


def strftime_to_timestamp(str_time, strf_time="%Y-%m-%d %H:%M:%S"):
    """
    字符串转时间戳
    str_time和strf_time格式必须一致
    """
    return int(time.mktime(time.strptime(str_time, strf_time)))


def get_month_days(timestamp):
    """
    根据时间戳获取当月天数
    """
    if not isinstance(timestamp, int):
        return timestamp

    if len(str(timestamp)) >= 13:
        timestamp = timestamp / 1000
    localtime = time.localtime(timestamp)
    return calendar.monthrange(localtime.tm_year, localtime.tm_mon)[1]


def get_time_difference(d_timestamp):
    """
    获取时间差值
    """
    now_time = datetime.datetime.fromtimestamp(int(time.time()))
    dst_time = datetime.datetime.fromtimestamp(int(d_timestamp))
    diff = now_time - dst_time
    return diff.days + 1


def get_time_list(interval=7, _type="days", strf_time="%Y-%m-%d", **kwargs):
    """
    按指定范围获取时间序列分组

    interval: 序列范围
    strf_time:格式化形式
    _type:分组形式
        months:每月
        weeks:每周
        days:每天
        hours:每小时
    """
    ret_list = list()

    for i in range(interval + 1):
        date_time = datetime.datetime.now() - relativedelta(**{_type: +i})
        str_time = datetime_to_strftime(date_time, strf_time=strf_time)
        ret_list.append(str_time)
    ret_list.sort(reverse=False)

    return ret_list
