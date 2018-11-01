import os

HOME = os.path.expanduser("~")
CURRENT_FOLDER = "/".join(__file__.split("/")[:-1])

DATASETS_CONFIG_FOLDER = os.path.join(CURRENT_FOLDER, "..", "datasets-configs")
DATASETS_FOLDER = os.path.join(HOME, ".datasets-data-fetcher")
DOWNLOAD_CONFIG_FILE = os.path.join(HOME, ".datafetcher", "download-config.txt")

__all__ = ["DATASETS_CONFIG_FOLDER", "DATASETS_FOLDER", "DOWNLOAD_CONFIG_FILE"]
