import os
import pytest
import tempfile
import requests

from dafter.fetcher import get_dataset
from dafter.fetcher import is_valid_url
from dafter.fetcher import is_valid_path
from dafter.fetcher import delete_dataset
from dafter.fetcher import normalize_name
from dafter.fetcher import is_valid_config
from dafter.fetcher import is_dataset_in_db
from dafter.fetcher import normalize_filename
from dafter.fetcher import get_config_dataset
from dafter.fetcher import check_internet_connection
from dafter.fetcher import is_dataset_being_downloaded

from dafter.fetcher import DATASETS_FOLDER


def test_is_valid_url():

    assert is_valid_url("https://raw.githubusercontent.com/vinzeebreak/dafter/master/dafter/datasets-configs/colleges.json") == True
    assert is_valid_url("https://raw.githubusercontent.com/vinzeebreak/dafter/master/dafter/datasets-configs/crime-data-2010-present-los-angeles.json") == True
    assert is_valid_url("http://raw.githubusercontent.com/vinzeebreak/dafter/master/dafter/datasets-configs/colleges.json") == True
    assert is_valid_url("http://raw.githubusercontent.com/vinzeebreak/dafter/master/dafter/datasets-configs/crime-data-2010-present-los-angeles.json") == True

    assert is_valid_url("https://www.google.com/") == True
    assert is_valid_url("https://www.google.com//") == True
    assert is_valid_url("https://www.google/") == True

    assert is_valid_url("www.google.com") == False
    assert is_valid_url("google.com") == False
    assert is_valid_url("http://example") == False
    assert is_valid_url("êŷŝ%µù;!§°~ç") == False
    assert is_valid_url("êŷŝ%µù;!§°~ç") == False
    assert is_valid_url(None) == False
    assert is_valid_url(1) == False


def test_is_valid_path():
    HOME = os.path.expanduser("~")
    TEMP = tempfile.gettempdir()

    assert is_valid_path(HOME) == False
    assert is_valid_path(TEMP) == False
    assert is_valid_path("êŷŝ%µù;!§°~ç") == False
    assert is_valid_path(None) == False
    assert is_valid_path(1) == False

    f = tempfile.NamedTemporaryFile()
    fname = f.name
    assert is_valid_path(fname) == True
    os.remove(fname)


def test_is_valid_config():

    c1 = {
        "name": "blahblah",
        "urls": [
            {
                "url": "https://www.example.com/"
            },
            {
                "url": "https://www.example2.com/"
            }
        ],
        "type": "csv"
    }
    assert is_valid_config(c1) == True

    c2 = {
        "urls": [
            {
                "url": "https://www.example.com/"
            },
            {
                "url": "https://www.example2.com/"
            }
        ],
        "type": "csv"
    }
    assert is_valid_config(c2) == False

    c3 = {
        "name": "blahblah",
        "type": "csv"
    }
    assert is_valid_config(c3) == False

    c4 = {
        "name": "blahblah",
        "urls": [
            {
                "url": "https://www.example.com/"
            },
            {
                "url": "https://www.example2.com/"
            }
        ]
    }
    assert is_valid_config(c4) == False

    c5 = {
        "name": "blahblah",
        "urls": [],
        "type": "csv"
    }
    assert is_valid_config(c5) == False

    c6 = {
        "name": "blahblah",
        "urls": [
            {
                "url": "www.example"
            },
            {
                "url": "https://www.example2.com/"
            }
        ],
        "type": "csv"
    }
    assert is_valid_config(c6) == False

    c7 = {
        "name": "blahblah",
        "urls": [
            {
                "url": None
            }
        ],
        "type": "csv"
    }
    assert is_valid_config(c7) == False

    c8 = {
        "name": None,
        "urls": [
            {
                "url": "https://www.example.com/"
            },
            {
                "url": "https://www.example2.com/"
            }
        ],
        "type": "csv"
    }
    assert is_valid_config(c8) == False

    assert is_valid_config([]) == False
    assert is_valid_config(dict()) == False
    assert is_valid_config(1) == False
    assert is_valid_config("") == False
    assert is_valid_config(None) == False


def test_normalize_filename():

    assert normalize_filename("test") == "test"
    assert normalize_filename("àéèçüïöëîûâêôŷ") == "àéèçüïöëîûâêôŷ"
    assert normalize_filename("https://example.com/file.json/") == "file.json"
    assert normalize_filename("https://example.com/file.json") == "file.json"
    assert normalize_filename("https://example.com/file.json/?param=zjzj") == "file.json"
    assert normalize_filename("https://example.com/file.json?param=zdoz") == "file.json"
    assert normalize_filename("") == ""
    
    with pytest.raises(ValueError):
        _ = normalize_filename(None)
    with pytest.raises(ValueError):
        _ = normalize_filename(1)
    with pytest.raises(ValueError):
        _ = normalize_filename([])
    with pytest.raises(ValueError):
        _ = normalize_filename(())


