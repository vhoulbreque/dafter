import os
import pytest
import shutil
import tempfile
import requests

from dafter.fetcher import get_dataset
from dafter.fetcher import delete_dataset
from dafter.fetcher import search_datasets
from dafter.fetcher import get_all_datasets
from dafter.fetcher import DATASETS_FOLDER


def clean_dataset(folder_name=DATASETS_FOLDER):
    try:
        shutil.rmtree(folder_name)
    except:
        pass


def test_get_dataset():

    GOOD_NAME_DATASET = "colleges"
    COLLEGES_FOLDER_NAME = os.path.join(DATASETS_FOLDER, "colleges")
    COLLEGES_FILE_NAME = os.path.join(COLLEGES_FOLDER_NAME, "Colleges.txt")

    # Working examples

    ## With a "name"
    clean_dataset(COLLEGES_FOLDER_NAME)

    d = get_dataset("colleges")
    assert d.name == "colleges"
    assert d.urls == [{"url": "https://beachpartyserver.azurewebsites.net/VueBigData/DataFiles/Colleges.txt", "bytes": 3162832}]
    assert d.save_path == DATASETS_FOLDER
    assert d.save_folder == os.path.join(DATASETS_FOLDER, "colleges")

    ## With a "url"
    clean_dataset(COLLEGES_FOLDER_NAME)

    d = get_dataset("https://raw.githubusercontent.com/vinzeebreak/dafter/master/dafter/datasets-configs/colleges.json")
    assert d.name == "colleges"
    assert d.urls == [{"url": "https://beachpartyserver.azurewebsites.net/VueBigData/DataFiles/Colleges.txt", "bytes": 3162832}]
    assert d.save_path == DATASETS_FOLDER
    assert d.save_folder == os.path.join(DATASETS_FOLDER, "colleges")

    ## With a "path"
    clean_dataset(COLLEGES_FOLDER_NAME)

    r = requests.get("https://raw.githubusercontent.com/vinzeebreak/dafter/master/dafter/datasets-configs/colleges.json")
    with tempfile.TemporaryDirectory() as temp_dir_name:
        temp_json_path = os.path.join(temp_dir_name, "colleges.json")
        with open(temp_json_path, "wb") as f:
            f.write(r.content)
    
        d = get_dataset(temp_json_path)
        assert d.name == "colleges"
        assert d.urls == [{"url": "https://beachpartyserver.azurewebsites.net/VueBigData/DataFiles/Colleges.txt", "bytes": 3162832}]
        assert d.save_path == DATASETS_FOLDER
        assert d.save_folder == os.path.join(DATASETS_FOLDER, "colleges")

    # The dataset has already been fetched
    d = get_dataset("colleges")
    assert d == None

    clean_dataset(COLLEGES_FOLDER_NAME)

    # Invalid arguments
    with pytest.raises(ValueError):
        d = get_dataset(None)
    with pytest.raises(ValueError):
        d = get_dataset(1)
    with pytest.raises(ValueError):
        d = get_dataset([])
    with pytest.raises(ValueError):
        d = get_dataset(())

    # Inexistant datasets
    assert get_dataset("") == None
    assert get_dataset("&é\"'(-è_çà)=&é'(-è_çà)=)") == None
    assert get_dataset("mnist_") == None
    assert get_dataset("MNIST") == None
    assert get_dataset("m\tn\ti\ts\tt") == None
    assert get_dataset("mNIST") == None
    
    # No internet connection
    # TODO

    # Not a valid dataset name, dataset url or json file
    with tempfile.TemporaryDirectory() as temp_dir_name:
        temp_json_path = os.path.join(temp_dir_name, "colleges.json")
        with open(temp_json_path, "w") as f:
            d = {
                "name": "colleges", 
                "urls": [{"url": "https://beachpartyserver.azurewebsites.net/VueBigData/DataFiles/Colleges.txt", "bytes": 3162832}]
            }
            f.write(str(d))
    
        d = get_dataset(temp_json_path)
        assert d == None

    with tempfile.TemporaryDirectory() as temp_dir_name:
        temp_json_path = os.path.join(temp_dir_name, "colleges.json")
        with open(temp_json_path, "w") as f:
            d = {
                "name": "colleges", 
                "urls": [],
                "type": "blah"
            }
            f.write(str(d))
    
        d = get_dataset(temp_json_path)
        assert d == None

    with tempfile.TemporaryDirectory() as temp_dir_name:
        temp_json_path = os.path.join(temp_dir_name, "colleges.json")
        with open(temp_json_path, "w") as f:
            d = {
                "urls": [{"url": "https://beachpartyserver.azurewebsites.net/VueBigData/DataFiles/Colleges.txt", "bytes": 3162832}],
                "type": "blah"
            }
            f.write(str(d))
    
        d = get_dataset(temp_json_path)
        assert d == None

    with tempfile.TemporaryDirectory() as temp_dir_name:
        temp_json_path = os.path.join(temp_dir_name, "colleges.json")
        with open(temp_json_path, "w") as f:
            f.write("blah")
    
        d = get_dataset(temp_json_path)
        assert d == None


