#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
    name="Bicycle sharing analysis",
    version="1.0",
    install_requires=[
        "apache-beam[gcp]==2.47.0",
        "geopy==2.3.0"
    ],
    packages=find_packages(exclude=["notebooks"]),
    py_modules=["config"],
    include_package_data=True,
    description="Analyze bicycle sharing data",
)
