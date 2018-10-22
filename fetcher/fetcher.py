import os
import shutil

from .dataset import CSVDataset, ZIPDataset
from .utils import is_dataset_in_db, get_datasets_with_tag, normalize_name


DATASETS_FOLDER = os.path.join(os.path.expanduser("~"),
                                ".datasets-data-fetcher")

def get_dataset(dataset_config):

    name = dataset_config["name"]
    urls = dataset_config["urls"]
    type = dataset_config["type"]

    if is_dataset_in_db(name):
        print("The dataset was already existing in database")
        return

    if type == "csv":
        dataset = CSVDataset(name, urls, save_path=DATASETS_FOLDER)
    elif type == "zip":
        dataset = ZIPDataset(name, urls, save_path=DATASETS_FOLDER)
    dataset.download()


def delete_dataset(dataset_config):

    name = dataset_config["name"]

    if not is_dataset_in_db(name):
        print("The dataset is not in database")
        return

    name = normalize_name(name)
    name = os.path.join(DATASETS_FOLDER, name)
    try:
        print("Deleting {}...".format(name))
        shutil.rmtree(name)
    except Exception as e:
        print("An exception occurred while deleting {}: {}".format(name, e))


def list_datasets(tag):
    dataset_names = get_datasets_with_tag(tag)

    for dn in dataset_names:
        print(dn)


def info_dataset(dataset_config):
    name = dataset_config["name"]
    urls = dataset_config["urls"]
    type = dataset_config["type"]
    desc = dataset_config["description"]

    s = "name: {}\nurls: {}\ntype: {}\ndescription: {}\n".format(name, urls,
                                                                 type, desc)
    print(s)
