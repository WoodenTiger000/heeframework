#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 
# @Time    : 2020/11/11 19:04
# @Author  : yanhu.zou
from logging import Logger

# 自动注入
from commons.subdir.test1 import Test1
from dao.person_dao import PersonDAO
from hee_framework import component

log: Logger = None

# 自动注入
person_dao: PersonDAO = None

# 自动注入
test1: Test1 = None

@component
class TestService:

    def __init__(self):
        log.info("初始化TestService")

    def test1(self):
        log.info("测试业务")
        name = person_dao.select_by_name()

        test1.hello()

        return name