def test_delete_dataset():

    d = get_dataset("colleges")
    dataset_config = delete_dataset("colleges")
    assert dataset_config["name"] == "colleges"
    assert dataset_config["urls"] == [{"url": "https://beachpartyserver.azurewebsites.net/VueBigData/DataFiles/Colleges.txt", "bytes": 3162832}]
    assert dataset_config["type"] == "csv"

    # Invalid Arguments
    with pytest.raises(ValueError):
        d = delete_dataset(None)
    with pytest.raises(ValueError):
        d = delete_dataset(1)
    with pytest.raises(ValueError):
        d = delete_dataset([])
    with pytest.raises(ValueError):
        d = delete_dataset(())

    # Inexistant datasets
    assert get_dataset("") is None
    assert get_dataset("&é\"'(-è_çà)=&é'(-è_çà)=)") is None
    assert get_dataset("mnist_") is None
    assert get_dataset("MNIST") is None
    assert get_dataset("m\tn\ti\ts\tt") is None
    assert get_dataset("mNIST") is None

    # The dataset is not in database
    dataset_config = delete_dataset("colleges")
    assert dataset_config is None


def test_get_all_datasets():
    # TODO
    pass


def test_search_datasets():

    with pytest.raises(ValueError):
        search_datasets("datasetname", 1)
    with pytest.raises(ValueError):
        search_datasets("datasetname", [None])
    with pytest.raises(ValueError):
        search_datasets("datasetname", (None,))        
    with pytest.raises(ValueError):
        search_datasets("datasetname", ())
    with pytest.raises(ValueError):
        search_datasets("datasetname", [1, 2])
    with pytest.raises(ValueError):
        search_datasets("datasetname", ("tg1", "tg2"))
    with pytest.raises(ValueError):
        search_datasets("datasetname", ["tg1", None])
    with pytest.raises(ValueError):
        search_datasets("datasetname", ["tg1", None, 1])
    with pytest.raises(ValueError):
        search_datasets(1, ["t1"])
    with pytest.raises(ValueError):
        search_datasets([], ["t1"])
    with pytest.raises(ValueError):
        search_datasets((), ["t1"])
    with pytest.raises(ValueError):
        search_datasets(["datasetname", None, 1], ["t1"])

    assert search_datasets(None, None) != []
    assert search_datasets("datasetname", None) == []
    assert search_datasets("datasetname", []) == []
    assert search_datasets(None, ["t1"]) == []
    assert search_datasets("", ["t1"]) == []
    assert search_datasets("\n\t ", ["t1"]) == []
    assert search_datasets("çàŷù%~#9*", ["t1"]) == []


if __name__ == "__main__":
    pytest.main([__file__])