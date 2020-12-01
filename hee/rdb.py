#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 
# @Time    : 2020/11/17 18:11
# @Author  : yanhu.zou
from abc import abstractmethod


class RDB:
    @abstractmethod
    def select_all(self, sql: str, params: dict):
        pass

    @abstractmethod
    def select_one(self, sql: str, params: dict):
        pass

    @abstractmethod
    def execute(self, sql: str, params: dict):
       pass

    def get_conn(self):
        pass