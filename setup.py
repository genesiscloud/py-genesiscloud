#!/usr/bin/env python
from setuptools import find_packages, setup

project = "pygc"
version = "0.1.0"

setup(
    name=project,
    version=version,
    description="A library to interact with genesiscloud",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Oz Tiram",
    author_email="oz.tiram@gmail.com",
    url="https://github.com/oz123/pygc",
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
