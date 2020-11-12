#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# HeeFramework
# @Time    : 2020/11/10 15:06
# @Author  : yanhu.zou
__version__ = "1.0.16"

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
        self.scan_and_load_submod('.')
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
        log_.info("scan path: %s " % path)
        self.cnt += 1
        """
         Scan and load all modules
         This method will scan from the current directory, and if a python file is found, it will be loaded as a submodule.
         After the submodule is successfully loaded, all classes under the module will be scanned and an instance of each class will be created.
         The name of the instance object of this class in the container is: module name + class name.

         If there is a log variable in the submodule, create a Logger object and associate it
         If the submodule ends with the controller, create a route and register it in the route

         Finally, all modules are loaded into the context.
        """
        if path == '__pycache__':
            return

        # Determine if it is a path, process the sub-path recursively
        if os.path.isdir(path):
            for subpath in os.listdir(path):
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


            # Automatic log injection
            if 'log' in dir(submod):
                submod_logger = log4p.GetLogger(logger_name=submod_full_name, config="config/log4p.json")
                submod.log = submod_logger.logger
                log_.info("submod [" + submod_full_name + "] log has been initialized.")


            # save submods
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
                    # The same class is instantiated only once. The class imported in
                    #  TODO is also considered a member of this class.
                    #  I will see if there is a way to exclude it later.
                    #  Currently, the name is used to prevent repeated construction
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
        TODO objects are automatically injected, and the language feature has not found a way to achieve it,
        because there is no way to get the annotations of the object member variables
        For the time being, only module-level dependency injection can be used
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
