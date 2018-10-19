import os

from .utils import is_dataset_in_db
from .dataset import CSVDataset, ZIPDataset


def get_dataset(dataset_config):

    name = dataset_config["name"]
    urls = dataset_config["urls"]
    type = dataset_config["type"]

    DATASETS_FOLDER = os.path.join(os.path.expanduser("~"),
                                    ".datasets-data-fetcher")
    if is_dataset_in_db(name):
        print("The dataset was already existing in database")
        return

    if type == "csv":
        dataset = CSVDataset(name, urls, save_path=DATASETS_FOLDER)
    elif type == "zip":
        dataset = ZIPDataset(name, urls, save_path=DATASETS_FOLDER)
    dataset.download()
