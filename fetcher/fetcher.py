from .utils import is_dataset_in_db
from .dataset import CSVDataset, ZIPDataset


def get_dataset(dataset_config):

    name = dataset_config["name"]
    urls = dataset_config["urls"]
    type = dataset_config["type"]

    DATA_FOLDER = "data"
    if is_dataset_in_db(name):
        print("The dataset was already existing in database")

    if type == "csv":
        dataset = CSVDataset(name, urls, save_path=DATA_FOLDER)
    elif type == "zip":
        dataset = ZIPDataset(name, urls, save_path=DATA_FOLDER)
    dataset.download()
