import os
import shutil

from fetcher import DATASETS_FOLDER
from .dataset import Dataset
from .utils import is_dataset_in_db, get_datasets_with_tag, normalize_name, \
    is_dataset_being_downloaded


def get_dataset(dataset_config):
    """Downloads the files of the dataset from the urls and saves them on the
    disk.

    Args:
        dataset_config (dict): The config of the dataset to download, as stored
            in the json file of the dataset located in
            "data-fetcher/datasets-configs"

    Returns:
        None
    """
    name = dataset_config["name"]
    urls = dataset_config["urls"]
    type = dataset_config["type"]

    if is_dataset_in_db(name) and not is_dataset_being_downloaded(name):
        print("The dataset has already been fetched")
        return

    dataset = Dataset(name, urls, extension=type, save_path=DATASETS_FOLDER)
    dataset.download()


def delete_dataset(dataset_config):
    """Deletes the files of the dataset located on the disk.
    Args:
        dataset_config (dict): The config of the dataset to delete, as stored
            in the json file of the dataset located in
            "data-fetcher/datasets-configs"

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


def list_datasets(tag):
    """Lists all the datasets names in the config files that have the tag `tag`.
    Prints all the names of all the datasets that match this criteria.

    Args:
        tag (str): The tag.

    Returns:
        None
    """
    dataset_names = get_datasets_with_tag(tag)

    for dn in dataset_names:
        in_db = is_dataset_in_db(dn)
        is_being_downloaded = is_dataset_being_downloaded(dn)

        if in_db and not is_being_downloaded:
            status = "X"
        elif in_db and is_being_downloaded:
            status = "/"
        else:
            status = " "
        print("{} {}".format(status, dn))


def info_dataset(dataset_config):
    """Lists all the relevant information about a dataset. Prints these
    informations.

    Args:
        dataset_config (dict): The config of the dataset to describe, as stored
            in the json file of the dataset located in
            "data-fetcher/datasets-configs"

    Returns:
        None
    """
    name = dataset_config["name"]
    urls = dataset_config["urls"]
    type = dataset_config["type"]
    desc = dataset_config["description"]

    in_db = is_dataset_in_db(name)
    is_being_downloaded = is_dataset_being_downloaded(name)

    if in_db and not is_being_downloaded:
        status = "[IN DATABASE]"
    elif in_db and is_being_downloaded:
        status = "[BEING DOWNLOADED]"
    else:
        status = "[NOT IN DATABASE - NOT BEING DOWNLOADED]"

    s = """status: {}\nname: {}\nurls: {}\n
type: {}\ndescription: {}\n""".format(status, name, urls, type, desc)
    print(s)
