#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# HeeFramework
# @Time    : 2020/11/10 15:06
# @Author  : yanhu.zou
__version__ = "1.0.6"

"""
HeeFramework

Summary:
A module-oriented comprehensive IOC container framework, 
which realizes the automatic management of dependent components 
and component dependencies, and defines a new python module organization.

Main Feature
1. Dynamically discover and import packages (the root directory scanned by default is application.py, which is the directory where this file is located)

2. Dynamically identify and register the controller

3. Automatically and dynamically instantiate objects

4. Automatic dependency injection

5. Automatically create and associate class variable logger or log

Next Version Plan
1. Automatically check and import dependencies before running

"""
import os
import importlib
import inspect

import log4p
from flask import Flask, Blueprint

logger_ = log4p.GetLogger(logger_name=__name__, logging_level="INFO")
log_ = logger_.logger

heeFlask = Flask(__name__)


class HeeContainer:
    """
    submod and object container.
    """
    def __init__(self):
        # all submods
        self.submods: dict = {}
        # object container
        self.objects: dict = {}

    def get_obj_by_name(self, obj_name: str):
        if obj_name in self.objects:
            return self.objects[obj_name]
        else:
            return None

    def get_submod_by_name(self, submod_name: str):
        if submod_name in self.submods :
            return self.submods[submod_name]


hee_container = HeeContainer()


class Hee:
    """
    Facade of Hee
    """
    def __init__(self):
        super(Hee, self).__init__()
        self.__container = hee_container

    def get_obj_by_name(self, name: str):
        return self.__container.get_obj_by_name(name)

    def get_sub_mod(self, name: str):
        return self.__container.get_submod_by_name(name)


class HeeMapping(Blueprint):
    def __init__(self, prefix: str):
        print("a11")
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        submod_name = calframe[1][0].f_locals['__name__']
        super(HeeMapping, self).__init__(name=submod_name, import_name=submod_name, url_prefix=prefix)



class HeeApplication:
    """
    HeeApplication
    Building restful applications easily
    The user needs to create a class inherited from this class and execute the start method in the main function to start the application
    """

    def __init__(self):
        # Hee
        self.hee = Hee()

        self.cnt = 0

        # Load all submods.
        log_.info('Start loading SubMod.')
        self.scan_and_load_submod('src')
        for submod in hee_container.submods.values():
            log_.info(submod)
        log_.info('All SubMod loaded.')

        # instantiate all objects in the container.
        self.instantiate_objects()

        # Build sub dependencies
        self.build_submod_dependencies()

        # Build object dependencies
        self.build_bean_dependencies()



    def sart(self):
        pass


    def scan_and_load_submod(self, path):
        log_.info("迭代%-4i path=%-30s " % (self.cnt, path))
        self.cnt += 1
        """
        扫描并加载所有的模块
        该方法会从当前目录下往下进行扫描，如果有发现有python文件，则将其加载为子模块。
        加载子模块成功后，会扫描模块下的所有类，创建每个类的实例，
        容器中该类的实例对象的名称为：模块名 + 类名。

        如果子模块中有log或logger变量，则创建Logger对象，并进行关联
        如果子模块是以Controller结尾的，则创建路由，并将其注册到路由中

        最终将所有的模块加载到上下文中。
        """
        if path == '__pycache__':
            return

        # 判断如果是路径，递归处理子路径
        if os.path.isdir(path):
            for subpath in os.listdir(path):
                self.scan_and_load_submod(path + "/" + subpath)

        # 如果是一个python文件，加载处理模块
        elif path.endswith(".py"):
            # 根路径下的所有文件都跳过
            if path == 'hee_framework':
                return
            # 加载所有的子模块
            submod_full_name = path.replace("./", "").replace("/", ".").replace(".py", "")
            log_.info('Load submod: ' + submod_full_name)
            submod = importlib.import_module(submod_full_name)


            # 自动注入 log
            if 'log' in dir(submod):
                submod_logger = log4p.GetLogger(logger_name=submod_full_name, config="config/log4p.json")
                submod.log = submod_logger.logger
                log_.info("submod [" + submod_full_name + "] log has been initialized.")


            # 将子模块引用进行归档
            hee_container.submods[submod_full_name] = submod


    def instantiate_objects(self):
        """
        Instantiate all objects.
        """
        log_.info("Start instantiating objects")
        # Scan all submod
        for submod_name in hee_container.submods:
            classes = inspect.getmembers(hee_container.submods[submod_name], inspect.isclass)
            for name, class_ in classes:
                if hasattr(class_, 'hee_dependency_enable'):
                    contained_object_name = class_.__module__ + '.' + class_.__name__
                    # 同一个类仅实例化一次，TODO 因为import进来的类也算本类的成员，后面看是否有办法排除掉，目前通过名称防止重复构建
                    if contained_object_name not in hee_container.objects:
                        obj = class_()  # 初始化示例
                        log_.info("contained object: " + contained_object_name)
                        hee_container.objects[contained_object_name] = obj

        log_.info("objects in container: ")
        for key in hee_container.objects:
            log_.info("name=" + key + ", object: " + hee_container.objects[key].__str__())


    def build_submod_dependencies(self):
        """
        Building sub dependencies.
        After all objects are created successfully, the HeeFramework automatically scans and assembles dependencies
        """
        # Inject dependencies into submods
        log_.info("Start to automatically inject dependencies into the submods.")
        for submod_name in hee_container.submods:
            submod = hee_container.submods[submod_name]
            # print("submod: ", submod)
            members = inspect.getmembers(submod)
            for m in members:
                if m[0] == '__annotations__':
                    annos = m[1]
                    for var_name in annos:
                        var_type = annos[var_name]
                        contained_object_name = var_type.__module__ + "." + var_type.__name__
                        if contained_object_name in hee_container.objects:
                            setattr(submod, var_name, hee_container.objects[contained_object_name])
                            log_.info(
                                "Auto inject [" + contained_object_name + "] into submod " + submod_name + " success.")


    def build_bean_dependencies(self):
        """
        Building sub dependencies.
        After all beans are created successfully, the HeeFramework automatically scans and assembles dependencies.
        TODO 对象自动注入，语言特性暂无找到可以实现的方式，因为找不到可以获取 对象成员变量注解的途径
        暂时只能使用模块级别的依赖注入
        """
        log_.info("Start to automatically inject dependencies into the objects.")
        # Inject dependencies into contained objects
        for obj_name in hee_container.objects:
            if obj_name != 'service.ner_data_service.NerDataService':
                continue
            obj = hee_container.objects[obj_name]
        #  print("obj.__dict__", obj.__dict__)

class HeeRestApplication(HeeApplication):
    """
    HeeRestApplication
    Used to build restful applications
    """

    def __init__(self):
        super(HeeRestApplication, self).__init__()
        self.initialize_controller()

    def initialize_controller(self):
        """
        Map all controllers
        """
        log_.info("Map all controllers.")
        for submod_name in hee_container.submods:
            if submod_name.endswith("controller"):
                submod = hee_container.submods[submod_name]
                if hasattr(submod, 'mapping'):
                    heeFlask.register_blueprint(submod.mapping)

                pass

    def start(self):
        log_.info("application is starting...")
        heeFlask.run()





class HeeWebApplication(HeeApplication):
    pass


class HeeSchedApplication(HeeApplication):
    pass




def component(cls):
    """
    Component annotation, the annotated class will be automatically instantiated in the container,
    and the instantiated object will be automatically injected when the submodule is initialized.
    """
    cls.hee_dependency_enable = True
    return cls
