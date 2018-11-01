import os
import io
import gzip
import zipfile

import requests

from fetcher import DOWNLOAD_CONFIG_FILE
from .utils import normalize_name
from .downloadhelper import DownloadHelper


class Dataset:
    """Object representing a dataset"""

    def __init__(self, name, urls, extension=None, save_path=None):
        """
        Args:
            name (str): The name of the dataset.
            urls (list of str): The list of all the urls containing a file to
                download.
            extension (str, optional): The extension of the files being
                downloaded.
            save_path (str, optional): The folder where to save the files of
                the dataset being downloaded.
        """
        self.name = normalize_name(name)
        self.urls = urls
        self.save_path = save_path

        if extension is None:
            extension = normalize_filename(self.urls[0]).split('.')[-1]
        self.extension = extension

        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)

    def _handle_post_download(self, filename):
        """Handles the post download processing. Can unzip, uncompress, unpickle
        the files depending on their extensions.

        Args:
            filename (str): the filename of the particular file that needs to be
                processed.
        """
        pass

    def download(self):
        """Handles the download of the different files of the dataset located at
        different urls.
        """
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
                # Useful to resume an interrupted download
                dh = DownloadHelper(self.name, f_name)
                dh.create_chunk_count()
                chunks_to_skip = dh.get_chunk_count()
                with open(f_name, 'wb') as f:
                    c = 0
                    for chunk in r:
                        c += 1
                        if c > chunks_to_skip:
                            f.write(chunk)
                            dh.add_chunk_count(n_chunks=1)
                dh.remove_chunk_count()
                self._handle_post_download(f_name)
            else:
                print("Failed downloading {}".format(url))

    def __repr__(self):
        return self.name
