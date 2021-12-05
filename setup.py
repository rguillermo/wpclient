#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'requests>=2.26.0',
    'pydantic>=1.8.2',
    'aiohttp>=3.8.1',
    'cchardet>=2.1.7'
]

test_requirements = ['pytest>=6.2.5', ]

setup(
    author="Guillermo Reyes",
    author_email='jguillermo.dev@gmail.com',
    python_requires='>=3.9',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
    ],
    description="WordPress REST API client with async support",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='wpclient, async, aiohttp, requests, wordpress, api',
    name='wpclient',
    packages=find_packages(include=['wpclient', 'wpclient.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/rguillermo/wpclient',
    version='0.3.0',
    zip_safe=False,
)