def test_normalize_name():

    assert normalize_name("azertyuiop") == "azertyuiop"
    assert normalize_name("\tazertyuiop") == "_azertyuiop"
    assert normalize_name("azertyuiop\t") == "azertyuiop_"
    assert normalize_name("azert\tyuiop") == "azert_yuiop"
    assert normalize_name("\t\taze\trtyui\top\t\t") == "__aze_rtyui_op__"
    assert normalize_name(" azertyuiop") == "_azertyuiop"
    assert normalize_name("azertyuiop ") == "azertyuiop_"
    assert normalize_name("azert yuiop") == "azert_yuiop"
    assert normalize_name("  aze rtyui op  ") == "__aze_rtyui_op__"
    assert normalize_name("\nazertyuiop") == "_azertyuiop"
    assert normalize_name("azertyuiop\n") == "azertyuiop_"
    assert normalize_name("azert\nyuiop") == "azert_yuiop"
    assert normalize_name("\n\naze\nrtyui\nop\n\n") == "__aze_rtyui_op__"
    assert normalize_name("\t\n azertyuiop") == "___azertyuiop"
    assert normalize_name("azertyuiop\n\t ") == "azertyuiop___"
    assert normalize_name("azert\t\n yuiop") == "azert___yuiop"
    assert normalize_name("\t\n aze \t\nrtyui\t \nop\t\n ") == "___aze___rtyui___op___"
    assert normalize_name("azer\n tyuio\tp") == "azer__tyuio_p"

    assert normalize_name("azertyuiop.json") == "azertyuiop"
    assert normalize_name("\tazertyuiop.json") == "_azertyuiop"
    assert normalize_name("azertyuiop\t.json") == "azertyuiop_"
    assert normalize_name("azert\tyuiop.json") == "azert_yuiop"
    assert normalize_name("\t\taze\trtyui\top\t\t.json") == "__aze_rtyui_op__"
    assert normalize_name(" azertyuiop.json") == "_azertyuiop"
    assert normalize_name("azertyuiop .json") == "azertyuiop_"
    assert normalize_name("azert yuiop.json") == "azert_yuiop"
    assert normalize_name("  aze rtyui op  .json") == "__aze_rtyui_op__"
    assert normalize_name("\nazertyuiop.json") == "_azertyuiop"
    assert normalize_name("azertyuiop\n.json") == "azertyuiop_"
    assert normalize_name("azert\nyuiop.json") == "azert_yuiop"
    assert normalize_name("\n\naze\nrtyui\nop\n\n.json") == "__aze_rtyui_op__"
    assert normalize_name("\t\n azertyuiop.json") == "___azertyuiop"
    assert normalize_name("azertyuiop\n\t .json") == "azertyuiop___"
    assert normalize_name("azert\t\n yuiop.json") == "azert___yuiop"
    assert normalize_name("\t\n aze \t\nrtyui\t \nop\t\n .json") == "___aze___rtyui___op___"
    assert normalize_name("azer\n tyuio\tp.json") == "azer__tyuio_p"

    with pytest.raises(ValueError):
        _ = normalize_name(None)
    with pytest.raises(ValueError):
        _ = normalize_name(1)
    with pytest.raises(ValueError):
        _ = normalize_name([])
    with pytest.raises(ValueError):
        _ = normalize_name(())


def test_is_dataset_being_downloaded():
    # Wrong inputs

    with pytest.raises(ValueError):
        is_dataset_being_downloaded(None)
    with pytest.raises(ValueError):
        is_dataset_being_downloaded(1)
    with pytest.raises(ValueError):
        is_dataset_being_downloaded([])
    with pytest.raises(ValueError):
        is_dataset_being_downloaded(())
    with pytest.raises(ValueError):
        is_dataset_being_downloaded(True)
    with pytest.raises(ValueError):
        is_dataset_being_downloaded(["mnist", "colleges"])

    # Good inputs

    assert is_dataset_being_downloaded("") == False
    assert is_dataset_being_downloaded("è&ŷŝ%ùµ*9_`\"{}") == False

    get_dataset("colleges")
    assert is_dataset_being_downloaded("colleges") == False

    delete_dataset("colleges")
    assert is_dataset_being_downloaded("colleges") == False
    
    os.makedirs(os.path.join(DATASETS_FOLDER, "colleges"))
    COLLEGES_DATASET_PATH = os.path.join(DATASETS_FOLDER, "colleges", "Colleges.txt")
    with open(COLLEGES_DATASET_PATH, "w") as f:
        f.write("blah blah "* 500)
    assert is_dataset_being_downloaded("colleges") == True

    # TODO:
    # Raise an Exception here -> not supposed to have different dataset names, are we?
    os.rename(COLLEGES_DATASET_PATH, os.path.join(DATASETS_FOLDER, "colleges", "ahahah.txt"))
    assert is_dataset_being_downloaded("colleges") == True


