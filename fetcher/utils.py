import os
import json


DATASETS_CONFIG_FOLDER = os.path.join("/".join(__file__.split("/")[:-1]),
                                        "..", "datasets-configs")
DATASETS_FOLDER = os.path.join(os.path.expanduser("~"),
                                ".datasets-data-fetcher")
DOWNLOAD_CONFIG_FILE = os.path.join(os.path.expanduser("~"),
                                    ".datafetcher",
                                    "download-config.txt")


def is_download_over(datasetname):

    with open(DOWNLOAD_CONFIG_FILE, "r") as f:
        lines = [line.rstrip('\n') for line in f if line]

    for line in lines:
        d_name = line.split('\t')[0]
        if d_name == datasetname:
            return False
    return True


def create_chunk_count(datasetname, filename):

    with open(DOWNLOAD_CONFIG_FILE, "r") as f:
        lines = [line.rstrip('\n') for line in f if line]

    for line in lines:
        l = line.split('\t')
        d_name = l[0]
        f_name = l[1]

        if d_name == datasetname and f_name == filename:
            return int(l[2])

    with open(DOWNLOAD_CONFIG_FILE, "a") as f:
        f.write("{}\t{}\t{}\n".format(datasetname, filename, 0))

    return 0


def remove_chunk_count(datasetname, filename):
    with open(DOWNLOAD_CONFIG_FILE, "r") as f:
        lines = [line.rstrip('\n') for line in f if line]

    with open(DOWNLOAD_CONFIG_FILE, "w") as f:
        for line in lines:
            l = line.split('\t')
            d_name = l[0]
            f_name = l[1]
            if d_name == datasetname and f_name == filename:
                continue
            f.write("{}\n".format(line))

def add_chunk_download_config(datasetname, filename):
    with open(DOWNLOAD_CONFIG_FILE, "r") as f:
        lines = [line.rstrip('\n') for line in f if line]

    with open(DOWNLOAD_CONFIG_FILE, "w") as f:
        for line in lines:
            l = line.split('\t')
            d_name = l[0]
            f_name = l[1]
            c = int(l[2])
            if d_name == datasetname and f_name == filename:
                # increase the counter only for the right dataset
                # and the right file
                c += 1
            new_line = "{}\t{}\t{}\n".format(d_name, f_name, c)
            f.write(new_line)


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
    "data-fetcher/datasets-configs"

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
        print(files)
        if files:
            return True
    return False


def get_datasets_with_tag(tag):
    """Retrieves all the datasets in the config database that have the tag.

    Args:
        tag (str): The tag.

    Returns:
        dataset_names (list of str): The list of all the dataset names that
            match the criteria.
    """
    if tag is None:
        return []

    dataset_names = []

    config_files = os.listdir(DATASETS_CONFIG_FOLDER)
    for cf in config_files:
        cf = os.path.join(DATASETS_CONFIG_FOLDER, cf)
        with open(cf) as f:
            config = json.load(f)

        tags = config.get("tags", [])
        if tag in tags:
            dataset_names.append(config["name"])

    return dataset_names


def update_datafetcher():
    """Updates datafetcher. Downloads and executes the "update.sh" script."""
    import subprocess

    bash_command = "cd $HOME && curl https://raw.githubusercontent.com/vinzeebreak/data-fetcher-install/master/update.sh -sSf | bash"
    output = subprocess.check_output(['bash','-c', bash_command])
