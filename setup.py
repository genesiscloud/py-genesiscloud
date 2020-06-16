#!/usr/bin/env python

# MIT License
#
# Copyright (c) 2020 Genesis Cloud Ltd. <opensource@genesiscloud.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Authors:
#   Oz Tiram <otiram@genesiscloud.com>

import os
import sys

from setuptools import find_packages, setup

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))  # noqa


from genesiscloud import __version__

project = "py-genesiscloud"

setup(
    name=project,
    version=__version__,
    description="A library to interact with genesiscloud",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="GenesisCloud",
    author_email="opensource@genesiscloud.com",
    url="https://github.com/genesiscloud/py-genesiscloud",
    packages=find_packages(where='src'),
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Environment :: GPU",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License"
    ],
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "requests",
        "munch"
    ],
    dependency_links=[
    ],
    entry_points={
    },
    extras_require={
        "test": [
            "pytest",
            "responses"
        ],
        "dev": [
            "flake8"
            ]
    },
)
