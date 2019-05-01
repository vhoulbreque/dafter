#!/usr/bin/python
# coding=utf-8

from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop

import os
from os.path import expanduser


def create_config_dirs():
    HOME = expanduser("~")

    DATABASE_DIR = os.path.join(HOME, ".dafter")
    if not os.path.exists(DATABASE_DIR):
        os.makedirs(DATABASE_DIR)


class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        create_config_dirs()
        develop.run(self)

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        create_config_dirs()
        install.run(self)


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
    keywords=['dataset', 'datasets', 'cli', 'downloader'],
    entry_points={'console_scripts': ['dafter = dafter.cli:main']},
    install_requires=[
        'requests',
        'tqdm'
    ],
    packages=find_packages(),
    include_package_data=True,
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    },
    license='MIT')
