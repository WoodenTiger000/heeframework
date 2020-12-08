# **【HeeFramework】**
***
！先放到监控项目里面写

## 1 概要  
HeeFramewrok（以下简称Hee） 是一款面向模块的低侵入式的IOC容器框架，为解决构建企业级复杂软件而创建的。
Hee提供了一个容器来管理各个组件对象的生命周期和组件依赖性，并定义了一个新的模块组织方式。

## 2 主要特征及功能  
**1. 易于使用**  
    通过之后"使用说明章节"中的案例，您将会发现很快您就能上手使用该框架，并喜欢上它。
   
**2. 轻量级和面向模块**    
    Hee是轻量的，无论从体积上还是设计上。它通过动态模块引入机制来管理自身的依赖。
    比如框架对MySQL提供了支持但如果您恰好不需要MySQL时，应用在启动时并不会引入mysql相关的任何包。
   
**3. 低侵入性**   
    除了修饰器来标识您需要让容器管理的类外，几乎不会增加其他任何外的代码。

**4. 容器**  
    提供一个容器来管理对象的生命周期，您甚至可以配置您的对象将被如何创建。

**5. 控制器模块的自动注册**  
    您只需要创建您的控制器模块，Hee会自动将您创建的控制器模块进行加载和注册。

**6. 动态发现和导入用户自定义的模块**  
    提供动态扫描机制，能够从默认或指定的根路径下递归扫描各个模块，自动发现模块中标注的类，并自动创建该类的示例。

**7. 控制反转**  
    Hee通过控制反转技术自动注入对象依赖，包括单向依赖的和双向依赖。不需要您查找或者去创建您所需要的依赖，

**8. 内置组件**  
    Hee会为每个类自动创建通用的对象，比如说log对象。

**9. 在运行之前自动检查和导入依赖项 (TODO)**  
    Hee在启动时会自动扫描所框架自身依赖的模块，并自动导入。当然，导入哪些取决于您将要用到框架的哪些功能。

**10. 提供Web抽象层，简化Restful应用和Web应用的构建**  
    Hee启动时会给需要的控制器组件自动注入web对象，web对象可支持大多数的web操作，比如文件上传、下载。

## 3 涉及概念
### 3.1 动态模块
   动态模块是一种按需加载的内置模块，如果你在配置文件中出现了该模块的相关段落，则自动下载该动态模块的依赖，并初始化该动态模块。  
   如果没有配置该模块，则不会加载该模块的任何内容  

 
## 3 快速开始（小试牛刀）  
### 3.1 安装Hee
````
    pip3 install heeframework -i https://pypi.org/simple
````

### 3.2 Hee应用
#### 3.2.1 Hee IOC普通应用（HeeApplication）  
Hee IOC普通应用即为一个普通的应用程序，它与原生的Python程序的不同点在于提供了模块自动发现，对象容器和基于控制反转的依赖注入能力。
当然，普通应用亦能够使用Hee提供的丰富内置组件。

在你的工程源码根路径下创建一个application.py(文件名不是固定的，你完全自己可以取名字)，然后写入以下内容。
````python
from hee import HeeApplication

class Application(HeeApplication):
    # your code
    pass


if __name__ == '__main__':
    app = Application()
    # your logic
    input()   # replace with other
````
完成之后，执行 python3 application.py 即可启动该项目。


#### 3.2.2. Hee Restful应用(HeeRestApplication)  
在你的工程源码根路径下创建一个application.py(文件名不是固定的，你完全自己可以取名字)，然后写入以下内容。
````python
from hee import HeeRestApplication

class Application(HeeRestApplication):
    # your code
    pass

if __name__ == '__main__':
    app = Application()
    app.start()
````
写完之后，python3 application.py 即可启动该项目。
启动之后会自动生成配置目录：config/app.conf，config/log4p.json。  

#### 3.2.3. Hee Web应用(HeeWebApplication)  
在你的工程源码根路径下创建一个application.py(文件名不是固定的，你完全自己可以取名字)，然后写入以下内容。
````python
from hee import HeeWebApplication

class Application(HeeWebApplication):
    # your code
    pass

if __name__ == '__main__':
    app = Application()
    app.start()
