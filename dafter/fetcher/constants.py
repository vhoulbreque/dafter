#!/usr/bin/python
# coding=utf-8

import os

HOME = os.path.expanduser("~")
CURRENT_FOLDER = "/".join(__file__.split("/")[:-1])

DATASETS_CONFIG_FOLDER = os.path.join(CURRENT_FOLDER, "..", "datasets-configs")
DATASETS_FOLDER = os.path.join(HOME, ".dafter")
VERSION_FILE = os.path.join(CURRENT_FOLDER, "..", "VERSION.txt")

__all__ = ["DATASETS_CONFIG_FOLDER", "DATASETS_FOLDER", "VERSION_FILE"]
