# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.md') as f:
    readme = f.read()

setup(
    description='vlib core libraries',
    long_description=readme,
    author='David Link',
    author_email='dlink@fwk.com',
    url='https://github.com/dlink/vlib',
    packages=['vlib'],
)
