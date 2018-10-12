

class CSVDataset(Dataset):

    def __init__(self):
        pass

    def save(self, path):
        pass

    def __repr__(self):
        return self.name



class Dataset:

    def __init__(self, name, urls, format):
        self.name = name
        self.urls = urls
        self.format = format

    def save(self, path):
        pass


    def __repr__(self):
        return '{}'.format(self.name)