````
写完之后，python3 application.py 即可启动该项目。
启动之后会自动生成配置目录：config/app.conf，config/log4p.json。  


#### 3.2.4 如何创建一个调度批处理应用(HeeSchedApplication)  
在你的工程源码根路径下创建一个application.py(文件名不是固定的，你完全自己可以取名字)，然后写入以下内容。
````python
from hee import HeeSchedApplication

class Application(HeeSchedApplication):
    # your code
    pass

if __name__ == '__main__':
    app = Application()
    app.start()
````
完成之后，python3 application.py 即可启动该项目

### 3.3 控制器
当你构建的是一个HeeRestApplication或者HeeWebApplication时，控制器将会是一个必不可少的子模块组件。
控制器是处理来自互联网的http请求的第一道屏障，主要用于各种控制能力，包括参数认证控制、权限控制、校验控制、流程控制，返回控制等等。
#### 3.3.1 如何创建一个控制器模块
在您的根目录下创建一个controller文件夹，创建 foo_controller.py 文件，并写入以下内容。控制器将会被自动注册到应用程序，您无需任何其他操作。
````python
from hee import HeeMapping

mapping:HeeMapping = HeeMapping("/foo")

@mapping.route("/find")
def find():
    print("finding bar!")
    return "bar"
````
当以上完成后，像前面一样启动您的的Application，随后就可以在浏览器中输入：http://localhost:5000/foo/find，如果正确返回bar，恭喜您，您成功编写了您的第一个controller！


##### 3.4 子模块
在你HeeApplication所在的目录创建子文件夹service，service文件夹中创建的任何.py文件将会视为子模块(submod)，子模块将会自动导入容器进行管理。
子模块会被Hee扫描，并加入Hee容器。
我们现在在service目录创建一个foo_service.py，并写入以下内容: 
````python
from logging import Logger
from hee import component

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
提示1：FooService类有一个@component装饰，这是一个非常重要的装饰器，表示容器会创建一个component并交由容器进行管理。
提示2：该模块有一个为None的log成员，前面提到过，该log是Hee内置对象，Hee会将其自动注入，不需要对依赖进行手工查找。
提示3：我们可以将组件按职责划分为不同的层级。

#### 3.5 控制反转与依赖注入
控制反转的核心思想是，你不要从容器查找或者自己去创建依赖的对象，而是通过被动的方式传递给你。
这里我们让Hee给FooController自动注入FooService的实例。我们修改foo_controller为以下：
````python
from logging import Logger

from hee import HeeMapping
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

OK, 修改完成之后，我们重启应用，然后浏览器中输入：http://localhost:5000/foo/find，您在日志中将会看到：
````
2020-11-13 15:02:27,562 - foo_service.py line+18 - INFO - do my business!
2020-11-13 15:02:27,563 - foo_controller.py line+21 - INFO - my business done
````
再次恭喜你，成功完成了初试牛刀！


## 4 开发指南  
### 4.1 构建一个WEB应用
#### 4.1.1. HEE WEB应用(HeeWebApplication)  
1. 创建启动程序
````python
from hee import HeeWebApplication

class Application(HeeWebApplication):
    # your code
    pass

if __name__ == '__main__':
    app = Application()
    app.start()
````
写完之后，python3 application.py 即可启动该项目。
启动之后会自动生成配置目录：config/app.conf，config/log4p.json。  


#### 4.2 构建一个Restful应用  
#### 4.2.1. Hee Restful应用(HeeRestApplication)  
TODO


#### 4.3 构建一个调用应用  
TODO

#### 4.4 构建一个自定义的普通应用
TODO

#### 5 常见问题  
本章节主要介绍介绍开发过程中极其常见的问题以及对应的解决方案，方便研发迅速定位问题并解决问题。
  
5.1 经过核对，SQL的命名参数是足够的，却报参数不够的异常  
错误信息如下
````
final_sql = sql % params  
TypeError: not enough arguments for format string
````
解决：
大概率是因为sql占位参数的小括号写成大括号了，例如%{name}，应该写为%(name)，一眼过去差不多，不容易发现。

5.1 查询报错 
TypeError: can't multiply sequence by non-int of type 'str'











