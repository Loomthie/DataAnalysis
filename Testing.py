"""
This File is used for testing imports and functionality of the package
"""
from DataAnalysis.Data import Data
from DataAnalysis.HypothesisTests import TwoSampleT

set = Data('Two Sample Test', {'s1':[724,718,776,760,745,759,795,756,742,740,761,749,739,747,742],
                               's2':[735,775,729,755,783,760,738,780]})

print(set[0])