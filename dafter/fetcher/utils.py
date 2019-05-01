#!/usr/bin/python
# coding=utf-8

import os
import json
import requests

from .constants import DATASETS_FOLDER, DATASETS_CONFIG_FOLDER, VERSION_FILE


def is_dataset_being_downloaded(datasetname):
    """Tells if the dataset is currently being downloaded.

    TODO: also check if the number of downloaded files is the same at what is
    expected in the config.

    Args:
        datasetname (str): The name of the dataset.

    Returns:
        bool (bool): True if the dataset is being downloaded, False otherwise.
    """

    datasetname = normalize_filename(datasetname)

    folders = os.listdir(DATASETS_FOLDER)
    for folder in folders:
        if folder == datasetname:
            files = os.listdir(os.path.join(DATASETS_FOLDER, folder))

            # First, test if an incomplete file is present
            for filename in files:
                if "incomplete" in filename:
                    return True

            # Second, test if all the files have been downloaded
            config = get_config_dataset(datasetname)
            if len(config["urls"]) != len(files):
                return True

            break

    return False


def normalize_filename(filename):
    """Normalizes the name of a file. Used to avoid characters errors and/or to
    get the name of the dataset from a url.

    Args:
        filename (str): The name of the file.

    Returns:
        f_name (str): The normalized filename.
    """
    f_name = filename.split('/')[-1]
    f_name = f_name.split('?')[0]
    return f_name


def normalize_name(s):
    """Normalizes the name of a file. Used to avoid characters errors and/or to
    get the name of the dataset from a config filename.

    Args:
        s (str): The name of the file.

    Returns:
        new_s (str): The normalized name.
    """
    if s is None:
        return ''

    s = s.replace('.json', '')

    new_s = ''
    for c in s:
        if c in ' \t\n':
            new_s += '_'
        else:
            new_s += c
    return new_s


def get_config_dataset(datasetname):
    """Gets the config of a dataset from its config file located in
    "dafter/datasets-configs"

    Args:
        datasetname (str): The name of the dataset.

    Returns:
        config (dict): The configuration info about the dataset.
    """

    for config_file in os.listdir(DATASETS_CONFIG_FOLDER):
        cf = config_file.replace(".json", "")
        if cf != datasetname:
            continue

        config = None
        config_file = os.path.join(DATASETS_CONFIG_FOLDER, config_file)
        with open(config_file) as f:
            config = json.load(f)
        return config

    return None


def is_dataset_in_db(datasetname):
    """Tells if the dataset is located on the disk.

    Args:
        datasetname (str): The name of the dataset.

    Returns:
        bool (bool): True if the dataset is located on the disk, False
            otherwise.
    """
    datasetname = normalize_name(datasetname)

    folders = os.listdir(DATASETS_FOLDER)
    if datasetname in folders:
        dataset_folder = os.path.join(DATASETS_FOLDER, datasetname)
        files = os.listdir(dataset_folder)
        if files:
            return True
    return False


def check_internet_connection():
    """Checks if there is a working internet connection."""
    url = 'http://www.google.com/'
    timeout = 5
    try:
        _ = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError as e:
        return False
    return False


def get_version():
    with open(VERSION_FILE) as f:
        version = [l.strip() for l in f][0]
        return version
