# dafter : the data fetcher

![dafter-logo](docs/dafter_logo.png)

## You have just found dafter.

Dafter is a command line downloader of public datasets. It takes care of downloading and formatting the datasets' files so that you can spend hours building models instead of looking for datasets and their urls.

 - [Install](#install-dafter)
 - [Commands](#commands)
 - [How to contribute](#how-to-contribute)


## Install dafter

To install dafter, just do:
```bash
pip install dafter
```

## Commands

To download the MNIST dataset:
```bash
dafter get mnist
```

To delete MNIST from your machine:
```bash
dafter delete mnist
```

To search among downloadable datasets:
```bash
# Search all available datasets
dafter search
# Search all available datasets that have the tags "image" and "deep-learning"
# and whose name contains "mni"
dafter search mni --tags image deep-learning
```

To list all the datasets that have been downloaded and are stored on your machine:
```bash
# Lists all datasets in database
dafter list
# Lists all datasets in database that have the tag "twitter" and whose name
# contains "sentiment"
dafter list sentiment --tags twitter
```

## Update

To update `dafter`, do:
```bash
pip install --upgrade dafter
```

## Uninstall

To uninstall `dafter`, do:

```bash
pip uninstall dafter
```

## How to contribute?

### Add a new dataset

To add a new dataset, just add a `json` file called `name-of-the-dataset.json` in the `datasets-configs` folder.

```json
{
  "name": "name-of-the-dataset",
  "urls": [
    {
      "url": "https://site.com/file1.tar.gz",
      "bytes": 45221
    },
    {
      "url": "https://site.com/file2.tar.gz",
      "bytes": 1147803
    }
  ],
  "type": "tar.gz",
  "tags": ["tag1", "tag2", "tag3"],
  "description": "This is a description of the dataset",
  "source": "https://site.com/"
}
```
