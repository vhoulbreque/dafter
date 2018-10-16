import os
import io
import zipfile

import requests

from utils import normalize_filename, normalize_name


class CSVDataset:

    def __init__(self, name, urls, save_path=None):
        self.name = normalize_name(name)
        self.urls = urls
        self.save_path = save_path

        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)

    def download(self):
        folder = os.path.join(self.save_path, self.name)
        if not os.path.exists(folder):
            os.makedirs(folder)

        for i, url in enumerate(self.urls):
            resp = requests.get(url)

            f_name = normalize_filename(url)
            if len(self.urls) > 1:
                f_name = f_name.split('.')
                f_name = '.'.join(f_name[0:-1]) + '_{}'.format(i) + '.' + f_name[-1]

            f_name = os.path.join(folder, f_name)

            with open(f_name, 'w') as f:
                f.write(resp.text)

    def __repr__(self):
        return self.name


class ZIPDataset:

    def __init__(self, name, urls, save_path=None):
        self.name = normalize_name(name)
        self.urls = urls
        self.save_path = save_path

        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)

    def download(self):
        folder = os.path.join(self.save_path, self.name)
        if not os.path.exists(folder):
            os.makedirs(folder)

        for i, url in enumerate(self.urls):
            r = requests.get(url, stream=True)
            z = zipfile.ZipFile(io.BytesIO(r.content))
            z.extractall(folder)

    def __repr__(self):
        return self.name


if __name__ == "__main__":

    colleges = CSVDataset("colleges", ["https://beachpartyserver.azurewebsites.net/VueBigData/DataFiles/Colleges.txt"], save_path="data")
    crimes = CSVDataset("crimes", ["https://data.lacity.org/api/views/y8tr-7khq/rows.csv?accessType=DOWNLOAD"], save_path="data")
    payments = ZIPDataset("payments", ["http://download.cms.gov/openpayments/PGYR13_P062918.ZIP"], save_path="data")
    salaries = CSVDataset("employee_salaries", ["https://data.montgomerycountymd.gov/api/views/xj3h-s2i7/rows.csv?accessType=DOWNLOAD"], save_path="data")
    journal = CSVDataset("journal_influence", ["https://github.com/FlourishOA/Data/raw/master/estimated-article-influence-scores-2015.csv"], save_path="data")
    medical_charge = ZIPDataset("medical_charge", ["https://www.cms.gov/Research-Statistics-Data-and-Systems/Statistics-Trends-and-Reports/Medicare-Provider-Charge-Data/Downloads/Inpatient_Data_2011_CSV.zip"], save_path="data")
    met_objects = CSVDataset("met_objects", ["https://github.com/metmuseum/openaccess/raw/master/MetObjects.csv"], save_path="data")
    midwest = CSVDataset("midwest_survey", ["https://raw.githubusercontent.com/fivethirtyeight/data/master/region-survey/MIDWEST.csv"], save_path="data")
    road_safety = ZIPDataset("road_safety", ["http://data.dft.gov.uk/road-accidents-safety-data/RoadSafetyData_2015.zip"], save_path="data")
    traffic_violations = CSVDataset("traffic_violations", ["https://data.montgomerycountymd.gov/api/views/4mse-ku6q/rows.csv?accessType=DOWNLOAD"], save_path="data")

    datasets = [colleges, crimes, payments, salaries, journal, medical_charge,
                met_objects, midwest, road_safety, traffic_violations]

    for d in datasets:
        print(d.name)
        d.download()
