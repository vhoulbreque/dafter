import os
import io
import gzip
import zipfile

import requests

from .utils import normalize_name


class Dataset:

    def __init__(self, name, urls, save_path=None):
        self.name = normalize_name(name)
        self.urls = urls
        self.save_path = save_path

        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)

    def __repr__(self):
        return self.name


class CSVDataset(Dataset):

    def __init__(self, name, urls, save_path=None):
        Dataset.__init__(self, name, urls, save_path=save_path)

    def download(self):
        print("Downloading {}...".format(self.name))

        folder = os.path.join(self.save_path, self.name)
        if not os.path.exists(folder):
            os.makedirs(folder)

        for i, url in enumerate(self.urls):
            print("{} / {} - {}".format(i+1, len(self.urls), url))
            resp = requests.get(url)

            if len(self.urls) > 1:
                f_name = "{}_{}.csv".format(self.name, i)
            else:
                f_name = "{}.csv".format(self.name)

            f_name = os.path.join(folder, f_name)

            with open(f_name, 'w') as f:
                f.write(resp.text)


class ZIPDataset(Dataset):

    def __init__(self, name, urls, save_path=None):
        Dataset.__init__(self, name, urls, save_path=save_path)

    def download(self):
        print("Downloading {}...".format(self.name))

        folder = os.path.join(self.save_path, self.name)
        if not os.path.exists(folder):
            os.makedirs(folder)

        for i, url in enumerate(self.urls):
            print("{} / {} - {}".format(i+1, len(self.urls), url))

            r = requests.get(url, stream=True)
            if r.status_code == 200:
                z = zipfile.ZipFile(io.BytesIO(r.content))
                z.extractall(folder)
            else:
                print("Failed downloading {}".format(url))


class GZDataset(Dataset):

    def __init__(self, name, urls, save_path=None):
        Dataset.__init__(self, name, urls, save_path=save_path)

    def download(self):
        print("Downloading {}...".format(self.name))

        folder = os.path.join(self.save_path, self.name)
        if not os.path.exists(folder):
            os.makedirs(folder)

        for i, url in enumerate(self.urls):
            print("{} / {} - {}".format(i+1, len(self.urls), url))
            if len(self.urls) > 1:
                f_name = "{}_{}.gz".format(self.name, i)
            else:
                f_name = "{}.gz".format(self.name)
            f_name = os.path.join(folder, f_name)

            r = requests.get(url, stream=True)
            if r.status_code == 200:
                with open(f_name, 'wb') as f:
                    for chunk in r:
                        f.write(chunk)
            else:
                print("Failed downloading {}".format(url))


class TarDataset(Dataset):

    def __init__(self, name, urls, save_path=None):
        Dataset.__init__(self, name, urls, save_path=save_path)

    def download(self):
        print("Downloading {}...".format(self.name))

        folder = os.path.join(self.save_path, self.name)
        if not os.path.exists(folder):
            os.makedirs(folder)

        for i, url in enumerate(self.urls):
            print("{} / {} - {}".format(i+1, len(self.urls), url))
            if len(self.urls) > 1:
                f_name = "{}_{}.tar.gz".format(self.name, i)
            else:
                f_name = "{}.tar.gz".format(self.name)
            f_name = os.path.join(folder, f_name)

            r = requests.get(url, stream=True)
            if r.status_code == 200:
                with open(f_name, 'wb') as f:
                    for chunk in r:
                        f.write(chunk)
            else:
                print("Failed downloading {}".format(url))
