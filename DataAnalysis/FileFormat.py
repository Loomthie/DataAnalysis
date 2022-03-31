import os
import pandas as pd

class Document:
    fileName = ""
    fileType = ""
    content = ""

    def __init__(self,content,**kwargs):
        self.content = content
        for key in kwargs:
            if key not in self.__dict__ and key not in Document.__dict__:
                raise AttributeError(f"{key} not a recognized element")
            self.__dict__[key] = kwargs[key]

    def get_binary(self):
        return self.fileName

    def save_file(self,path=os.getcwd()):
        print('save_file')
        wb = self.get_binary()
        with open(f'{path}/{self.fileName}{self.fileType}','wb') as file:
            file.write(bytes(wb,'utf-8'))


class ExcelFile(Document):
    fileType = ".xlsx"

    def save_file(self,path=os.getcwd()):
        self.content.to_excel(f"{path}/{self.fileName}{self.fileType}")
