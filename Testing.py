"""
This File is used for testing imports and functionality of the package
"""
from DataAnalysis.Data import Data

data = Data("Test Data",{"A":[1,2,3,4,5,6,7,8,9],"B":[1,2,3,4,5],"C":[1,2,3,4,5]})

data.store_data_excel("TestData")