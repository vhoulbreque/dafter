import os
import requests

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
        self.urls = urls
        self.save_path = save_path

        if extension is None:
            extension = normalize_filename(self.urls[0]).split('.')[-1]
        self.extension = extension

        self.save_folder = os.path.join(self.save_path, self.name)
        if not os.path.exists(self.save_folder):
            os.makedirs(self.save_folder)

    def download(self):
        """Handles the download of the different files of the dataset located at
        different urls.
        """

        def download_file(url, local_filename, resume_byte_pose=None):
            """Download a file"""
            if resume_byte_pose:
                resume_header = {'Range': 'bytes=%d-' % resume_byte_pos}
                write_mode = "ab"
            else:
                resume_header = {'Range': 'bytes=%d-' % 0}
                write_mode = "wb"

            # Download from the beginning
            with requests.get(url, stream=True, headers=resume_header) as r:
                with open(local_filename, write_mode) as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:  # filter out keep-alive new chunks
                            f.write(chunk)
                            f.flush()

        print("Downloading {}...".format(self.name))

        stored_f_name = [os.path.join(self.save_folder, f_name)
                                for f_name in os.listdir(self.save_folder)]
        for i, url in enumerate(self.urls):
            print("{} / {} - {}".format(i+1, len(self.urls), url))

            f_name = "{}_{}.{}".format(self.name, i, self.extension) if len(self.urls) > 1 else "{}.{}".format(self.name, self.extension)
            f_name = os.path.join(self.save_folder, f_name)

            # Test if already downloaded
            if f_name in stored_f_name:
                print("{} was already downloaded".format(f_name))
                continue

            # Test if incomplete download
            incomplete_f_name = "{}.incomplete".format(f_name)
            if incomplete_f_name in stored_f_name:
                resume_byte_pos = os.path.getsize(incomplete_f_name)  # 56282L
                resume_byte_pos = str(resume_byte_pos)[:-1]
                resume_byte_pos = int(resume_byte_pos)
            else:
                resume_byte_pos = None

            try:
                download_file(url, incomplete_f_name, resume_byte_pos)
                # From "datasetname.incomplete" to "datasetname"
                os.rename(incomplete_f_name, f_name)
                print("The dataset has been stored in {}".format(self.save_folder))

                url_loader = "https://vinzeebreak.github.io/dafter-loader/docs/{}/".format(self.name)
                print("To load the dataset inside a script or a notebook, see: {}".format(url_loader))
            except Exception as e:
                print("Failed downloading {}".format(url))
                print("Exception : ", e)

    def __repr__(self):
        return self.name