def test_get_config_dataset():
    # Wrong input
    with pytest.raises(ValueError):
        get_config_dataset(None)
    with pytest.raises(ValueError):
        get_config_dataset([])
    with pytest.raises(ValueError):
        get_config_dataset([None])
    with pytest.raises(ValueError):
        get_config_dataset(["mnist"])
    with pytest.raises(ValueError):
        get_config_dataset(())
    with pytest.raises(ValueError):
        get_config_dataset(1)
    with pytest.raises(ValueError):
        get_config_dataset(True)
    with pytest.raises(ValueError):
        get_config_dataset(dict())

    # Inexistant dataset

    ## Name
    assert get_config_dataset("") is None
    assert get_config_dataset("\n\t ") is None
    assert get_config_dataset("è&ŷŝ%ùµ*9_`\"") is None

    ## Path
    f = tempfile.NamedTemporaryFile()
    fname = f.name
    assert get_config_dataset(fname) is None
    os.remove(fname)

    r = requests.get("https://raw.githubusercontent.com/vinzeebreak/ironcar/master/config.json")
    with tempfile.TemporaryDirectory() as temp_dir_name:
        temp_json_path = os.path.join(temp_dir_name, "config.json")
        with open(temp_json_path, "wb") as f:
            f.write(r.content)

        config = get_config_dataset(temp_json_path)
        assert config is None

    ## Url
    assert get_config_dataset("https://raw.githubusercontent.com/vinzeebreak/ironcar/master/config.json") is None

    # Existing dataset

    ## Url
    config = get_config_dataset("https://raw.githubusercontent.com/vinzeebreak/dafter/master/dafter/datasets-configs/colleges.json")
    assert config["name"] == "colleges"
    assert config["urls"] == [{"url": "https://beachpartyserver.azurewebsites.net/VueBigData/DataFiles/Colleges.txt", "bytes": 3162832}]
    assert config["type"] == "csv"

    ## Path
    r = requests.get("https://raw.githubusercontent.com/vinzeebreak/dafter/master/dafter/datasets-configs/colleges.json")
    with tempfile.TemporaryDirectory() as temp_dir_name:
        temp_json_path = os.path.join(temp_dir_name, "colleges.json")
        with open(temp_json_path, "wb") as f:
            f.write(r.content)

        config = get_config_dataset(temp_json_path)
        assert config["name"] == "colleges"
        assert config["urls"] == [{"url": "https://beachpartyserver.azurewebsites.net/VueBigData/DataFiles/Colleges.txt", "bytes": 3162832}]
        assert config["type"] == "csv"

    ## Real datasetname
    config = get_config_dataset("colleges")
    assert config["name"] == "colleges"
    assert config["urls"] == [{"url": "https://beachpartyserver.azurewebsites.net/VueBigData/DataFiles/Colleges.txt", "bytes": 3162832}]
    assert config["type"] == "csv"


def test_is_dataset_in_db():
    DATASET_NAME = "colleges"

    get_dataset(DATASET_NAME)
    assert is_dataset_in_db(DATASET_NAME) == True

    delete_dataset(DATASET_NAME)
    assert is_dataset_in_db(DATASET_NAME) == False

    # Wrong inputs
    with pytest.raises(ValueError):
        is_dataset_in_db(None)
    with pytest.raises(ValueError):
        is_dataset_in_db([])
    with pytest.raises(ValueError):
        is_dataset_in_db(["colleges"])
    with pytest.raises(ValueError):
        is_dataset_in_db(())
    with pytest.raises(ValueError):
        is_dataset_in_db(True)

    # Strange strings
    assert is_dataset_in_db("") == False
    assert is_dataset_in_db("è&ŷŝ%ùµ*9_`\"") == False


def test_check_internet_connection():
    # TODO
    pass


if __name__ == "__main__":
    pytest.main([__file__])
