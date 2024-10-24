import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt   # data visualization
# import seaborn as sns # statistical data visualization
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import json


with open("AllPrintingsSorted.json", 'r',errors="ignore") as f:
        file = json.load(f);


result= {}
result["meta"] = file["meta"]
result["data"] = {}

def filter_by_key(key, value):
        print(1)
        for id in file["data"]:
                result["data"][id] = {}
                result["data"][id]["cards"] = {}
                totalSetCards = file["data"][id]["totalSetSize"]  
                for card_count in range(totalSetCards) :       
                        if (key in file["data"][id]["cards"][card_count] 
                        and value in file["data"][id]["cards"][card_count][key] ):      
                                result["data"][id]["cards"][card_count] = {}              