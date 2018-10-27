import os
import io
import gzip
import zipfile

import requests

from .utils import normalize_name


class Dataset:

    def __init__(self, name, urls, extension=None, save_path=None):
        self.name = normalize_name(name)
        self.urls = urls
        self.save_path = save_path

        if extension is None:
            extension = normalize_filename(self.urls[0]).split('.')[-1]
        self.extension = extension

        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)

    def download(self):
        print("Downloading {}...".format(self.name))

        folder = os.path.join(self.save_path, self.name)
        if not os.path.exists(folder):
            os.makedirs(folder)

        for i, url in enumerate(self.urls):
            print("{} / {} - {}".format(i+1, len(self.urls), url))
            if len(self.urls) > 1:
                f_name = "{}_{}.{}".format(self.name, i, self.extension)
            else:
                f_name = "{}.{}".format(self.name, self.extension)
            f_name = os.path.join(folder, f_name)

            r = requests.get(url, stream=True)
            if r.status_code == 200:
                with open(f_name, 'wb') as f:
                    for chunk in r:
                        f.write(chunk)
            else:
                print("Failed downloading {}".format(url))

    def __repr__(self):
        return self.name
