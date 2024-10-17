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

resultsorted= {}
resultsorted["meta"] = file["meta"]
resultsorted["data"] = {}

for id in file["data"]:
    resultsorted["data"][id] = {}
    resultsorted["data"][id]["cards"] = {}
    totalSetCards = file["data"][id]["totalSetSize"]     # Nombre de cartes dans 1 Set
    if ("cards" in file["data"][id]):
        for card_count in range(totalSetCards) :        # on parcourt la liste de carte
            if ("uuid" in file["data"][id]["cards"][card_count] ):      
                resultsorted["data"][id]["cards"][card_count] = {}

                resultsorted["data"][id]["cards"][card_count]["uuid"] = file["data"][id]["cards"][card_count]["uuid"]

                resultsorted["data"][id]["cards"][card_count]["name"] = file["data"][id]["cards"][card_count]["name"]

                resultsorted["data"][id]["cards"][card_count]["extension"] = id 

                resultsorted["data"][id]["cards"][card_count]["rarity"] = file["data"][id]["cards"][card_count]["rarity"]
                
                resultsorted["data"][id]["cards"][card_count]["manaValue"] = file["data"][id]["cards"][card_count]["manaValue"]

                if ("artist" in file["data"][id]["cards"][card_count] ):
                    resultsorted["data"][id]["cards"][card_count]["artist"] = file["data"][id]["cards"][card_count]["artist"]

                if ("power" in file["data"][id]["cards"][card_count] ):
                    resultsorted["data"][id]["cards"][card_count]["power"] = file["data"][id]["cards"][card_count]["power"]

                if ("toughness" in file["data"][id]["cards"][card_count] ):
                    resultsorted["data"][id]["cards"][card_count]["toughness"] = file["data"][id]["cards"][card_count]["toughness"]
                
                if (file["data"][id]["cards"][card_count]["supertypes"] ):
                    resultsorted["data"][id]["cards"][card_count]["supertypes"] = file["data"][id]["cards"][card_count]["supertypes"]
                
                if (file["data"][id]["cards"][card_count]["types"] ):
                    resultsorted["data"][id]["cards"][card_count]["types"] = file["data"][id]["cards"][card_count]["types"]
                
                if (file["data"][id]["cards"][card_count]["subtypes"] ):
                    resultsorted["data"][id]["cards"][card_count]["subtypes"] = file["data"][id]["cards"][card_count]["subtypes"]


with open('AllPrintingsSorted.json', 'w') as f:
    json.dump(resultsorted, f, indent=4)


