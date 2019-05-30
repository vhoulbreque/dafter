#!/usr/bin/python
# coding=utf-8

import os

HOME = os.path.expanduser("~")
CURRENT_FOLDER = os.sep.join(__file__.split(os.sep)[:-1])

DATASETS_CONFIG_FOLDER = os.path.join(CURRENT_FOLDER, "..", "datasets-configs")
DATASETS_FOLDER = os.path.join(HOME, ".dafter")

__all__ = ["DATASETS_CONFIG_FOLDER", "DATASETS_FOLDER"]
