#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# HeeFramework
# @Time    : 2020/11/10 15:06
# @Author  : yanhu.zou
__version__ = "1.0.23"

import datetime
import json

"""
HeeFramework

1. Simple to use
    Through the case in the "Instructions section" later, you will find that you will soon be able to use the framework and like it.
   
2. Lightweight and module-oriented
    Hee is lightweight, both in terms of volume and design. It manages its dependencies through the introduction of dynamic modules.
    For example, the framework provides support for MySQL but if you happen to not need MySQL, the application will not introduce any mysql-related packages at startup.
   
3. Low invasiveness
    In addition to decorators to identify the classes you need to let the container manage, almost no additional code is added.

4. Container
    Provide a container to manage the life cycle of an object, and you can even configure how your object will be created.

5. Automatic registration of the controller module
    You only need to create your controller module, and Hee will automatically load and register the controller module you created.

6. Dynamically discover and import user-defined modules
    Provides a dynamic scanning mechanism that can recursively scan each module from the default or specified root path, automatically discover the classes marked in the modules, and automatically create examples of that class.

7. Inversion of Control
    Hee automatically injects object dependencies through the inversion of control technology, including one-way dependencies and two-way dependencies. You don’t need to find or create the dependencies you need,

8. Built-in objects
    Hee will automatically create common objects for each class, such as log objects.

9. Automatically check and import dependencies (TODO) before running
    When Hee starts, it will automatically scan the modules that the framework itself depends on and import them automatically. Of course, what to import depends on which features of the framework you will use.
  


"""

import shutil
import sys
import os
import importlib
import inspect

import log4p
from flask import Flask, Blueprint, request, send_from_directory

from heeconfig import Config

print("heeframework start starts to initialize.")

logger_ = log4p.GetLogger(logger_name=__name__, logging_level="INFO", config="config/log4p.json")
log_ = logger_.logger


class HeeContainer:
    """
    submod and object container.
    """

    def __init__(self):
        # all submods
        self.submods: dict = {}
        # object container
        self.objects: dict = {}
        log_.info("HeeContainer init.")

    def get_obj_by_name(self, obj_name: str):
        if obj_name in self.objects:
            return self.objects[obj_name]
        else:
            return None

    def get_submod_by_name(self, submod_name: str):
        if submod_name in self.submods:
            return self.submods[submod_name]


class Hee:
    """
    Facade of Hee
    """

    def __init__(self, hee_container):
        super(Hee, self).__init__()
        self.__container = hee_container
        log_.info("hee init")

    def get_obj_by_name(self, name: str):
        return self.__container.get_obj_by_name(name)

    def get_sub_mod(self, name: str):
        return self.__container.get_submod_by_name(name)


