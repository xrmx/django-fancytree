#!/usr/bin/env python

from distutils.core import setup
import fancytree
import os

setup(name='django-fancytree',
      version=fancytree.__version__,
      description='Django forms widget that uses Fancytree to display tree data',
      author='Riccardo Magliocchetti',
      author_email='riccardo.magliocchetti@gmail.com',
      url='https://github.com/xrmx/django-fancytree',
      packages=['fancytree',],
      keywords=['django', 'fancytree', 'mptt', 'tree'],
      classifiers=[
          'Programming Language :: Python',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Environment :: Web Environment',
          'Framework :: Django',
          'Topic :: Software Development :: Libraries :: Application Frameworks',
      ],
      long_description=open(
          os.path.join(os.path.dirname(__file__), 'README.rst'),
      ).read().strip(),
      include_package_data=True,
      install_required=[
          'Django',
      ]
)
