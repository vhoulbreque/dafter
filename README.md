# dafter

## You just found the ultimate datafetcher

Fetches all kind of datasets, whatever the format.

 - [Install](#install)
 - [Commands](#commands)
 - [How to contribute](#how-to-contribute)


## Install

**Up-to-date version**:
```bash
curl https://raw.githubusercontent.com/vinzeebreak/dafter-install/master/install.sh -sSf | bash -s -- --up-to-date
```

## Commands

To download the MNIST dataset:
```bash
dafter get mnist
```

To delete MNIST from the database:
```bash
dafter delete mnist
```

To search among available datasets:
```bash
# Search all available datasets
dafter search
# Search all available datasets that have the tags "image" and "deep-learning"
# and whose name contains "mni"
dafter search mni --tags image deep-learning
```

To list all downloaded datasets:
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
dafter update
```

## Uninstall

To uninstall `dafter`, do:

```bash
dafter uninstall
# or
curl https://raw.githubusercontent.com/vinzeebreak/dafter-install/master/uninstall.sh -sSf | bash
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
