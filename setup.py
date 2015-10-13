#!/usr/bin/env python

from setuptools import setup

setup(
    name="rockProcessor",
    version="0.1",
    description="Utility to Convert JSON produced by SparkRocks to a VTK File",
    author="Michael Gardner",
    url="https://github.com/shellshocked2003/rockProcessor",
    packages=['rockProcessor'],
    package_dir={'rockProcessor': 'src'},
    install_requires=['pyevtk'],
)