class HeeApplication:
    """
    HeeApplication
    Building restful applications easily
    The user needs to create a class inherited from this class and execute the start method in the main function to start the application
    """

    def __init__(self):
        # Hee container
        self.hee_container = HeeContainer()

        # Hee
        self.hee = Hee(self.hee_container)

        # Config
        self.config = Config()

        # dynami module MYSQL
        if self.config.has_section('MYSQL'):
            host_ = self.config.get_str('MYSQL', 'host')
            port_ = self.config.get_int('MYSQL', 'port')
            user_ = self.config.get_str('MYSQL', 'user')
            password_ = self.config.get_str('MYSQL', 'pass')
            db_ = self.config.get_str('MYSQL', 'db')
            pool_max_ = self.config.get_int('MYSQL', 'pool_max')
            pool_init_ = self.config.get_int('MYSQL', 'pool_init')
            pool_idle_ = self.config.get_int('MYSQL', 'pool_idle')

            # 初始化数据库管理
            self.dbmysql = DbMySQL(
                host=host_,
                port=port_,
                user=user_,
                password=password_,
                database=db_,
                pool_init=pool_init_,
                pool_max=pool_max_,
                pool_idle=pool_idle_
            )

        # Load all submods.
        log_.info('Start loading SubMod.')
        self.scan_and_load_submod('.')
        for submod in self.hee_container.submods.values():
            log_.info(submod)
        log_.info('All SubMod loaded.')

        # instantiate all objects in the container.
        self.instantiate_objects()

        # Build sub dependencies
        self.build_submod_dependencies()

        # Build object dependencies
        self.build_bean_dependencies()

    def start(self):
        pass

    def scan_and_load_submod(self, path):
        """
         Scan and load all modules
         This method will scan from the current directory, and if a main files is found, it will be loaded as a submodule.
         After the submodule is successfully loaded, all classes under the module will be scanned and an instance of each class will be created.
         The name of the instance object of this class in the container is: module name + class name.

         If there is a log variable in the submodule, create a Logger object and associate it
         If the submodule ends with the controller, create a route and register it in the route

         Finally, all modules are loaded into the context.
        """
        log_.info("scan path: %s " % path)

        # Determine if it is a path, process the sub-path recursively
        if os.path.isdir(path):
            for subpath in os.listdir(path):
                if subpath == './hee':
                    return

                if subpath.endswith('__pycache__'):
                    return

                if subpath == 'static':
                    return

                if subpath == 'template':
                    return

                self.scan_and_load_submod(path + "/" + subpath)

        # If it is a python file, load the processing module
        elif path.endswith(".py"):
            # All files under the root path are skipped
            if path == 'hee_framework':
                return
            # Load all submods
            submod_full_name = path.replace("./", "").replace("/", ".").replace(".py", "")
            log_.info('Load submod: ' + submod_full_name)
            submod = importlib.import_module(submod_full_name)

            # Automatic config injection
            if 'config' in dir(submod):
                submod.config = self.config

            # Automatic log injection
            if 'log' in dir(submod):
                submod_logger = log4p.GetLogger(logger_name=submod_full_name, config="config/log4p.json")
                submod.log = submod_logger.logger
                log_.info("submod [" + submod_full_name + "] log has been initialized.")

            # Automatic hee injection
            if 'hee' in dir(submod):
                submod.hee = self.hee
                log_.info("submod [" + submod_full_name + "] hee has been initialized.")

            # -- flows are dynamic builtin module. --
            # db_mysql dynamic module injection
            if 'db' in dir(submod):
                submod.db = self.dbmysql
                log_.info("submod [" + submod_full_name + "] dynamic module has been initialized.")

            # save submods
            self.hee_container.submods[submod_full_name] = submod

    def instantiate_objects(self):
        """
        Instantiate all objects.
        """
        log_.info("Start instantiating objects")
        # Scan all submod
        for submod_name in self.hee_container.submods:
            classes = inspect.getmembers(self.hee_container.submods[submod_name], inspect.isclass)
            for name, class_ in classes:
                if hasattr(class_, 'hee_dependency_enable'):
                    contained_object_name = class_.__module__ + '.' + class_.__name__
                    # The same class is instantiated only once. The class imported in
                    #  TODO is also considered a member of this class.
                    #  I will see if there is a way to exclude it later.
                    #  Currently, the name is used to prevent repeated construction
                    if contained_object_name not in self.hee_container.objects:
                        obj = class_()  # 初始化示例
                        log_.info("contained object: " + contained_object_name)
                        self.hee_container.objects[contained_object_name] = obj

        log_.info("objects in container: ")
        for key in self.hee_container.objects:
            log_.info("name=" + key + ", object: " + self.hee_container.objects[key].__str__())

    def build_submod_dependencies(self):
        """
        Building sub dependencies.
        After all objects are created successfully, the HeeFramework automatically scans and assembles dependencies
        """
        # Inject dependencies into submods
        log_.info("Start to automatically inject dependencies into the submods.")
        for submod_name in self.hee_container.submods:
            submod = self.hee_container.submods[submod_name]
            # print("submod: ", submod)
            members = inspect.getmembers(submod)
            for m in members:
                if m[0] == '__annotations__':
                    annos = m[1]
                    for var_name in annos:
                        var_type = annos[var_name]
                        contained_object_name = var_type.__module__ + "." + var_type.__name__
                        if contained_object_name in self.hee_container.objects:
                            setattr(submod, var_name, self.hee_container.objects[contained_object_name])
                            log_.info(
                                "Auto inject [" + contained_object_name + "] into submod " + submod_name + " success.")

    def build_bean_dependencies(self):
        """
        Building sub dependencies.
        After all beans are created successfully, the HeeFramework automatically scans and assembles dependencies.
        TODO objects are automatically injected, and the language feature has not found a way to achieve it,
        because there is no way to get the annotations of the object member variables
        For the time being, only module-level dependency injection can be used
        """
        log_.info("Start to automatically inject dependencies into the objects.")
        # Inject dependencies into contained objects
        for obj_name in self.hee_container.objects:
            if obj_name != 'service.ner_data_service.NerDataService':
                continue
            obj = self.hee_container.objects[obj_name]
        #  print("obj.__dict__", obj.__dict__)


