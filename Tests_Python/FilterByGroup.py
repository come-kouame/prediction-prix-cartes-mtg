import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt   # data visualization
# import seaborn as sns # statistical data visualization
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import json


with open("AllPrintingsSorted.json", 'r',errors="ignore") as f:
        file = json.load(f)


result= {}
result["meta"] = file["meta"]
result["data"] = {}

def filter_by_key(key, value): # Appeler "key" et "valeur" entre guillemets
        for uuid in file["data"]:
                if (key in file["data"][uuid]
                and value in file["data"][uuid][key] ):
                        if (key == "legalities"):
                                if (value in file["data"][uuid][key]):
                                        result["data"] = file["data"]
                        else:
                                result["data"] = file["data"][uuid]


#filter_by_key("subtypes" , "Human")
#filter_by_key("power" , "12")


with open("TestFilterByKey.json", 'w') as f:
        json.dump(result,f, indent=4)