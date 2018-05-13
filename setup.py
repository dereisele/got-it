from distutils.core import setup
setup(
  name = 'got-it',
  packages = ['gotit', 'gotit.extractor_blueprint'],
  scripts = ['bin/got-it'],
  version = '0.1',
  description = 'Index content on catch-up TV services',
  author = 'Alexander Eisele',
  author_email = 'git@eiselecloud.de',
  url = 'https://github.com/derEisele/got-it',
  download_url = 'https://github.com/derEisele/got-it/archive/0.1.tar.gz',
  keywords = [''],
  install_requires=[
    'requests>=1.0',
    'mysql-connector',
    'SQLAlchemy',
    'pluginbase',
  ],
  classifiers = [],
)
