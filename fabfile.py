from fabric.api import *


def pack():
    local('python setup.py sdist --formats=gztar', capture=False)