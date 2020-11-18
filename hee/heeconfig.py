#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 
# @Time    : 2020/11/17 15:02
# @Author  : yanhu.zou
import configparser


class Config:
    """
    Config component
    """

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config/app.conf', encoding='UTF-8')
        pass

    def has_section(self, section: str):
        return self.config.has_section(section)

    def get_section(self, section: str):
        """
        return it If exists, return None if it does not exist.
        :param section:
        :return:
        """
        if self.config.has_section(section):
            return self.config[section]
        return None

    def get_str(self, section: str, key: str):
        """
        get config properties
        :param section:
        :param key:
        :return:
        """
        if self.config.has_section(section):
            return self.config[section].get(key)
        else:
            return None

    def get_int(self, section: str, key: str):
        if self.config.has_section(section):
            return int(self.config[section].get(key))
        else:
            return None
