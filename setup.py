try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import sys, re

reqs = ['requests>=2.5']

tests_requires = ['nose', 'responses', 'mock']

version = ''
with open('quickpay_api_client/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(),
                        re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

setup(
    name='quickpay-api-client',
    version=version,
    description='Python client for QuickPay API',
    author_email="support@quickpay.net",
    author="QuickPay Developers",
    url="https://github.com/QuickPay/quickpay-python-client",
    packages=['quickpay_api_client'],
    license='MIT',
    install_requires=reqs,
    tests_requires=tests_requires,
    test_suite='nose.collector')
