import os
import pytest
import shutil
import tempfile

from dafter.fetcher import Dataset
from dafter.fetcher import DATASETS_FOLDER


def test_init_dataset():

    GOOD_NAME_DATASET = "good name of dataset"
    GOOD_URLS_ARGUMENT = [{"url": "https://www.example.com/file.json", "bytes": 125541}]

    # Only positional arguments
    with pytest.raises(ValueError):
        d = Dataset(None, None)
    with pytest.raises(ValueError):
        d = Dataset(None, [])
    with pytest.raises(ValueError):
        d = Dataset(None, GOOD_URLS_ARGUMENT)
    with pytest.raises(ValueError):
        d = Dataset("", GOOD_URLS_ARGUMENT)
    with pytest.raises(ValueError):
        d = Dataset("\t\n    \n", GOOD_URLS_ARGUMENT)
    with pytest.raises(ValueError):
        d = Dataset(1, GOOD_URLS_ARGUMENT)
    with pytest.raises(ValueError):
        d = Dataset([], GOOD_URLS_ARGUMENT)
    with pytest.raises(ValueError):
        d = Dataset(GOOD_NAME_DATASET, [])
    with pytest.raises(ValueError):
        d = Dataset(GOOD_NAME_DATASET, 1)
    with pytest.raises(ValueError):
        d = Dataset(GOOD_NAME_DATASET, None)
    with pytest.raises(ValueError):
        d = Dataset(GOOD_NAME_DATASET, [1, 2])
    with pytest.raises(ValueError):
        d = Dataset(GOOD_NAME_DATASET, ())
    with pytest.raises(ValueError):
        d = Dataset(GOOD_NAME_DATASET, [{"blah": "https://www.example.com/file.json", "bytes": 125541}])
    with pytest.raises(ValueError):
        d = Dataset(GOOD_NAME_DATASET, "this is a string")

    # Optional arguments included
    with pytest.raises(ValueError):
        d = Dataset(GOOD_NAME_DATASET, GOOD_URLS_ARGUMENT, None)
    with pytest.raises(ValueError):
        d = Dataset(GOOD_NAME_DATASET, GOOD_URLS_ARGUMENT, 1)
    with pytest.raises(ValueError):
        d = Dataset(GOOD_NAME_DATASET, GOOD_URLS_ARGUMENT, [])

    d = Dataset(GOOD_NAME_DATASET, GOOD_URLS_ARGUMENT)
    assert d.name == "good_name_of_dataset"
    assert d.urls == GOOD_URLS_ARGUMENT
    assert d.save_path == DATASETS_FOLDER
    assert d.save_folder == os.path.join(DATASETS_FOLDER, "good_name_of_dataset")

    d = Dataset("good name of dataset.json", GOOD_URLS_ARGUMENT)
    assert d.name == "good_name_of_dataset"
    assert d.urls == GOOD_URLS_ARGUMENT
    assert d.save_path == DATASETS_FOLDER
    assert d.save_folder == os.path.join(DATASETS_FOLDER, "good_name_of_dataset")

    with tempfile.TemporaryDirectory() as temp_dir_name:
        d = Dataset(GOOD_NAME_DATASET, GOOD_URLS_ARGUMENT, temp_dir_name)
        assert d.name == "good_name_of_dataset"
        assert d.urls == GOOD_URLS_ARGUMENT
        assert d.save_path == temp_dir_name
        assert d.save_folder == os.path.join(temp_dir_name, "good_name_of_dataset")


def clean_dataset(folder_name=DATASETS_FOLDER):
    try:
        shutil.rmtree(folder_name)
    except:
        pass


