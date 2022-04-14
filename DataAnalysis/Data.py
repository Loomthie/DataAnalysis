import pandas as pd
import numpy as np
import xlsxwriter
from DataAnalysis.FileFormat import *


class Data:

    def __init__(self,title:str,vals:dict):
        self.mean = {}
        self.st_dev = {}
        self.title = title
        self.sub_data_sets = {}
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
        wb = xlsxwriter.Workbook(fname,options={"nan_inf_to_errors":True})
        ws = wb.add_worksheet("Complete Data Set")
        ws.write_row(row=0,col=0,data=['Title:',self.title])
        ws.write_row(row=2,col=0,data=[i for i in self.vals])
        for row in range(len(self.vals.iloc[:,1])):
            ws.write_row(row=row+3,col=0,data=[self.vals.iloc[row,:][key] for key in self.vals])
        for key in self.sub_data_sets:
            subData:Data
            subData = self.sub_data_sets[key]
            ws = wb.add_worksheet(key)
            ws.write_row(row=0,col=0,data=['Title:',subData.title])
            ws.write_row(row=2,col=0,data=[i for i in subData.vals])
            for row in range(len(subData.vals.iloc[:,1])):
                ws.write_row(row=row+3,col=0,data=[subData.vals.iloc[row,:][item] for item in subData.vals])
        wb.close()

    def tidy_merge(self,cols,newColKey:str, newColVal:str, include=True):
        new_df = {}
        for key in self.vals:
            if key in cols and include:
                continue
            if key not in cols and not include:
                continue
            new_df[key] = []
        new_df[newColKey] = []
        new_df[newColVal] = []

        for row in range(len(self.vals.iloc[:,1])):
            rowData = dict(self.vals.iloc[row,:])
            for key in rowData:
                if key in new_df:
                    continue
                new_df[newColKey].append(key)
                new_df[newColVal].append(rowData[key])
                for key2 in rowData:
                    if key2 in cols and include:
                        continue
                    elif key2 not in cols and not include:
                        continue
                    new_df[key2].append(rowData[key2])
        return Data(self.title,new_df)

    def create_subset(self,title,func):
        new_data = {}
        for key in self.vals:
            new_data[key] = []
        for row in self.vals.iloc:
            if func(row):
                for key in new_data:
                    new_data[key].append(row[key])
        self.sub_data_sets[title] = Data(title,new_data)
        return Data(title,new_data)







