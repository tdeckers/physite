from setuptools import setup
from setuptools.command.test import test as TestCommand
import os
import sys

import physite

here= os.path.abspath(os.path.dirname(__file__))
class PyTest(TestCommand):
        def finalize_options(self):
            TestCommand.finalize_options(self)
            self.test_args = []
            self.test_suite = True

        def run_tests(self):
            import pytest
            errcode = pytest.main(self.test_args)
            sys.exit(errcode)

setup(
        name='physite',
        version=physite.__version__,
        url='',
        license='',
        author='Tom Deckers',
        author_email='tom@ducbase.com',
        description='Physical display of site information (traffic, ...)',
        packages=['physite'],
        platforms='any',
        install_requires=[
            'google-api-python-client>=1.3.1'
            ],
        tests_require=['pytest'],
        cmdclass={'test': PyTest},
        extras_require={
            'testing': ['pytest']}
        )
