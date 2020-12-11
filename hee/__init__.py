import os
import shutil
import sys
import configparser

# check and install flask
try:
    import flask
except:
    print('Can not find flask, start installing...')
    os.system('pip3 install flask==1.1.2')

# check and install log4p
try:
    import log4p
except:
    print('Can not find log4p, start installing...')
    os.system('pip3 install log4p==2019.7.13.3')

try:
    import apscheduler
except:
    print('Can not find apscheduler, start installing apscheduler...')
    os.system('pip3 install apscheduler==3.6.3')

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

# all dynamic module
#
print("Hee starts check dynamic module...")
if config.has_section('MYSQL'):
    print("MYSQL config section exists, load dependencies.")
    try:
        import pymysql
    except:
        os.system('pip3 install pymysql')
    try:
        import dbutils
    except:
        os.system('pip3 install dbutils')
    print("MYSQL dynamic module initialized.")

if config.has_section('HEEJOB'):
    print("HEEJOB config section exists, load dependencies.")
    try:
        import apscheduler
    except:
        os.system('pip3 install apscheduler')

from hee.heeframework import HeeRestApplication
from hee.heeframework import HeeWebApplication
from hee.heeframework import HeeApplication
from hee.heeframework import HeeSchedApplication
from hee.heeframework import HeeMapping
from hee.heeframework import component

print("execute heeframework __init__.py")