class HeeRestApplication(HeeApplication):
    """
    HeeRestApplication
    Used to build restful applications
    """

    def __init__(self):
        static_path = os.getcwd() + os.path.sep + 'static'
        template_path = os.getcwd() + os.path.sep + 'template'
        log_.info("static file path: " + static_path)
        log_.info("tempalte file path: " + template_path)
        super(HeeRestApplication, self).__init__()
        self.heeFlask = Flask(__name__, static_folder=static_path, template_folder=template_path)
        self.web = Web(self.heeFlask)
        self.initialize_controller()

    def initialize_controller(self):
        """
        Map all controllers
        """
        log_.info("Map all controllers.")
        for submod_name in self.hee_container.submods:
            if submod_name.endswith("controller"):
                submod = self.hee_container.submods[submod_name]
                if hasattr(submod, 'mapping'):
                    self.heeFlask.register_blueprint(submod.mapping)

                if hasattr(submod, 'web'):
                    submod.web = self.web
                pass

    def start(self, host="127.0.0.1", port=5000):
        log_.info("application is starting...")
        self.heeFlask.run(host=host, port=port)


class Web:
    """
    If you are building a web application, the web object will be injected into the controller when the controller is initialized. The web object provides the ability to process request parameters, request data acquisition, file download, upload, etc.
    """

    def __init__(self, flask: Flask):
        self.flask: Flask = flask

    def request_params(self):
        return request.args

    def request_data(self):
        return request.data

    def request_files(self):
        return request.files

    def download(self, directory: str, file: str, **options):
        abs_download_dir = os.path.abspath(directory)
        # log_.info("abs_download_file: " + abs_download_dir)
        if not os.path.exists(abs_download_dir):
            return "file not existed!"
        else:
            return send_from_directory(abs_download_dir, file, **options)

    def static_file(self, filename: str):
        """
        根路径
        :param filename:
        :return:
        """
        return self.flask.send_static_file(filename)

    def json(self, data):
        return json.dumps(data, cls=DateEncoder)

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self, obj)

class HeeMapping(Blueprint):
    """
    Used to declare the request path, each controller needs to create an object of this type
    """

    def __init__(self, prefix: str):
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        submod_name = calframe[1][0].f_locals['__name__']
        super(HeeMapping, self).__init__(name=submod_name, import_name=submod_name, url_prefix=prefix)


class HeeWebApplication(HeeRestApplication):
    def __init__(self):
        self.initialize_default_dir()
        super(HeeWebApplication, self).__init__()

    def initialize_default_dir(self):
        """
        Initialize all default paths of the project.
        If it is a web project, it will directly initialize a static path and template path to prevent static files and template files
        :return:
        """
        root_path = os.getcwd()
        if not os.path.exists(root_path + "/static/"):
            os.mkdir(root_path + "/static/")
            log_.info("The static dir does not exists, create it.")
        if not os.path.exists("template/"):
            os.mkdir("template")
            log_.info("The template dir does not exists, create it.")


class HeeSchedApplication(HeeApplication):
    def __init__(self):
        self.initialize_default_dir()
        super(HeeSchedApplication, self).__init__()

    def initialize_default_dir(self):
        """
        If it is a scheduling project, a jobs directory will be initialized to place scheduling tasks
        :return:
        """
        if not os.path.exists("jobs/"):
            os.mkdir("jobs/")
            log_.info("The static dir does not exists, create it.")


def component(cls):
    """
    Component annotation, the annotated class will be automatically instantiated in the container,
    and the instantiated object will be automatically injected when the submodule is initialized.
    """
    cls.hee_dependency_enable = True
    return cls
