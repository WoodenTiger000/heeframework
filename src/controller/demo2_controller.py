from logging import Logger

from flask import send_from_directory

from hee_framework import HeeMapping
from service.ner_data_service import NerDataService

# 日志，自动注入
log: Logger = None

# 创建映射
mapping: HeeMapping = HeeMapping("/demo2")

# 实体抽取服务，自动注入
ner_data_service: NerDataService = None

@mapping.route('/test')
def test():
    log.info("demo2.log")
    ner_data_service.injection_test()
    return "demo2.test!"

# 下载文件
@mapping.route('/download')
def download():
    return send_from_directory('files', '3.xls')


