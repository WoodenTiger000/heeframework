import os


import shutil
import sys

# check and install flask
try:
    import flask
except:
    print('Can not find flask, start installing...')
    os.system('pip install flask')

# check and install log4p
try:
    import log4p
except:
    print('Can not find log4p, start installing...')
    os.system('pip install log4p')

# check and install configparser
try:
    import configparser
except:
    print('Can not find configparser, start installing configparser...')
    os.system('pip install configparser')

# load configfile
config = configparser.ConfigParser()
config.read('config/app.conf', encoding='UTF-8')

# check and create config dir
if not os.path.exists("config/"):
    os.mkdir("config/")

if not os.path.exists("modules/"):
    os.mkdir("modules/")

if not os.path.exists("modules/service/"):
    os.mkdir("modules/service/")

if not os.path.exists("modules/dao/"):
    os.mkdir("modules/dao/")

if not os.path.exists("modules/controller"):
    os.mkdir("modules/controller")

if not os.path.exists("static/"):
    os.mkdir("static/")

# check and create log dir
if not os.path.exists("../logs"):
    os.mkdir("../logs")

# copy log4p.json to config dir if not exists
if not os.path.exists("config/log4p.json"):
    pkgdir = sys.modules['hee'].__path__[0]
    fullpath = os.path.join(pkgdir, 'log4p_template.json')
    shutil.copy(fullpath, 'config/log4p.json')

# copy app.conf to config dir if not exists
if not os.path.exists("config/app.conf"):
    pkgdir = sys.modules['hee'].__path__[0]
    fullpath = os.path.join(pkgdir, 'app_template.conf')
    shutil.copy(fullpath, 'config/app.conf')

# dynamic module
if config.has_section('mybatis'):
    print("mybatis 有的")


from hee.heeframework import HeeRestApplication
from hee.heeframework import HeeApplication
from hee.heeframework import HeeSchedApplication
from hee.heeframework import HeeMapping
from hee.heeframework import component

print("execute heeframework __init__.py")