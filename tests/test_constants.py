import pytest

from os.path import isdir

from dafter.fetcher import DATASETS_FOLDER
from dafter.fetcher import DATASETS_CONFIG_FOLDER


def test_directories():

    assert isdir(DATASETS_FOLDER) == True
    assert isdir(DATASETS_CONFIG_FOLDER) == True


if __name__ == "__main__":
    pytest.main([__file__])