#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：LiShun
@File    ：es_rule_dsl_tool.py
@Time    ：2022/4/20 16:12
@Desc    ：根据指定规则生成DSL查询语句
"""
from fastapi_rest_framework.lib.elasticsearch_dsl import Search, Q


class RuleEsDSL:
    def __init__(self, s_time, e_time, size=10000, dsl_dict=None):
        self.base_dsl_obj = self.__init_base_dsl_obj(s_time, e_time, size, dsl_dict)

    def __init_base_dsl_obj(self, s_time, e_time, size, dsl_dict):
        """
        初始化DSL
        """
        track_total_hits = {"track_total_hits": True}

        # 自定义DSL
        if dsl_dict:
            dsl_dict.update(track_total_hits)
            s = Search.from_dict(dsl_dict)

        # 预加载时间范围
        else:
            if s_time and e_time:
                q = Q("range", **{'start_time': {'lte': e_time}}) & Q("range", **{'start_time': {'gte': s_time}})
            else:
                q = Q()
            # 精确返回总数
            s = Search.from_dict(track_total_hits).filter(q)
            s = s[0:size]

        return s

    def set_source_field(self, fields=None):
        """
        指定返回字段
        @param fields: 字段值 <list>
        @return: None
        """
        self.base_dsl_obj = self.base_dsl_obj.source(fields)

    def get_rule_dsl(self, rule_dict):
        """
        根据规则生成DSL
        """
        for key, value in rule_dict.items():
            if not value.get("value"):
                continue

            # 复杂结构
            elif "." in key:
                nested_path, search_field = key.split(".")
                # 包含
                if value.get("switch") in ("is", u"is"):
                    q = Q("nested", path=nested_path, query=Q("terms", **{key: value.get("value")}))
                # 不包含
                else:
                    q = ~Q("nested", path=nested_path, query=Q("terms", **{key: value.get("value")}))

            # 普通结构
            else:
                # 包含
                if value.get("switch") in ("is", u"is"):
                    q = Q("terms", **{key: value.get("value")})
                # 不包含
                else:
                    q = ~Q("terms", **{key: value.get("value")})
            self.base_dsl_obj = self.base_dsl_obj.filter(q)
        return self.base_dsl_obj.to_dict()
