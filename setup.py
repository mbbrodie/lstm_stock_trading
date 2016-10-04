#!/usr/bin/env python

from setuptools import setup
from setuptools.command.test import test as TestCommand
import sys


class PyTest(TestCommand):

    def initialize_options(self):
        TestCommand.initialize_options(self)

    def finalize_options(self):
        TestCommand.finalize_options(self)

        self.test_args = ['app', '--cov', 'app', '--cov-report',
                          'term-missing']
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)

setup(
    name='pytdf-sample-agent',
    version='0.0.1',
    packages=['sample_agent'],
    include_package_data=True,
    install_requires=[
        'pandas',
    ],
    tests_require=[
        'pytest',
        'pytest-cov',
        'configparser'
    ],
    cmdclass={
        'test': PyTest,
    },
)
