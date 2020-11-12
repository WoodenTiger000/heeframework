from flask import Blueprint, request, jsonify
from logging import Logger

# flask自动分模块方案，
# 注意1：DemoController名字不能跟其他的Controller重复
# 注意2：blueprint变量名称不能改变
from hee_framework import HeeMapping
from service.test_service import TestService

# 自动注入
log: Logger = None

# 创建映射
mapping = HeeMapping("/demo1")

# 自动注入
test_service: TestService = None


@mapping.route('/test')
def test():
    log.info("demo1.log")
    test_service.test1()
    return "demo1.test!"


# 测试例子，接收json，并返回json
@mapping.route('/json-test', methods=['POST'])
def json_test():

    req_body = request.get_json()
    log.info("request info: %s" % req_body)

    resp_info = {"code": "000000", "desc": "响应成功", "data": {"userId": "11111", "password": 2222}}

    resp_body = jsonify(resp_info)

    return resp_body
