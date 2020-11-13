import os

try:
    import flask
except:
    print('Can not find flask, start installing...')
    os.system('pip install flask')

try:
    import log4p
except:
    print('Can not find log4p, start installing...')
    os.system('pip install log4p')

from hee.heeframework import HeeRestApplication
from hee.heeframework import HeeApplication
from hee.heeframework import HeeSchedApplication
from hee.heeframework import HeeMapping
from hee.heeframework import component

