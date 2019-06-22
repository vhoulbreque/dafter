#!/usr/bin/python
# coding=utf-8

import os
import re
import json
import requests

from .constants import DATASETS_FOLDER, DATASETS_CONFIG_FOLDER


def is_valid_url(s):

    if not isinstance(s, str):
        return False

    regex = re.compile(
                    r'^(?:http|ftp)s?://' # http:// or https://
                    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
                    r'localhost|' #localhost...
                    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
                    r'(?::\d+)?' # optional port
                    r'(?:/?|[/?]\S+)$', re.IGNORECASE
                    )
    return re.match(regex, s) is not None


def is_valid_path(s):
    if not isinstance(s, str):
        return False
    return os.path.isfile(s)


def is_valid_config(config):

    if not isinstance(config, dict):
        return False

    fields = ["name", "urls", "type"]
    for field in fields:
        if field not in config:
            return False
        if config[field] is None:
            return False

    urls_ = config["urls"]
    if type(urls_) != list:
        return False
    if len(urls_) == 0:
        return False

    for url_ in urls_:
        if "url" not in url_:
            return False

        url_validity = is_valid_url(url_["url"])
        if not url_validity:
            return False

    return True


def is_dataset_being_downloaded(datasetname):
    """Tells if the dataset is currently being downloaded.

    TODO: also check if the number of downloaded files is the same at what is
    expected in the config.

    Args:
        datasetname (str): The name of the dataset.

    Returns:
        bool (bool): True if the dataset is being downloaded, False otherwise.
    """

    def get_size_file(path):
        size = str(os.path.getsize(path))  # eg. 56282L
        size = "".join(c for c in size if c.isdigit())
        size = int(size)
        return size

    # TODO: normalize name of normalize_filename?
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
            for u_ in config["urls"]:
                file_path = os.path.join(os.path.join(DATASETS_FOLDER, folder, normalize_filename(u_["url"])))
                if not os.path.isfile(file_path):
                    return True

            # Third, if all the files have been downloaded, 
            # test if the bytes size match
            for u_ in config["urls"]:
                if "bytes" in u_:
                    file_path = os.path.join(os.path.join(DATASETS_FOLDER, folder, normalize_filename(u_["url"])))

                    expected_bytes = u_["bytes"]
                    downloaded_bytes = get_size_file(file_path)

                    if expected_bytes != downloaded_bytes:
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

    if not isinstance(filename, str):
        raise ValueError("filename must be a str, not {}".format(type(filename)))

    if filename == "":
        return ""

    first_part = filename.split('?')[0]
    f_parts = [s for s in first_part.split('/') if s != ""]
    f_name = f_parts[-1]

    return f_name


def normalize_name(s):
    """Normalizes the name of a file. Used to avoid characters errors and/or to
    get the name of the dataset from a config filename.

    Args:
        s (str): The name of the file.

    Returns:
        new_s (str): The normalized name.
    """
    if not isinstance(s, str):
        raise ValueError("filename must be a str, not {}".format(type(s)))

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

    if not isinstance(datasetname, str):
        raise ValueError("datasetname must be a str, not {}".format(type(datasetname)))

    config = None
    if is_valid_url(datasetname):
        url = datasetname
        r = requests.get(url=url)
        if r.status_code == 200:
            config = r.json()
            if not is_valid_config(config):
                print("There is a missing parameter in the config file")
                config = None
        else:
            config = None
    elif is_valid_path(datasetname):
        config_file = datasetname
        with open(config_file) as f:
            try:
                config = json.load(f)
                if not is_valid_config(config):
                    print("There is a missing parameter in the config file")
                    config = None
            except:
                config = None
    else:
        for config_file in os.listdir(DATASETS_CONFIG_FOLDER):
            cf = config_file.replace(".json", "")
            if cf != datasetname:
                continue

            config_file = os.path.join(DATASETS_CONFIG_FOLDER, config_file)
            with open(config_file) as f:
                config = json.load(f)

    return config


def is_dataset_in_db(datasetname):
    """Tells if the dataset is located on the disk.

    Args:
        datasetname (str): The name of the dataset.

    Returns:
        bool (bool): True if the dataset is located on the disk, False
            otherwise.
    """

    if not isinstance(datasetname, str):
        raise ValueError("datasetname must be a str, not {}".format(type(datasetname)))

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
