#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 
# @Time    : 2020/11/12 11:53
# @Author  : yanhu.zou
from hee_framework import component


@component
class Test1:
    def __init__(self):
        print("==============init test1!")

    def hello(self):
        print("test1 say hello!")

