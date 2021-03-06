import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()

requires = [
    'pyramid',
    'pyramid_chameleon',
    'pyramid_debugtoolbar',
    'pyramid_tm',
    'pyramid_mako',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
    'waitress',
    'formencode',
    'python-magic',
    'requests',
    ]

setup(name='ParticleDB',
      version='0.0',
      description='ParticleDB',
      long_description=README,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='particledb',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = particledb:main
      [console_scripts]
      initialize_ParticleDB_db = particledb.scripts.initializedb:main
      clean_ParticleDB_db = particledb.scripts.cleandb:main
      """,
      )
