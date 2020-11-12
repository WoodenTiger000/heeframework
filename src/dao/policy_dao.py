#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# @Time    : 2020/11/10 17:22
# @Author  : yanhu.zou
from logging import Logger

from commons.db_manager import DBManager
from hee_framework import component

# 自动注入
log: Logger = None

# 自动注入
db: DBManager = None

@component
class PolicyDAO:

    def __init__(self):
        log.info("TestDAO 初始化完成！")

    def select_by_id(self):
        log.info("根据Id查询政策")
        sql = "select * from PA_POLICY"
        db.execute(sql)



