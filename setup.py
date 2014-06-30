#!/usr/bin/env python

from distutils.core import setup
from fancytree import VERSION
import os

setup(name='django-fancytree',
      version=VERSION,
      description='Django forms widget that uses Fancytree to display tree data',
      author='Riccardo Magliocchetti',
      author_email='riccardo.magliocchetti@gmail.com',
      url='https://github.com/xrmx/django-fancytree',
      packages=['fancytree',],
      keywords=['django', 'fancytree', 'mptt', 'tree'],
      classifiers=[
          'Development Status :: 1 - Planning',
          'Programming Language :: Python',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Framework :: Django',
      ],
      long_description=open(
          os.path.join(os.path.dirname(__file__), 'README.rst'),
      ).read().strip(),
)
