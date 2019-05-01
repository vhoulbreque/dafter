#!/usr/bin/python
# coding=utf-8

import os
import requests
from tqdm import tqdm

from .utils import normalize_name, normalize_filename


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
        self.urls = urls  # List of dicts ("url", "bytes")
        self.save_path = save_path

        if extension is None:
            extension = normalize_filename(self.urls[0]["url"]).split('.')[-1]
        self.extension = extension

        self.save_folder = os.path.join(self.save_path, self.name)
        if not os.path.exists(self.save_folder):
            os.makedirs(self.save_folder)

    def download(self):
        """Handles the download of the different files of the dataset located at
        different urls.
        """

        def fit_desc_size(desc):
            LEN_FINAL_DESC = 20
            if desc is None:
                return " " * LEN_FINAL_DESC
            if len(desc) == LEN_FINAL_DESC:
                return desc
            if len(desc) <= LEN_FINAL_DESC:
                return " " * (LEN_FINAL_DESC-len(desc)) + desc
            index = (LEN_FINAL_DESC-1)//2
            return desc[:index] + ".." + desc[-index:]

        def download_file(url, dst, first_byte=None, file_size=None, desc=None):
            """Download a file

            Args:
                url (str): The url of the file to download
                dst (str): The name of the file and its path where the
                    downloaded file will be stored
                first_byte (int): Non zero if the file has already been
                    downloaded but the download has previously been
                    interrupted. Number of bytes already downloaded
                file_size (int): The total file size of the downloaded file
                desc (str): The description string that is used to decorate
                    the progress bar

            Returns:
                None
            """

            if first_byte is None:
                first_byte = 0
            if file_size is None:
                headers = requests.head(url).headers
                if "Content-Length" in headers:
                    file_size = int(headers["Content-Length"])

            resume_header = {'Range': 'bytes=%s-' % (first_byte)}

            pbar = tqdm(total=file_size, initial=first_byte, unit='B', unit_scale=True, desc=desc)

            r = requests.get(url, headers=resume_header, stream=True)
            with open(dst, 'ab') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        f.flush()
                        pbar.update(len(chunk))
            pbar.close()

        print("Downloading {}...".format(self.name))

        stored_f_name = [os.path.join(self.save_folder, f_name)
                                for f_name in os.listdir(self.save_folder)]
        exception = False
        for i, url_d in enumerate(self.urls):
            url = url_d.get("url", None)
            file_size = url_d.get("bytes", None)
            small_url = fit_desc_size(url.split('/')[-1])
            desc = "{} / {} - {}".format(i+1, len(self.urls), small_url)

            f_name = "{}_{}.{}".format(self.name, i, self.extension) if len(self.urls) > 1 else "{}.{}".format(self.name, self.extension)
            f_name = os.path.join(self.save_folder, f_name)

            # Test if already downloaded
            if f_name in stored_f_name:
                continue

            # Test if incomplete download
            incomplete_f_name = "{}.incomplete".format(f_name)
            if incomplete_f_name in stored_f_name:
                first_byte = str(os.path.getsize(incomplete_f_name))  # 56282L
                first_byte = "".join(c for c in first_byte if c.isdigit())
                first_byte = int(first_byte)
            else:
                first_byte = None

            try:
                download_file(url, incomplete_f_name, first_byte, file_size, desc)
                # From "datasetname.incomplete" to "datasetname"
                os.rename(incomplete_f_name, f_name)
            except Exception as e:
                exception = True
                print("Failed downloading {}".format(url))
                print("Exception : ", e)

        if not exception:
            print("The dataset has been stored in {}".format(self.save_folder))
            url_loader = "https://vinzeebreak.github.io/dafter-loader/docs/datasets/{}/".format(self.name)
            print("To load the dataset inside a script or a notebook, see: {}".format(url_loader))

    def __repr__(self):
        return self.name
