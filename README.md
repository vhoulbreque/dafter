# dafter

## You just found the ultimate datafetcher

Fetches all kind of datasets, whatever the format.

 - [Install](#install)
 - [Commands](#commands)
 - [How to contribute](#how-to-contribute)


## Install

**Last stable version**:
```bash
curl https://raw.githubusercontent.com/vinzeebreak/dafter-install/master/install.sh -sSf | bash
```

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

To list all datasets that have a certain tag, say `image`:
```bash
dafter list image
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
```

or

```bash
curl https://raw.githubusercontent.com/vinzeebreak/dafter-install/master/uninstall.sh -sSf | bash
```

## How to contribute?

### Add a new dataset

To add a new dataset, just add a `json` file called `name-of-the-dataset.json` in the `datasets-configs` folder.

```json
{
  "name": "name-of-the-dataset",
  "urls": [
    "https://site.com/file1.tar.gz",
    "https://site.com/file2.tar.gz",
    "https://site.com/file3.tar.gz"
  ],
  "size": "23.4 MB",
  "type": "tar.gz",
  "tags": ["tag1", "tag2", "tag3"],
  "description": "This is a description of the dataset",
  "source": "https://site.com/"
}
```
