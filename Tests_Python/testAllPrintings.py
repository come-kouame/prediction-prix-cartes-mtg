import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt   # data visualization
# import seaborn as sns # statistical data visualization
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import json



with open("AllPrintings.json", 'r') as f:
    file = json.load(f)

result= {}
result["meta"] = file["meta"]
result["data"] = {}




count = 0
for id in file["data"]:
    if count > 10:
        break
    count += 1
    print(file["data"][id]["cards"])
    result["data"][id] = {}
    if ("cards" in file["data"][id]):
        result["data"][id]["cards"] = file["data"][id]["cards"]


with open('AllPrintTest.json', 'w') as f:d
    json.dump(result, f, indent=4)


# ATTENTION : CERTAINS ATTRIBUTS SONT OBSOLETES (ex:hasFoil,hasNotFoil) SUR MTJSON "O"