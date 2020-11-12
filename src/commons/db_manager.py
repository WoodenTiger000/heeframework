#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 
# @Time    : 2020/11/11 19:12
# @Author  : yanhu.zou
from logging import Logger

from commons.conn_pool import ConnectionPool
from hee_framework import component


# 自动注入
log: Logger = None

# 数据库连接池，自动注入
conn_pool: ConnectionPool = None

@component
class DBManager:

    def __init__(self):
        log.info("数据库组件初始化")

    def execute(self, sql: str):
        conn_pool.get_conn()
        log.info("执行SQL: " + sql)



