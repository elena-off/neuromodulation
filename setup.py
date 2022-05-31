#!/usr/bin/env python
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='neuromodulation',
    version='0.0.0',
    description='Toy Repo for Master Thesis Elena',
    author='Elena Offenberg',
    author_email='e.offenberg@stud.uni-goettingen.de',
    packages=find_packages(exclude=[]),
    install_requires=[],
)