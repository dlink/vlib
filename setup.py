# -*- coding: utf-8 -*-

from setuptools import setup
import string


with open('README.md') as f:
    readme = f.read()

setup(
    description='vlib core libraries',
    long_description=readme,
    author='David Link',
    author_email='dlink@fwk.com',
    url='https://github.com/dlink/vlib',
    packages=['vlib'],
    name='vlib',
    version='0.1',
    scripts=[],
    install_requires=map(string.strip, open('requirements.txt').readlines()),
)
