### **【HeeFramework】**
***


#### 1 Overview
HeeFramewrok (Hee for short) is a module-oriented, low-invasive IOC container framework, created to solve the problem of building enterprise-level complex software.
Hee provides a container to manage the life cycle and component dependencies of each component object. Hee defines a new module organization.

#### 2 Main features and functions
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
    
#### 3 User Guide
##### 3.1 Install Hee
````
    pip install hee-framework -i https://pypi.org/simple
````

##### 3.2 Hee Application
###### 3.2.1 How to create a Hee ordinary application
Create an application.py under the root path of your project source code (the file name is not fixed, you can name it yourself), and then write the content.
````python
from heeframework import HeeApplication

class Application(HeeApplication):
    # your code
    pass


if __name__ =='__main__':
    app = Application()
    # your logic
    input() # replace with other
````
After writing, execute python3 application.py to start the project.


###### 3.2.2. How to create a Hee Restful application
Create an application.py under the root path of your project source code (the file name is not fixed, you can name it yourself), and then write the content.
````python
from heeframework import HeeRestApplication

class Application(HeeRestApplication):
    # your code
    pass

if __name__ =='__main__':
    app = Application()
    app.start()
````
After writing, python3 application.py can start the project


###### 3.2.3 How to create a scheduling batch application
Create an application.py under the root path of your project source code (the file name is not fixed, you can name it yourself), and then write the content.
````python
from heeframework import HeeScheduledApplication

class Application(HeeScheduledApplication):
    # your code
    pass

if __name__ =='__main__':
    app = Application()
    app.start()
````
After writing, python3 application.py can start the project

##### 3.3 Controller
The controller refers to the first barrier for processing http requests from the Internet, and is mainly used for various control capabilities, including parameter authentication control, permission control, verification control, process control, return control, and so on.
##### 3. How to create a controller module
Create a controller folder in your root directory, create a foo_controller.py file, and write the content. The controller will be automatically registered to the app, you don't need any other operations.
````python
from heeframework import HeeMapping

mapping:HeeMapping = HeeMapping("/foo")

@mapping.route("/find")
def find():
    print("finding bar!")
    return "bar"
````
When the above is completed, start your Application as before, and then you can enter in the browser: http://localhost:5000/foo/find, if you return to the bar correctly, congratulations, you have successfully written your first A controller!


##### 3.4 Submodule
Create a subfolder service in the directory where your HeeApplication is located. Any .py file created in the service folder will be treated as a submod, and the submodule will be automatically imported into the container for management.
The sub-modules will be scanned by Hee and added to the Hee container.
We now create a foo_service.py in the service directory and write the following:
````python
from logging import Logger
from heeframework import component

# Automatic injection
log: Logger = None

@component
class FooService:
    def __init__(self):
        pass

    def do_something(self):
        log.info("do my business!")
        return "my business done"
````
Note 1: The FooService class has a @component decoration, which is a very important decorator, which means that the container will create a component and hand it over to the container for management.
Note 2: This module has a log member that is None. As mentioned earlier, changing log is a built-in object of Hee, and Hee will automatically inject it, so don't worry about its value as None.

#### 3.5 Inversion of Control
The core idea of ​​inversion of control is that you don't want to find or create dependent objects from the container, but pass it to you in a passive way.
Here we let Hee automatically inject an instance of FooService into FooController. We modify foo_controller to the following:
````python
from logging import Logger

from heeframework import HeeMapping
from modules.service.foo_service import FooService

mapping = HeeMapping("/foo")

# log
log: Logger = None

# foo service, auto injection
foo_service: FooService = None

@mapping.route("/find")
def find():
    log.info(foo_service.do_something())
    return "bar"

````

OK, after the modification is completed, we restart the application, and enter: http://localhost:5000/foo/find in the browser, you will see in the log:
````
2020-11-13 15:02:27,562-foo_service.py line+18-INFO-do my business!
2020-11-13 15:02:27,563-foo_controller.py line+21-INFO-my business done
````
Congratulations again, you made it!



#### 3 Upgrade plan
1. dynamic framework module support [like mybatis]
2. dynamic framework module support [kafka]
3. dynamic framework module support [redis]