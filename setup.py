#!/usr/bin/env python
import os
import sys

from setuptools import find_packages, setup

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))  # noqa


from genesiscloud import __version__

project = "genesiscloud"

setup(
    name=project,
    version=__version__,
    description="A library to interact with genesiscloud",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Oz Tiram",
    author_email="oz.tiram@gmail.com",
    url="https://github.com/genesiscloud/py-genesiscloud",
    packages=find_packages(where='src'),
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "requests"
    ],
    dependency_links=[
    ],
    entry_points={
    },
    extras_require={
        "test": [
            "pytest"
            "responses"
        ],
        "dev": [
            "flake8"
            ]
    },
)
