#!/usr/bin/python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='dafter',
    version='0.2',
    description='dafter CLI',
    long_description=
    ('Dafter is a command line downloader of public datasets. It takes care of '
    'downloading and formatting the datasets files so that you can spend '
    'hours building models instead of looking for datasets and their urls.'),
    author='Vincent Houlbreque',
    url='https://github.com/vinzeebreak/dafter',
    keywords=['dataset', 'datasets', 'cli'],
    entry_points={'console_scripts': ['dafter = dafter.cli:main']},
    install_requires=[
        'requests',
        'tqdm'
    ],
    packages=find_packages(),
    include_package_data=True,
    license='Apache 2.0')
