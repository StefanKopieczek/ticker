from setuptools import setup

setup(name='ticker',
      version='0.12',
      description='Yahoo finance wrapper for stock information',
      url='http://github.com/stefankopieczek/ticker',
      author='Stefan Kopieczek',
      author_email="stefankopieczek+ticker@gmail.com",
      license='LGPL 2.0',
      packages=['ticker'],
      install_requires=[
          'bs4',
          'requests',
      ],
      zip_safe=False)
