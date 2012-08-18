import os
import sys

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid',
    'SQLAlchemy',
    'transaction',
    'colander',
    'pyramid_tm',
    'pyramid_beaker',
    'beaker',
    'pyramid_debugtoolbar',
    'zope.sqlalchemy',
    'cryptacular',
    'markdown',
    'webtest',
    'Babel'
    ]

if sys.version_info[:3] < (2,5,0):
    requires.append('pysqlite')

setup(name='kook',
      version='0.6.7-krew',
      description='a robust recipe inventory storing and sharing',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='Max Korinets',
      author_email='mkorinets@gmail.com',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='kook',
      install_requires = requires,
      entry_points = """\
      [paste.app_factory]
      main = kook:main
      [console_scripts]
      populate_kook = kook.scripts.populate:main
      """,
      )

