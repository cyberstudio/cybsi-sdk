from setuptools import setup, find_packages

from cybsi_sdk.__version__ import (
      __title__,
      __author_email__,
      __license__,
      __version__,
      __description__,
      __author__,
)

setup(
      name=__title__,
      author=__author__,
      author_email=__author_email__,
      license=__license__,
      version=__version__,
      description=__description__,
      packages=find_packages(),
      install_requires=[
            'requests~=2.26',
      ],
      python_requires='~=3.7',
)
