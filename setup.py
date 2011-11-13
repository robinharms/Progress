import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()

requires = (
    'pyramid',
    'repoze.zodbconn',
    'repoze.tm2>=1.0b1', # default_commit_veto
    'repoze.retry',
    'ZODB3',
    'WebError',
    'slugify',
    'repoze.folder',
    'pytz',
    'colander',
    'deform',
    'betahaus.pyracont',
    'fanstatic',
    )

setup(name='Progress',
      version='0.0',
      description='Progress',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='Robin Harms Oredsson / Betahaus',
      author_email='robin@betahaus.net',
      url='',
      keywords='web pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires = requires,
      tests_require= requires,
      test_suite="progress",
      entry_points = """\
      [paste.app_factory]
      main = progress:main
      [fanstatic.libraries]
      progress_csslib = progress.fanstaticlib:progress_csslib
      progress_jslib = progress.fanstaticlib:progress_jslib
      """,
      paster_plugins=['pyramid'],
      )

