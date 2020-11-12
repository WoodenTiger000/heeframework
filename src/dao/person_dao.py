#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 
# @Time    : 2020/11/11 18:58
# @Author  : yanhu.zou
from logging import Logger

from hee_framework import component

log: Logger = None

@component
class PersonDAO:
    def __init__(self):
        print("Test2DAO 初始化！")

    def select_by_name(self):
        log.info("查询人物")
        return "zhangsan"

