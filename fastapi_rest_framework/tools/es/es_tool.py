#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：LiShun
@File    ：es_tool.py
@Time    ：2022/4/20 16:01
@Desc    ：
"""

import datetime
import json
import traceback
from elasticsearch import Elasticsearch
from elasticsearch import helpers

# 默认type
TYPE = '_doc'


class EsUtil(object):
    es_client = None

    def __init__(self, es_host_list):
        if not EsUtil.es_client:
            EsUtil.es_client = Elasticsearch(es_host_list,
                                             timeout=60,
                                             max_retries=10,
                                             retry_on_timeout=True)
        self.es = EsUtil.es_client

    def get_client(self):
        """
        提供原生的es_Client
        :return:
        """
        return self.es

    def is_index_exist(self, index_name):
        return self.es.indices.exists(index=index_name)

    def get_available_index(self, start_time=None, end_time=None, prefix=None, suffix=None):
        results = list()
        index_ = "*"
        start_date = None
        end_date = None
        if prefix:
            index_ = prefix + index_
        if suffix:
            index_ = index_ + suffix
        res = self.es.cat.indices(index=index_, format="json")
        if start_time:
            start_date = datetime.datetime.fromtimestamp(start_time / 1000).strftime("%Y%m%d")

        if end_time:
            end_date = datetime.datetime.fromtimestamp(end_time / 1000).strftime("%Y%m%d")

        for ind in res:
            indices = ind.get('index', '').split('-')
            if start_date and len(indices) > 1:
                if indices[-2] < start_date:
                    continue
            if end_date and len(indices) > 1:
                if indices[-2] > end_date:
                    continue
            results.append(ind)
        return results

    def get_available_index_name(self, start_time=None, end_time=None, prefix=None, suffix=None):
        results = list()
        indices = self.get_available_index(start_time, end_time, prefix, suffix)
        if not indices:
            return results
        for index_ in indices:
            results.append(index_.get("index"))
        return results

    def search(self, index_name, request_body, request_params=dict()):
        """
        查询接口（原生）
        :param request_params:
        :param index_name:
        :param request_body:
        :return:
        """
        return self.es.search(index=index_name, body=request_body, params=request_params, request_timeout=60)

    def scroll_search(self, index_name, scroll, request_body, request_params=dict()):
        """
        通过快照进行分页查询,并返回第一个快照查询的结果和快照的id，用于继续查询
        注：此查询只能不停的向后查询，不能返回上一页
        :param request_params:
        :param index_name 索引名称
        :param scroll 快照保留的时间
        :param request_body 查询的请求参数
        :return: response为查询的数据，scroll_msg返回，并用于获取下一次的快照信息,scroll_size可用于跳出循环后记录开始from
        """
        response = self.es.search(index=index_name, scroll=scroll, body=request_body, params=request_params,
                                  request_timeout=60)
        scroll_msg = {'scroll_id': response.get('_scroll_id'), 'scroll': scroll}
        return scroll_msg, response

    def scroll_next(self, scroll_msg, request_params=dict()):
        """
        传入scroll_search返回的第一个参数，用于获取下一次的快照
        :param request_params:
        :param scroll_msg:
        :return:
        """
        response = self.es.scroll(body=scroll_msg, params=request_params)
        scroll_msg = {'scroll_id': response.get('_scroll_id'), 'scroll': scroll_msg.get('scroll')}
        return scroll_msg, response

    def delete_index(self, index_name):
        """
        删除索引
        :param index_name:
        :return:
        """
        return self.es.indices.delete(index=index_name)['acknowledged']

    def index(self, index_name, request_body):
        """
        单条doc插入
        :param index_name 索引名称
        :param request_body 请求数据dict
        {
          "name": "Alice",
          "address": "武汉",
          "age": 1,
          "birthday": "2019-06-03T18:47:45.999"
        }
        :return:
        """
        return self.es.index(index=index_name, doc_type=TYPE, body=request_body).get('result')

    def bulk_insert(self, index_name, data_list):
        """
        批量插入
        :return:
        """
        actions = list()
        for data in data_list:
            action = {
                "_index": index_name,
                "_type": TYPE,
                '_source': data
            }
            actions.append(action)

        # print json.dumps(actions)
        return helpers.bulk(self.es, actions)

    def search_after_start(self, index_name, request_body):
        """
        通过elasticsearch search after 避免深度分页的问题
        :return:
        """
        if request_body.get('size') is None and request_body.get('sort') is None:
            raise Exception('request body is not validate')
        response = self.es.search(index=index_name, body=request_body)
        search_after_body = {
            'size': request_body.get('size'),
            'sort': request_body.get('sort'),
            'search_after': request_body.get('hits', {}).get('hits', {}).get('sort')
        }
        return search_after_body, response

    def search_after(self, index_name, search_after_body):
        """
        search_after
        :param index_name:
        :param search_after_body
        :return:
        """
        response = self.es.search(index=index_name, body=search_after_body)

        search_after_body = {
            'size': search_after_body.get('size'),
            'sort': search_after_body.get('sort'),
            'search_after': response.get('hits', {}).get('hits', {}).get('sort')
        }
        return search_after_body, response
