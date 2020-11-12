#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 实现对 NerDat 导出的操作
# @FileName: T.py
# @Time    : 2020/11/10 15:06
# @Author  : yanhu.zou
from logging import Logger

import xlwt
import xlrd
import re

from dao.person_dao import PersonDAO
from dao.policy_dao import PolicyDAO
from hee_framework import component


# 依赖注入
log: Logger = None

# 依赖注入
policy_dao: PolicyDAO = None

# 依赖注入
person_dao: PersonDAO = None

@component
class NerDataService:

    def __init__(self):
        self.ner_x = 0

    # 依赖注入测试
    def injection_test(self):
        log.info("ner_test")
        # 先进行政策查询
        policy_dao.select_by_id()
        # 然后查询人物
        person_dao.select_by_name()


    # 行政处罚转为
    def export_excel(self):
        workbook = xlrd.open_workbook("files/455.xlsx")

        sheet0_name = workbook.sheet_names()[0]
        log.info("sheet0_name：" + sheet0_name)

        sheet0 = workbook.sheet_by_index(0)

        workbook = xlwt.Workbook(encoding='utf-8')
        sheetOut = workbook.add_sheet("sheet-000")
        sheetOut.col(9).width = 256 * 100

        log.info("数据总行数：" + sheet0.nrows.__str__())

        detail = ''
        for i in range(sheet0.nrows):
            sheetOut.row(i).height = 69

            for j in range(len(sheet0.row_values(1))):
                if j == 9:  # 第九列是detail
                    # 处理第0行
                    detail = sheet0.row_values(i)[j]
                    # log.info(detail)
                    detail = detail.replace("\n", "\t")  # 清除所有的换行
                    # log.info(detail)

                    # 正则置换html元素
                    table_reg = re.compile('<table.*?>')
                    detail = table_reg.sub('', detail)

                    td_reg = re.compile('<td.*?>')
                    detail = td_reg.sub('', detail)

                    span_reg = re.compile('<span.*?>')
                    detail = span_reg.sub('', detail)

                    tr_reg = re.compile('<tr.*?>')
                    detail = tr_reg.sub('', detail)

                    p_reg = re.compile('<p.*?>')
                    detail = p_reg.sub('', detail)

                    url_reg = re.compile(
                        '(ht|f)tp(s?)://[0-9a-zA-Z]([-.\w]*[0-9a-zA-Z])*(:(0-9)*)*(/?)([a-zA-Z0-9\-.?,\'/\\\+&amp;%$#_]*)?')
                    detail = url_reg.sub('', detail)

                    # 其他特殊置换
                    detail = detail.replace('<tbody>', '')
                    detail = detail.replace("<tr>", "")
                    detail = detail.replace("</tr>", "\n")
                    detail = detail.replace("<td>", "\t")
                    detail = detail.replace("</td>", "\t")
                    detail = detail.replace('</span>', '')
                    detail = detail.replace('</p>', '')
                    detail = detail.replace('&nbsp;', '')
                    detail = detail.replace("<br>", "\t")
                    detail = detail.replace('</tbody>', '')
                    detail = detail.replace('</table>', '')
                    detail = detail.replace('/', '')
                    detail = detail.replace('<th>', '')
                    detail = detail.replace("<table>", '')
                    detail = detail.replace("<table", '')
                    detail = detail.replace(">", '')
                    detail = detail.replace("<strong", '')
                    detail = detail.replace("[登录](javascript:void\\(0\\);)	", "")
                    detail = detail.replace("<b", "")
                    detail = detail.replace("![]()", '')

                    sheetOut.write(i, 9, detail)

                else:
                    sheetOut.write(i, j, sheet0.row_values(i)[j])

            # 打印查看
            print("\n")
            print(
                i.__str__() + '------------------------------------------------------------------------------------------------------------')
            print(detail)

        workbook.save("files/3.xls")