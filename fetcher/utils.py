import os
import json


DATASETS_CONFIG_FOLDER = os.path.join("/".join(__file__.split("/")[:-1]),
                                        "..", "datasets-configs")
DATASETS_FOLDER = os.path.join(os.path.expanduser("~"),
                                ".datasets-data-fetcher")


def normalize_filename(filename):
    f_name = filename.split('/')[-1]
    f_name = f_name.split('?')[0]
    return f_name


def normalize_name(s):
    if s is None:
        return ''

    s = s.replace('.json', '')

    new_s = ''
    for c in s:
        if c in '- \t\n':
            new_s += '_'
        else:
            new_s += c
    return new_s


def get_config_dataset(datasetname):

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

    datasetname = normalize_name(datasetname)

    folders = os.listdir(DATASETS_FOLDER)
    if datasetname in folders:
        dataset_folder = os.path.join(DATASETS_FOLDER, datasetname)
        files = os.listdir(dataset_folder)
        print(files)
        if files:
            return True
    return False
