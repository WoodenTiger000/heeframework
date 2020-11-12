#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @FileName: Test2.py
# @Time    : 2020/11/10 15:03
# @Author  : yanhu.zou
from hee_framework import *

# TODO 规范
# 1. 报名小写
# 2. 全文件名小写，下划线隔开单词。
# 3. 类名大写，驼峰
# 4. 变量名小写，下划线隔开
#
class Application(HeeRestApplication):
    pass


if __name__ == '__main__':
    app = Application()
    app.start()
