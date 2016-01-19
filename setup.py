#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from setuptools import setup
from setuptools import find_packages

from docs import getVersion


# Variables ===================================================================
changelog = open('CHANGELOG.rst').read()
long_description = "\n\n".join([
    open('README.rst').read(),
    changelog
])


# Actual setup definition =====================================================
setup(
    name='',
    version=getVersion(changelog),
    description="Naïve bayesian text classifier for any dict-like backend.",
    long_description=long_description,
    url='https://github.com/Bystroushaak/redisbayes',

    author='Bystroushaak',
    author_email='bystrousak@kitakitsune.org',

    classifiers=[
        "Development Status :: 4 - Beta",
        'Intended Audience :: Developers',

        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",

        "License :: OSI Approved :: MIT License",

        "Topic :: Communications",
    ],
    license='MIT',

    packages=find_packages('src'),
    package_dir={'': 'src'},

    zip_safe=False,
    include_package_data=True,

    test_suite='py.test',
    tests_require=["pytest"],
    extras_require={
        "test": [
            "pytest",
        ],
        "docs": [
            "sphinx",
            "sphinxcontrib-napoleon",
        ]
    },
)
