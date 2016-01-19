# -*- coding: utf-8 -*-

from setuptools import setup
import string


with open('README.md') as f:
    readme = f.read()

setup(
    description='vlib core libraries',
    long_description=readme,
    author='David Link',
    author_email='dvlink@gmail.com',
    url='https://github.com/dlink/vlib',
    packages=['vlib'],
    name='vlib',
    version='1.2.2',
    scripts=[],
    license='GNU General Public License (GPL)',
    install_requires=map(string.strip, open('requirements.txt').readlines()),
)
