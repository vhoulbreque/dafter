import sys
import readline

from fetcher.fetcher import get_dataset
from fetcher.utils import get_config_dataset


args = sys.argv[1:]

if args:
    action = args[0]
    if action not in ["get", "delete"]:
        raise Exception("Wrong action")
    args = args[1:]

    if args:
        datasetname = args[0]
    else:
        raise Exception("No dataset")
else:
    raise Exception("No args")


dataset_config = get_config_dataset(datasetname)
if dataset_config:
    if action == "get":
        get_dataset(dataset_config)
    elif action == "delete":
        delete_dataset(dataset_config)
    else:
        print("No action")
else:
    raise Exception("The dataset does not exist")
