# -*- coding: utf-8 -*-

from setuptools import setup
import string


with open('README.md') as f:
    readme = f.read()

setup(
    name='vlib',
    packages=['vlib'],
    version='1.3.2',
    description='vlib core libraries',
    long_description=readme,
    url='https://github.com/dlink/vlib',
    author='David Link',
    author_email='dvlink@gmail.com',
    license='GNU General Public License (GPL)',
    # See https://PyPI.python.org/PyPI?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python :: 2.7',
        'Topic :: Database',
        'Topic :: Software Development :: Libraries',
    ],
    keywords = ['database', 'logging', 'config', 'orm', 'odict'],
    
    #scripts=[],
    #install_requires=map(string.strip, open('requirements.txt').readlines()),
)
