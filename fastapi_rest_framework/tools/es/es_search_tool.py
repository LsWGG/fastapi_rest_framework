#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：LiShun
@File    ：es_search_tool.py
@Time    ：2022/4/20 16:07
@Desc    ：
"""
from fastapi_rest_framework.tools.es.es_tool import EsUtil
from fastapi_rest_framework.tools.es.es_rule_dsl_tool import RuleEsDSL
from fastapi_rest_framework.tools.time_tool import timestamp_to_strftime


class SearchEsData:
    def __init__(self, index, s_time, e_time):
        self.index = index
        self.s_time = s_time
        self.e_time = e_time

    def search_data(self, dsl):
        """
        查询ES数据，整合游标查询
        @param dsl: DSL
        @return: 查询结果
        """
        ret = list()
        es = EsUtil(list())

        try:
            query_nums = es.search(self.index, dsl)
            total_nums = query_nums.get('hits', {}).get('total', {}).get("value", 0)
            print("%s -> %s时间内,索引%s有%s条数据" % (
                timestamp_to_strftime(self.s_time) if self.s_time else "None",
                timestamp_to_strftime(self.e_time) if self.e_time else "None ",
                self.index,
                total_nums
            ))
            if not total_nums:
                return ret

            scroll_msg, res = es.scroll_search(self.index, '1m', dsl)
            if 'hits' not in res.keys():
                return ret

            ret.extend(res["hits"]["hits"])
            i = 1
            while True:
                print("-----进行第<%s>次查询-----" % i)
                scroll_msg, res = es.scroll_next(scroll_msg)  # 滚动查询
                if (not res.get('_scroll_id')) or (not res.get('hits', {}).get('hits')):
                    break
                ret.extend(res["hits"]["hits"])
                i += 1
            es.es.clear_scroll(scroll_msg.get("scroll_id"))
            return ret
        except Exception as e:
            print("查询失败 > %s" % self.index)
            print(e)
            raise e

    def get_dsl(self, rule_dict, fields=None, dsl_dict=None):
        """
        根据规则生成DSL
        @param fields: 指定返回字段
        @param rule_dict: 规则配置
        @param dsl_dict: 自定义DSL
        @return:
        """
        es_obj = RuleEsDSL(s_time=self.s_time, e_time=self.e_time, dsl_dict=dsl_dict)
        # 指定返回字段
        if fields:
            es_obj.set_source_field(fields)
        # 应用查询规则
        dsl = es_obj.get_rule_dsl(rule_dict)

        return dsl
