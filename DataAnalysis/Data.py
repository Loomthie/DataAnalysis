import pandas as pd
import numpy as np
from DataAnalysis.FileFormat import *

class Data:
    title = ""
    vals = pd.DataFrame()
    mean = {}
    st_dev = {}

    def __init__(self,title:str,vals:dict):
        self.title = title
        max_length = max([len(vals[key]) for key in vals])
        for key in vals:
            while len(vals[key]) < max_length:
                vals[key].append(np.NaN)
        self.vals = pd.DataFrame(vals)
        for i in self.vals:
            self.mean[i] = 0
            self.st_dev[i] = 0
            n = 0
            for k in self.vals[i]:
                if pd.isna(k):
                    continue
                n += 1
                try:
                    self.mean[i] += k
                except TypeError:
                    self.mean[i] = "N/A"
                    break
            if self.mean[i] != "N/A":
                self.mean[i] /= n
                for k in self.vals[i]:
                    if pd.isna(k):
                        continue
                    self.st_dev[i] += (k-self.mean[i])**2
            else:
                self.st_dev[i] = "N/A"
            if self.st_dev[i] != "N/A":
                self.st_dev[i] /= n
                self.st_dev[i] **= 0.5

    def __repr__(self):
        mean_msg = "\n".join([f"\t{i} - {self.mean[i]}" for i in self.mean])
        st_dev_msg = "\n".join([f"\t{i} - {self.st_dev[i]}" for i in self.st_dev])
        return f'Title - {self.title}\n\n' \
               f'Means:\n' \
               f'{mean_msg}\n\n' \
               f'Standard Deviations:\n' \
               f'{st_dev_msg}'

    def store_data_excel(self,fname,path=None):
        doc = ExcelFile(self.vals,fileName=fname)
        if path is None:
            doc.save_file()
        else:
            doc.save_file(path=path)