def test_download():

    def assertions(r):
        assert r.name == "colleges"
        assert r.save_path == DATASETS_FOLDER
        assert r.save_folder == os.path.join(DATASETS_FOLDER, "colleges")
        assert os.path.isdir(COLLEGES_FOLDER_NAME) == True
        assert os.path.isfile(COLLEGES_FILE_NAME) == True


    GOOD_NAME_DATASET = "colleges"
    COLLEGES_FOLDER_NAME = os.path.join(DATASETS_FOLDER, "colleges")
    COLLEGES_FILE_NAME = os.path.join(COLLEGES_FOLDER_NAME, "Colleges.txt")

    # Good download

    clean_dataset(COLLEGES_FOLDER_NAME)

    GOOD_URLS_ARGUMENT = [{"url": "https://beachpartyserver.azurewebsites.net/VueBigData/DataFiles/Colleges.txt", "bytes": 3162832}]

    d = Dataset(GOOD_NAME_DATASET, GOOD_URLS_ARGUMENT)
    r = d.download()

    assertions(r)
    
    size = str(os.path.getsize(COLLEGES_FILE_NAME))
    size = int("".join(c for c in size if c.isdigit()))
    assert size == 3162832

    # Bad "bytes" value

    clean_dataset(COLLEGES_FOLDER_NAME)
    
    BAD_URLS_ARGUMENT = [{"url": "https://beachpartyserver.azurewebsites.net/VueBigData/DataFiles/Colleges.txt", "bytes": 0}]

    d = Dataset(GOOD_NAME_DATASET, BAD_URLS_ARGUMENT)
    r = d.download()
    
    assertions(r)

    size = str(os.path.getsize(COLLEGES_FILE_NAME))
    size = int("".join(c for c in size if c.isdigit()))
    assert size == 3162832

    # Already downloaded
    
    GOOD_URLS_ARGUMENT = [{"url": "https://beachpartyserver.azurewebsites.net/VueBigData/DataFiles/Colleges.txt", "bytes": 3162832}]

    d = Dataset(GOOD_NAME_DATASET, GOOD_URLS_ARGUMENT)
    r = d.download()

    assertions(r)

    size = str(os.path.getsize(COLLEGES_FILE_NAME))
    size = int("".join(c for c in size if c.isdigit()))
    assert size == 3162832

    # Already partially downloaded

    clean_dataset(COLLEGES_FOLDER_NAME)

    os.makedirs(COLLEGES_FOLDER_NAME)
    with open(COLLEGES_FILE_NAME + ".incomplete", "w") as f:
        s = "blah blah " * 500
        f.write(s)
    
    GOOD_URLS_ARGUMENT = [{"url": "https://beachpartyserver.azurewebsites.net/VueBigData/DataFiles/Colleges.txt", "bytes": 3162832}]

    d = Dataset(GOOD_NAME_DATASET, GOOD_URLS_ARGUMENT)
    r = d.download()
    
    assertions(r)

    size = str(os.path.getsize(COLLEGES_FILE_NAME))
    size = int("".join(c for c in size if c.isdigit()))
    assert size == 3162832

    # Already downloaded (but bigger size than what is supposed to exist)
    # Normally, should delete and download again

    clean_dataset(COLLEGES_FOLDER_NAME)

    os.makedirs(COLLEGES_FOLDER_NAME)
    with open(COLLEGES_FILE_NAME, "w") as f:
        for i in range(500000):
            s = "blah blah "
            f.write(s)
    
    GOOD_URLS_ARGUMENT = [{"url": "https://beachpartyserver.azurewebsites.net/VueBigData/DataFiles/Colleges.txt", "bytes": 3162832}]

    d = Dataset(GOOD_NAME_DATASET, GOOD_URLS_ARGUMENT)
    r = d.download()
    
    assertions(r)

    size = str(os.path.getsize(COLLEGES_FILE_NAME))
    size = int("".join(c for c in size if c.isdigit()))
    assert size == 3162832

    # Already downloaded, incomplete but same size as final dataset

    os.rename(COLLEGES_FILE_NAME, "{}.incomplete".format(COLLEGES_FILE_NAME))
    
    GOOD_URLS_ARGUMENT = [{"url": "https://beachpartyserver.azurewebsites.net/VueBigData/DataFiles/Colleges.txt", "bytes": 3162832}]

    d = Dataset(GOOD_NAME_DATASET, GOOD_URLS_ARGUMENT)
    r = d.download()
    
    assertions(r)

    size = str(os.path.getsize(COLLEGES_FILE_NAME))
    size = int("".join(c for c in size if c.isdigit()))
    assert size == 3162832

    # Clean-up

    clean_dataset(COLLEGES_FOLDER_NAME)


if __name__ == "__main__":
    pytest.main([__file__])