#!/usr/bin/python
# coding=utf-8

import os
import json
import shutil

from .constants import DATASETS_FOLDER, DATASETS_CONFIG_FOLDER
from .dataset import Dataset
from .utils import is_dataset_in_db, normalize_name, is_dataset_being_downloaded, \
    check_internet_connection


def get_dataset(dataset_config):
    """Downloads the files of the dataset from the urls and saves them on the
    disk.

    Args:
        dataset_config (dict): The config of the dataset to download, as stored
            in the json file of the dataset located in
            "dafter/datasets-configs"

    Returns:
        None
    """

    name = dataset_config["name"]
    urls = dataset_config["urls"]
    type = dataset_config["type"]

    if not check_internet_connection():
        print("Check your internet connection. Cannot download {}".format(name))
        return

    if is_dataset_in_db(name) and not is_dataset_being_downloaded(name):
        print("The dataset has already been fetched")
        return

    dataset = Dataset(name, urls, extension=type, save_path=DATASETS_FOLDER)
    try:
        dataset.download()
    except KeyboardInterrupt as e:
        print("\nThe download has been interrupted. "
              "Run \"dafter get {}\" to resume download".format(name))


def delete_dataset(dataset_config):
    """Deletes the files of the dataset located on the disk.
    Args:
        dataset_config (dict): The config of the dataset to delete, as stored
            in the json file of the dataset located in
            "dafter/datasets-configs"

    Returns:
        None
    """
    name = dataset_config["name"]

    if not is_dataset_in_db(name):
        print("The dataset is not in database")
        return

    name = normalize_name(name)
    name = os.path.join(DATASETS_FOLDER, name)
    try:
        print("Deleting {}...".format(name))
        shutil.rmtree(name)
        print("The dataset has been deleted!")
    except Exception as e:
        print("An exception occurred while deleting {}: {}".format(name, e))


def get_all_datasets():
    """Yields all the available datasets configs"""
    for config_file in os.listdir(DATASETS_CONFIG_FOLDER):
        cf = os.path.join(DATASETS_CONFIG_FOLDER, config_file)
        with open(cf) as f:
            config = json.load(f)
        yield config


def search_datasets(dataset_name, tags):
    """Lists all the datasets names in the config files that have the tags
    `tags` and the name `dataset_name`. Prints all the names and the statuses of
    all the datasets that match this criteria.

    Args:
        dataset_name (str): A string which is a substring of the datasets' names
            we will return
        tag (list of str): The tags.

    Returns:
        None
    """
    def valid_dataset(dataset_name, dn, tags, config):
        if dataset_name:
            if dataset_name not in dn:
                return False

        if tags:
            for t in tags:
                if t not in config_tags:
                    return False
        return True

    def get_status_icon(dataset_name):
        # Our dataset has all the tags needed
        in_db = is_dataset_in_db(dn)
        is_being_downloaded = is_dataset_being_downloaded(dn)

        if in_db and not is_being_downloaded:
            status = "X"
        elif in_db and is_being_downloaded:
            status = "/"
        else:
            status = " "
        return status

    if tags:
        tags = list(set(tags))
        tags = [t.strip() for t in tags]

    if dataset_name:
        dataset_name = dataset_name.strip()

    printed_list = []
    for config in get_all_datasets():
        config_tags = config["tags"]
        dn = config["name"]

        if not valid_dataset(dataset_name, dn, tags, config):
            continue

        status = get_status_icon(dn)
        printed_list.append("{} {}".format(status, dn))

    if printed_list:
        printed_list = sorted(printed_list)
        print("\n".join(printed_list))


def list_datasets(dataset_name, tags):
    """Lists all the dataset names of the downloaded datasets.

    Args:
        dataset_name (str): A string which is a substring of the datasets' names
            we will return
        tag (list of str): The tags.

    Returns:
        None
    """
    def valid_dataset(dataset_name, dn, tags, config):
        in_db = is_dataset_in_db(dn)
        if not in_db:
            return False

        if dataset_name:
            if dataset_name not in dn:
                return False

        if tags:
            for t in tags:
                if t not in config_tags:
                    return False
        return True

    def get_status_icon(dataset_name):
        # Our dataset has all the tags needed
        in_db = is_dataset_in_db(dn)
        is_being_downloaded = is_dataset_being_downloaded(dn)

        if in_db and not is_being_downloaded:
            status = "X"
        elif in_db and is_being_downloaded:
            status = "/"
        else:
            status = " "
        return status

    printed_list = []
    for config in get_all_datasets():
        config_tags = config["tags"]
        dn = config["name"]

        if not valid_dataset(dataset_name, dn, tags, config):
            continue

        status = get_status_icon(dn)
        printed_list.append("{} {}".format(status, dn))

    if printed_list:
        printed_list = sorted(printed_list)
        print("\n".join(printed_list))


def info_dataset(dataset_config):
    """Lists all the relevant information about a dataset. Prints these
    informations.

    Args:
        dataset_config (dict): The config of the dataset to describe, as stored
            in the json file of the dataset located in
            "dafter/datasets-configs"

    Returns:
        None
    """
    name = dataset_config["name"]
    urls = dataset_config["urls"]
    type = dataset_config["type"]
    desc = dataset_config["description"]
    tags = dataset_config["tags"]
    loader_url = "https://vinzeebreak.github.io/dafter-loader/docs/datasets/{}/".format(name)

    in_db = is_dataset_in_db(name)
    is_being_downloaded = is_dataset_being_downloaded(name)

    if in_db and not is_being_downloaded:
        status = "[IN DATABASE]"
    elif in_db and is_being_downloaded:
        status = "[BEING DOWNLOADED]"
    else:
        status = "[NOT IN DATABASE - NOT BEING DOWNLOADED]"

    print("status : {}".format(status))
    print("name : {}".format(name))
    print("urls : {}".format("\n".join([u["url"] for u in urls])))
    print("type : {}".format(type))
    print("description : {}".format(desc))
    print("tags : {}".format(" - ".join(tags)))
    print("How to load this dataset: {}".format(loader_url))
