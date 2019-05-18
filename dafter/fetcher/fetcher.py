#!/usr/bin/python
# coding=utf-8

import os
import json
import shutil

from .constants import DATASETS_FOLDER, DATASETS_CONFIG_FOLDER
from .dataset import Dataset
from .utils import is_dataset_in_db, normalize_name, is_dataset_being_downloaded, \
    check_internet_connection, get_config_dataset


def get_dataset(datasetname):
    """Downloads the files of the dataset from the urls and saves them on the
    disk.

    Args:
        dataset_config (dict): The config of the dataset to download, as stored
            in the json file of the dataset located in
            "dafter/datasets-configs"

    Returns:
        None
    """
    if not isinstance(datasetname, str):
        raise ValueError("datasetname must of type str, not {}".format(type(datasetname)))

    dataset_config = get_config_dataset(datasetname)
    if dataset_config is None:
        print("{} is not a valid dataset name, dataset url or "
              "json file".format(datasetname))
        return None

    name = dataset_config["name"]
    urls = dataset_config["urls"]

    if not check_internet_connection():
        print("Check your internet connection. Cannot download {}".format(name))
        return None

    if is_dataset_in_db(name) and not is_dataset_being_downloaded(name):
        print("The dataset has already been fetched")
        return None

    dataset = Dataset(name, urls, save_path=DATASETS_FOLDER)
    try:
        print("Downloading {}...".format(dataset.name))
        dataset.download()
    except KeyboardInterrupt as e:
        print("\nThe download has been interrupted. "
              "Run \"dafter get {}\" to resume download".format(name))
    except Exception as e:
        print("Failed downloading {}".format(name))
        print("The following exception occurred : ", e)
    else:
        print("The dataset has been stored in {}".format(dataset.save_folder))
        return dataset

    return None


def delete_dataset(datasetname):
    """Deletes the files of the dataset located on the disk.
    Args:
        dataset_config (dict): The config of the dataset to delete, as stored
            in the json file of the dataset located in
            "dafter/datasets-configs"

    Returns:
        None
    """
    if not isinstance(datasetname, str):
        raise ValueError("datasetname must of type str, not {}".format(type(datasetname)))

    dataset_config = get_config_dataset(datasetname)
    if dataset_config is None:
        print("Not a valid datasetname")
        return None

    name = dataset_config["name"]

    if not is_dataset_in_db(name):
        print("The dataset is not in database")
        return None

    name = normalize_name(name)
    name = os.path.join(DATASETS_FOLDER, name)
    try:
        print("Deleting {}...".format(name))
        shutil.rmtree(name)
        print("The dataset has been deleted!")
        return dataset_config
    except Exception as e:
        print("An exception occurred while deleting {}: {}".format(name, e))

    return None


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

    if not(dataset_name is None or isinstance(dataset_name, str)):
        raise ValueError("dataset_name must be a str, not {}".format(type(dataset_name)))
    
    if not(tags is None or isinstance(tags, list)):
        raise ValueError("tags must be a list of str, not {}".format(type(tags)))
    elif tags and not all([isinstance(t, str) for t in tags]):
        raise ValueError("the tags must be str, not {}".format(tags))

    if tags:
        tags = list(set(tags))
        tags = [t.strip() for t in tags]

    if dataset_name:
        dataset_name = dataset_name.strip()

    configs = []
    printed_list = []
    for config in get_all_datasets():
        config_tags = config["tags"]
        dn = config["name"]

        if not valid_dataset(dataset_name, dn, tags, config):
            continue

        status = get_status_icon(dn)
        printed_list.append("{} {}".format(status, dn))

        configs.append(config)

    if printed_list:
        printed_list = sorted(printed_list)
        print("\n".join(printed_list))
    
    return configs


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


def info_dataset(datasetname):
    """Lists all the relevant information about a dataset. Prints these
    informations.

    Args:
        dataset_config (dict): The config of the dataset to describe, as stored
            in the json file of the dataset located in
            "dafter/datasets-configs"

    Returns:
        dataset_info (dict): The info of the dataset to describe.
    """

    def fit_description(s):

        if not s:
            return ""

        LINE_SIZE = 80  # in chars

        lines = s.split("\n")
        final_lines = []
        for line in lines:
            if not line:
                continue
            line_s = line.split()
            current_s = ""
            for word in line_s:
                if len(word) + len(current_s) + 1 <= LINE_SIZE:
                    if current_s == "":
                        current_s += word
                    else:
                        current_s += " " + word
                else:
                    final_lines.append(current_s)
                    current_s = "" + word    
            if current_s:
                final_lines.append(current_s)
                current_s = ""
            final_lines[-1] = final_lines[-1] + "\n"

        return "\n                ".join(final_lines)

    dataset_config = get_config_dataset(datasetname)
    if dataset_config is None:
        print("Not a valid datasetname")

    name = dataset_config["name"]
    urls = dataset_config["urls"]
    type = dataset_config["type"]
    desc = dataset_config["description"]
    tags = dataset_config["tags"]

    desc = fit_description(desc)

    in_db = is_dataset_in_db(name)
    is_being_downloaded = is_dataset_being_downloaded(name)

    if in_db and not is_being_downloaded:
        status = "[IN DATABASE]"
    elif in_db and is_being_downloaded:
        status = "[BEING DOWNLOADED]"
    else:
        status = "[NOT IN DATABASE - NOT BEING DOWNLOADED]"

    status_str = '{:<15} {:<12}'.format("status:", status)
    name_str = '{:<15} {:<12}'.format("name:", name)
    type_str = '{:<15} {:<12}'.format("type:", type)
    desc_str = '{:<15} {:<12}'.format("description:", desc)
    tags_str = '{:<15} {:<12}'.format("tags:", ", ".join(tags))

    print("\n".join([name_str, type_str, desc_str, tags_str, status_str]))

    dataset_info = {
        "name": name,
        "urls": urls,
        "type": type,
        "description": desc,
        "tags": tags
    }

    return dataset_info