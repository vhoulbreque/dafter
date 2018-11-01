import os

from fetcher import DOWNLOAD_CONFIG_FILE


class DownloadHelper:
    """DownloadHelper object aims at resuming the interrupted downloads easily.
    """

    def __init__(self, datasetname, filename):
        """A DownloadHelper object helps for one particular file of one
        particular dataset.

        Args:
            datasetname (str): The name of the dataset.
            filename (str): The name of the file.
        """
        self.datasetname = datasetname
        self.filename = filename

    def _get_lines_config(self):
        """Get all the lines of the dataset download configuration file.

        Returns:
            lines (list of str): All the lines of the configuration file.
        """
        lines = []
        with open(DOWNLOAD_CONFIG_FILE, "r") as f:
            lines = [line.rstrip('\n') for line in f if line]
        return lines

    def create_chunk_count(self):
        """Creates the line with the chunk count at 0. If the line already
        exists, does nothing.
        """
        lines = self._get_lines_config()

        for line in lines:
            l = line.split('\t')
            d_name = l[0]
            f_name = l[1]

            if d_name == self.datasetname and f_name == self.filename:
                return

        with open(DOWNLOAD_CONFIG_FILE, "a") as f:
            f.write("{}\t{}\t{}\n".format(self.datasetname, self.filename, 0))

    def get_chunk_count(self):
        """Gets the number of chunks already downloaded. If the download has
        been interrupted, returns the value read from the configuration file
        else, returns 0.

        Returns:
            chunk_count (int): the number of chunks already downloaded.
        """
        lines = self._get_lines_config()

        for line in lines:
            l = line.split('\t')
            d_name = l[0]
            f_name = l[1]

            if d_name == self.datasetname and f_name == self.filename:
                return int(l[2])
        return 0

    def remove_chunk_count(self):
        """Removes the chunk count."""
        lines = self._get_lines_config()

        with open(DOWNLOAD_CONFIG_FILE, "w") as f:
            for line in lines:
                l = line.split('\t')
                d_name = l[0]
                f_name = l[1]
                if d_name == self.datasetname and f_name == self.filename:
                    continue
                f.write("{}\n".format(line))

    def add_chunk_count(self, n_chunks=1):
        """Updates the downloaded chunk count.

        Args:
            n_chunks (int, optional): the number of chunks to add to the
                current chunk count.
        """
        lines = self._get_lines_config()

        with open(DOWNLOAD_CONFIG_FILE, "w") as f:
            for line in lines:
                l = line.split('\t')
                d_name = l[0]
                f_name = l[1]
                c = int(l[2])
                if d_name == self.datasetname and f_name == self.filename:
                    # increase the counter only for the right dataset
                    # and the right file
                    c += n_chunks
                new_line = "{}\t{}\t{}\n".format(d_name, f_name, c)
                f.write(new_line)
