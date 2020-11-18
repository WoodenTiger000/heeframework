#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 
# @Time    : 2020/11/17 18:11
# @Author  : yanhu.zou
from abc import abstractmethod


class DB:
    @abstractmethod
    def select_all(self, sql, params=None):
        pass

    @abstractmethod
    def select_one(self, sql, params=None):
        pass

    @abstractmethod
    def execute(self, sql, params=None):
       pass