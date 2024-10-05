import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt   # data visualization
# import seaborn as sns # statistical data visualization
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import json



with open("AllPrintings.json", 'r',errors="ignore") as f:
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
    if ("cards" in file["data"][id]):       # On extrait les 10 premieres extensions pour l'instant
        result["data"][id]["cards"] = file["data"][id]["cards"]     # on remplit les cartes dans le fichier créé


with open('AllPrintTest.json', 'w') as f:
    json.dump(result, f, indent=4)


result1= {}
result1["meta"] = file["meta"]
result1["data"] = {}

deck_count = 0
for id in file["data"]:
    if deck_count > 10:
        break
    deck_count += 1
    result1["data"][id] = {}
    result1["data"][id]["cards"] = {}
    totalSetCards = file["data"][id]["totalSetSize"]        # Nombre de cartes dans 1 Set
    if ("cards" in file["data"][id]):
        for card_count in range(totalSetCards) :        # on parcourt la liste de carte
            if ("finishes" in file["data"][id]["cards"][card_count] 
            and "foil" in file["data"][id]["cards"][card_count]["finishes"] ):      # Pour savoir si la carte a une version foil utiliser "finishes". 
                result1["data"][id]["cards"][card_count] = file["data"][id]["cards"][card_count]["uuid"]      # on remplit seulement avec les cartes foil 
        


with open('AllFoils.json', 'w') as f:
    json.dump(result1, f, indent=4)


# ATTENTION : CERTAINS ATTRIBUTS SONT OBSOLETES (ex:hasFoil,hasNotFoil) SUR MTJSON "O"