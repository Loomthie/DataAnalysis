print("Testing")
from DataAnalysis.Data import Data

data = {"A":[1,2,3,4,5],"B":[1,2,3,4],"C":[1,2,3,4,5,6]}
dataset = Data("Compnent Values",data)
dataset.store_data_excel("TestingSpreadsheet")


