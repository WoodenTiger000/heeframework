#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 
# @Time    : 2020/11/12 11:43
# @Author  : yanhu.zou
from hee_framework import component


@component
class ConnectionPool:
    """
    数据库连接池
    """
    def __init__(self):
        print("初始化连接池！")

    def get_conn(self):
        print("获取连接成功！")