#!/usr/bin/python
# coding=utf-8

import sys
import argparse

from dafter.fetcher.utils import get_config_dataset, get_version
from dafter.fetcher.fetcher import get_dataset, delete_dataset, list_datasets, \
    info_dataset, search_datasets


DESCRIPTION = "Fetches all kind of datasets, whatever the format. Without pain."
USAGE = """usage: dafter [get dataset-name] [delete dataset-name] [info dataset-name] [list [dataset-name] [--tags tag0 .. tagN]] [search [dataset-name] [--tags tag0 .. tagN]]

Positional arguments:
  get dataset-name                               Downloads and saves the dataset files
  delete dataset-name                            Deletes the dataset files from the disk
  info dataset-name                              Describes the dataset
  list [dataset-name] [--tags tag0 .. tagN]      Lists all the datasets that are in database
  search [dataset-name] [--tags tag0 .. tagN]    Lists all the datasets available with these tags
  version                                        Get the version of dafter
"""

class DafterCLI():

    def __init__(self):
        self.parser = argparse.ArgumentParser(description=DESCRIPTION, usage=USAGE)
        self.parser.add_argument("command", help="Subcommand to run")

        args = self.parser.parse_args(sys.argv[1:2])

        if not hasattr(self, args.command):
            print("Unrecognized command")
            self.parser.print_help()
            exit(1)
        getattr(self, args.command)()

    def help(self):
        self.parser.print_help()
        exit(1)

    def version(self):
        v = get_version()
        print(v)

    def get(self):
        self.parser = argparse.ArgumentParser(description="Downloads and saves the dataset files")
        self.parser.add_argument('datasetname', help="Name of the dataset")

        args = self.parser.parse_args(sys.argv[2:])

        if not hasattr(args, "datasetname"):
            print("A dataset name is required")
            self.parser.print_help()
            exit(1)

        dataset_config = get_config_dataset(args.datasetname)
        if dataset_config:
            get_dataset(dataset_config)

    def delete(self):
        self.parser = argparse.ArgumentParser(description="Deletes the dataset files from the disk")
        self.parser.add_argument('datasetname', help="Name of the dataset")

        args = self.parser.parse_args(sys.argv[2:])

        if not hasattr(args, "datasetname"):
            print("A dataset name is required")
            self.parser.print_help()
            exit(1)

        dataset_config = get_config_dataset(args.datasetname)
        if dataset_config:
            delete_dataset(dataset_config)

    def info(self):
        self.parser = argparse.ArgumentParser(description="Describes the dataset")
        self.parser.add_argument('datasetname', help="Name of the dataset")

        args = self.parser.parse_args(sys.argv[2:])

        if not hasattr(args, "datasetname"):
            print("A dataset name is required")
            self.parser.print_help()
            exit(1)

        dataset_config = get_config_dataset(args.datasetname)
        if dataset_config:
            info_dataset(dataset_config)

    def search(self):
        self.parser = argparse.ArgumentParser(description="Lists all the datasets available with these tags")
        self.parser.add_argument("datasetname", help="keyword", nargs="?", default=None)
        self.parser.add_argument('--tags', help="tags", nargs='+', required=False)

        args = self.parser.parse_args(sys.argv[2:])

        datasetname = args.datasetname if hasattr(args, "datasetname") else None
        tags = args.tags if args.tags else []

        search_datasets(datasetname, tags)

    def list(self):
        self.parser = argparse.ArgumentParser(description="Lists all the datasets that are in database")
        self.parser.add_argument("datasetname", help="keyword", nargs="?", default=None)
        self.parser.add_argument('--tags', help="tags", nargs='+', required=False)

        args = self.parser.parse_args(sys.argv[2:])

        datasetname = args.datasetname if hasattr(args, "datasetname") else None
        tags = args.tags if hasattr(args, "tags") else []

        list_datasets(datasetname, tags)

def main():
    DafterCLI()
