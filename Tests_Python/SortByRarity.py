import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt   # data visualization
# import seaborn as sns # statistical data visualization
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import json



with open("AllPrintings.json", 'r',errors="ignore") as f:
    file = json.load(f)



resultrarity= {}
resultrarity["meta"] = file["meta"]
resultrarity["data"] = {}

for id in file["data"]:
    resultrarity["data"][id] = {}
    resultrarity["data"][id]["mythic"] = {}
    resultrarity["data"][id]["rare"] = {}
    resultrarity["data"][id]["uncommon"] = {}
    resultrarity["data"][id]["common"] = {}
    totalSetCards = file["data"][id]["totalSetSize"]     # Nombre de cartes dans 1 Set
    if ("cards" in file["data"][id]):
        for card_count in range(totalSetCards) :        # on parcourt la liste de carte
            if ("rarity" in file["data"][id]["cards"][card_count] 
            and "common" == file["data"][id]["cards"][card_count]["rarity"] ):      
                resultrarity["data"][id]["common"][card_count] = {}
                resultrarity["data"][id]["common"][card_count]["name"] = file["data"][id]["cards"][card_count]["name"]
                resultrarity["data"][id]["common"][card_count]["rarity"] = file["data"][id]["cards"][card_count]["rarity"]
                resultrarity["data"][id]["common"][card_count]["uuid"] = file["data"][id]["cards"][card_count]["uuid"]
            elif ("rarity" in file["data"][id]["cards"][card_count] 
            and "uncommon" == file["data"][id]["cards"][card_count]["rarity"] ):
                resultrarity["data"][id]["uncommon"][card_count] = {}
                resultrarity["data"][id]["uncommon"][card_count]["name"] = file["data"][id]["cards"][card_count]["name"]
                resultrarity["data"][id]["uncommon"][card_count]["rarity"] = file["data"][id]["cards"][card_count]["rarity"]
                resultrarity["data"][id]["uncommon"][card_count]["uuid"] = file["data"][id]["cards"][card_count]["uuid"]
            elif ("rarity" in file["data"][id]["cards"][card_count] 
            and "rare" == file["data"][id]["cards"][card_count]["rarity"] ):
                resultrarity["data"][id]["rare"][card_count] = {}
                resultrarity["data"][id]["rare"][card_count]["name"] = file["data"][id]["cards"][card_count]["name"]
                resultrarity["data"][id]["rare"][card_count]["rarity"] = file["data"][id]["cards"][card_count]["rarity"]
                resultrarity["data"][id]["rare"][card_count]["uuid"] = file["data"][id]["cards"][card_count]["uuid"]
            elif ("rarity" in file["data"][id]["cards"][card_count] 
            and "mythic" == file["data"][id]["cards"][card_count]["rarity"] ):
                resultrarity["data"][id]["mythic"][card_count] = {}
                resultrarity["data"][id]["mythic"][card_count]["name"] = file["data"][id]["cards"][card_count]["name"]
                resultrarity["data"][id]["mythic"][card_count]["rarity"] = file["data"][id]["cards"][card_count]["rarity"]
                resultrarity["data"][id]["mythic"][card_count]["uuid"] = file["data"][id]["cards"][card_count]["uuid"]
                
                    



with open('SortByRarity.json', 'w') as f:
    json.dump(resultrarity, f, indent=4)