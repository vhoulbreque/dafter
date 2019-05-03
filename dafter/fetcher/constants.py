#!/usr/bin/python
# coding=utf-8

import os

HOME = os.path.expanduser("~")
CURRENT_FOLDER = "/".join(__file__.split("/")[:-1])

#DATASETS_CONFIG_FOLDER = os.path.join(CURRENT_FOLDER, "..", "datasets-configs")

# see https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html

if 'XDG_DATA_HOME' in os.environ:
    DATASETS_FOLDER = os.path.join(os.environ['XDG_DATA_HOME'], "dafter")
    DATASETS_CONFIG_FOLDER = os.path.join(os.environ['XDG_DATA_HOME'], "dafter", "datasets-configs")
else:
    DATASETS_FOLDER = os.path.join(HOME, ".local", "share", "dafter")
    DATASETS_CONFIG_FOLDER = os.path.join(DATASETS_FOLDER, "datasets-configs")

VERSION_FILE = os.path.join(CURRENT_FOLDER, "..", "VERSION.txt")

__all__ = ["DATASETS_CONFIG_FOLDER", "DATASETS_FOLDER", "VERSION_FILE"]
