"""
A Python3 program that adds a Sigel to a given collection of binary MARC records (into MARC field 935 a; and optionally deduplicates this collection to another given collection)
"""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='marcsigel',
      version='0.0.1',
      description='a Python3 program that adds a Sigel to a given collection of binary MARC records (into MARC field 935 a; and optionally deduplicates this collection to another given collection)',
      url='https://github.com/slub/marcsigel',
      author='Bo Ferri',
      author_email='zazi@smiy.org',
      license="Apache 2.0",
      packages=[
          'marcsigel',
      ],
      package_dir={'marcsigel': 'marcsigel'},
      install_requires=[
          'argparse>=1.4.0',
          'pymarc>=3.1.13'
      ],
      entry_points={
          "console_scripts": ["marcsigel=marcsigel.marcsigel:run"]
      }
      )
