#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 
# @Time    : 2020/11/17 15:00
# @Author  : yanhu.zou
import datetime
from logging import Logger

import log4p

from hee.rdb import RDB

import pymysql
import pymysql.cursors
from dbutils.pooled_db import PooledDB

logger_ = log4p.GetLogger(logger_name=__name__, logging_level="INFO", config="config/log4p.json")
log = logger_.logger
"""
    容易出错的点：
    1. 在执行select或者execute方法时，传入参数一定要用小括号，不能用大阔号，这两个很难肉分的清的
"""


class DbMySQL(RDB):
    def __init__(self, host='127.0.0.1', port=6379, user='root', password='111', database='test', pool_max=50,
                 pool_init=2, pool_idle=2):
        self.POOL = PooledDB(
            creator=pymysql,  # 使用链接数据库的模块
            maxconnections=pool_max,  # 连接池允许的最大连接数，0和None表示不限制连接数
            mincached=pool_init,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
            maxcached=pool_idle,  # 链接池中最多闲置的链接，0和None不限制
            maxshared=3,
            # 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql和MySQLdb等模块的 threadsafety都为1，所有值无论设置为多少，_maxcached永远为0，所以永远是所有链接都共享。
            blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
            maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
            setsession=[],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
            ping=0,
            # Ping MySQL服务端，检查是否服务可用。# 如：0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is created, 4 = when a query is executed, 7 = always
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            charset='utf8'
        )

    def select_all(self, sql, params):
        """
        select all data
        :param params:
        :param sql:
        :return:
        """
        conn = self.get_conn()
        try:
            cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

            # 参数格式化
            final_sql = self._build_sql(sql, params)
            log.info("final_sql: " + final_sql)

            cursor.execute(final_sql)
            results = cursor.fetchall()
        finally:
            conn.close()
        return results

    def select_one(self, sql, params):
        """
        select all data
        :param params:
        :param sql:
        :return:
        """
        conn = self.get_conn()
        try:
            cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

            # 参数格式化
            final_sql = self._build_sql(sql, params)
            log.info("final_sql: " + final_sql)

            cursor.execute(final_sql)
            results = cursor.fetchone()
            return results
        finally:
            conn.close()

    def execute(self, sql: str, params: dict):
        """
        execute
        :param sql:
        :param params:
        :return:
        """
        conn = self.get_conn()
        try:
            cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

            # 参数格式化
            final_sql = self._build_sql(sql, params)
            log.info("final_sql: " + final_sql)

            row = cursor.execute(final_sql)
            conn.commit()
            return row
        finally:
            conn.close()

    # 构建查询语句，将#{param_name}替换为真正的值
    def _build_sql(self, sql, params):
        if params is None:
            return sql

        # TODO 时间关系，暂时先用replace的方式，另一种更高效的写法是通过对sql str中的字符进行遍历，
        # TODO 当遇到#和{时进行缓存，当遇到}时将参数值进行置换。

        # 转义单引号
        final_sql: str = sql

        for param_name in params:
            param_value = params[param_name]

            # int
            if isinstance(param_value, int) or isinstance(param_value, float):
                final_sql = final_sql.replace('#{' + param_name + '}', param_value.__str__())
            # datetime
            elif isinstance(param_value, datetime.datetime):
                param_value = '\'' + param_value.__str__().split('.')[0] + '\''
                final_sql = final_sql.replace('#{' + param_name + '}', param_value)
            # None
            elif param_value is None:
                final_sql = final_sql.replace('#{' + param_name + '}', '\'\'')
            # dict
            elif isinstance(param_value, dict):
                final_sql = final_sql.replace('#{' + param_name + '}', '\"' + param_value.__str__() + '\"')
            # Other
            else:
                # 将参数中的单引号全部进行转义
                param_value = param_value.__str__().replace("'", "''")
                final_sql = final_sql.replace('#{' + param_name + '}', '\'' + param_value + '\'')

        return final_sql

    def get_conn(self):
        """
        Get a connection, remember to return it.
        """
        conn = self.POOL.connection()
        return conn

