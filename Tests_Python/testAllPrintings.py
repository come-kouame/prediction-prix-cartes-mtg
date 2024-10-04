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
    result["data"][id] = {}
    if ("cards" in file["data"][id]): # On extrait les 10 premieres extensions pour l'instant
        result["data"][id]["cards"] = file["data"][id]["cards"]


with open('AllPrintTest.json', 'w') as f:d
    json.dump(result, f, indent=4)


# ATTENTION : CERTAINS ATTRIBUTS SONT OBSOLETES (ex:hasFoil,hasNotFoil) SUR MTJSON "O"
# Pour savoir si la carte a une version foil utiliser "finishes". 