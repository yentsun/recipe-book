from fabric.api import *

APP_NAME = 'kook'
env.hosts = ['ubuntu@ec2-alpha']
env.key_filename = ['/home/yentsun/.ssh/yentsunkey.pem']


def pack():
    local('~/env/bin/python setup.py sdist --formats=gztar', capture=False)


def deploy():
    dist = local('~/env/bin/python setup.py --fullname', capture=True).strip()
    put('dist/{dist}.tar.gz'.format(dist=dist),
        '{dist}.tar.gz'.format(dist=dist))
    run('tar xzf {dist}.tar.gz'.format(dist=dist))
    run('rm -f {dist}.tar.gz'.format(dist=dist))
    with cd('{dist}'.format(dist=dist)):
        run('~/env/bin/python setup.py install')
    with cd('{dist}/kook/tests'.format(dist=dist)):
        run('~/env/bin/nosetests views.py')
        run('~/env/bin/nosetests templates.py')
    with cd(APP_NAME):
        run('supervisorctl shutdown')
    run('rm -rf {appname}'.format(appname=APP_NAME))
    run('mv {dist} {appname}'.format(appname=APP_NAME, dist=dist))
    with cd(APP_NAME):
        run('supervisord')
        run('supervisorctl status')