#!/usr/bin/python
# coding=utf-8

import os
import shutil
import requests
from tqdm import tqdm

from .constants import DATASETS_FOLDER
from .utils import normalize_name, normalize_filename


class Dataset:
    """Object representing a dataset"""

    def __init__(self, name, urls, save_path=DATASETS_FOLDER):
        """
        Args:
            name (str): The name of the dataset.
            urls (list of str): The list of all the urls containing a file to
                download.
            save_path (str, optional): The folder where to save the files of
                the dataset being downloaded.
        """
        # Name
        if not isinstance(name, str) or name.strip() == "":
            raise ValueError("Wrong name for dataset : {}".format(name))
        self.name = normalize_name(name) 

        # Urls
        if not isinstance(urls, list):
            raise ValueError("Wrong type for urls : got {} instead of list".format(type(urls)))
        if not urls:
            raise ValueError("List of urls cannot be empty")
        for u_ in urls:
            if not isinstance(u_, dict) or "url" not in u_:
                raise ValueError("urls must be a list of dict objects with \"url\" field")
        self.urls = urls  # List of dicts ("url", "bytes")

        # Save_path
        if not isinstance(save_path, str):
            raise ValueError("save_path cannot be of type {}".format(type(save_path)))
        save_folder = os.path.join(save_path, self.name)
        try:
            if not os.path.exists(save_folder):
                os.makedirs(save_folder)
            self.save_folder = save_folder
            self.save_path = save_path
        except:
            raise ValueError("Incorrect save_path : {}".format(save_path))


    def download(self):
        """Handles the download of the different files of the dataset located at
        different urls.
        """
        def fit_desc_size(s):
            LEN_FINAL_DESC = 20
            if s is None:
                return " " * LEN_FINAL_DESC
            if len(s) == LEN_FINAL_DESC:
                return s
            if len(s) <= LEN_FINAL_DESC:
                return " " * (LEN_FINAL_DESC-len(s)) + s
            index = (LEN_FINAL_DESC-1)//2
            return s[:index] + ".." + s[-index:]

        def download_file(url, dst, first_byte=None, total_bytes=None, desc=None):
            """Download a file

            Args:
                url (str): The url of the file to download
                dst (str): The name of the file and its path where the
                    downloaded file will be stored
                first_byte (int): Non zero if the file has already been
                    downloaded but the download has previously been
                    interrupted. Number of bytes already downloaded
                total_bytes (int): The total file size of the downloaded file
                desc (str): The description string that is used to decorate
                    the progress bar

            Returns:
                None
            """

            if first_byte is None:
                first_byte = 0
            if total_bytes is None:
                headers = requests.head(url).headers
                if "Content-Length" in headers:
                    total_bytes = int(headers["Content-Length"])

            resume_header = {'Range': 'bytes=%s-' % (first_byte)}

            pbar = tqdm(total=total_bytes, initial=first_byte, unit='B', unit_scale=True, desc=desc)

            r = requests.get(url, headers=resume_header, stream=True)
            with open(dst, 'ab') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        f.flush()
                        pbar.update(len(chunk))
            pbar.close()

        def get_size_file(path):
            size = str(os.path.getsize(path))  # eg. 56282L
            size = "".join(c for c in size if c.isdigit())
            size = int(size)
            return size

        # Files that are already stored in the save_path folder
        stored_f_name = [os.path.join(self.save_folder, f_name)
                                for f_name in os.listdir(self.save_folder)]
                                
        for i, url_ in enumerate(self.urls):
            url = url_.get("url", None)
            total_bytes = url_.get("bytes", None)

            url_filename = normalize_filename(url)

            f_name = os.path.join(self.save_folder, url_filename)

            # Test if already downloaded
            if f_name in stored_f_name:
                if total_bytes:
                    saved_size = get_size_file(f_name)
                    if saved_size != total_bytes:
                        # Cannot take any risk: the file must be downloaded again
                        os.remove(f_name)
                    else:
                        continue
                else:
                    continue

            # Test if incomplete download
            incomplete_f_name = "{}.incomplete".format(f_name)
            if incomplete_f_name in stored_f_name:
                first_byte = get_size_file(incomplete_f_name)

                # If already downloaded, just misnamed
                if total_bytes and total_bytes == first_byte:
                    os.rename(incomplete_f_name, f_name)
                    continue
            else:
                first_byte = None

            # String displayed on the progress bar
            small_url = fit_desc_size(url_filename)
            desc = "{} / {} - {}".format(i+1, len(self.urls), small_url)

            download_file(url, incomplete_f_name, first_byte, total_bytes, desc)

            # From "datasetname.incomplete" to "datasetname"
            os.rename(incomplete_f_name, f_name)

        return self

    def __repr__(self):
        return self.name
