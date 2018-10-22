# datafetcher

## You just found the ultimate datafetcher

Fetches all kind of datasets, whatever the format.
For now, the supported formats are `.csv` and `.zip`.

## Install

To install `datafetcher`, do:
```bash
curl https://raw.githubusercontent.com/vinzeebreak/data-fetcher-install/master/install.sh -sSf | sh
```

## Commands

To download a dataset:
```bash
datafetcher get dataset-name
```

To delete a dataset from the database:
```bash
datafetcher delete dataset-name
```

To list all datasets that have a certain tag:
```bash
datafetcher list tag
```
