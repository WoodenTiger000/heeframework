#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 
# @Time    : 2020/11/17 15:00
# @Author  : yanhu.zou
from logging import Logger

from db import DB

log: Logger = None

import pymysql
import pymysql.cursors
from dbutils.pooled_db import PooledDB


class DbMySQL(DB):
    def __init__(self, host='127.0.0.1', port=6379, user='root', password='111', database='test', pool_max=50, pool_init=2, pool_idle=2):
        self.POOL = PooledDB(
            creator=pymysql,  # 使用链接数据库的模块
            maxconnections=pool_max,  # 连接池允许的最大连接数，0和None表示不限制连接数
            mincached=pool_init,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
            maxcached=pool_idle,  # 链接池中最多闲置的链接，0和None不限制
            maxshared=3,    # 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql和MySQLdb等模块的 threadsafety都为1，所有值无论设置为多少，_maxcached永远为0，所以永远是所有链接都共享。
            blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
            maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
            setsession=[],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
            ping=0,   # ping MySQL服务端，检查是否服务可用。# 如：0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is created, 4 = when a query is executed, 7 = always
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
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute(sql, params)
        results = cursor.fetchall()
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
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute(sql, sql, params)
        results = cursor.fetchone()
        conn.close()
        return results

    def execute(self, sql, params):
        """
        execute
        :param sql:
        :param params:
        :return:
        """
        conn = self.get_conn()
        cursor = conn.cursor()
        row = cursor.execute(sql, params)
        conn.commit()
        conn.close()
        return row

    def get_conn(self):
        """
        Get a connection, remember to return it.
        """
        conn = self.POOL.connection()
        return conn
