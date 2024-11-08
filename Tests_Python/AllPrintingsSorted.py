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
    totalSetCards = file["data"][id]["totalSetSize"]
    if ("cards" in file["data"][id]):
        for card_count in range(totalSetCards) :        # on parcourt la liste de carte
            if ("uuid" in file["data"][id]["cards"][card_count] ):      
                uuid = file["data"][id]["cards"][card_count]["uuid"]
                resultsorted["data"][uuid] = {}

                resultsorted["data"][uuid]["name"]  = file["data"][id]["cards"][card_count]["name"]

                resultsorted["data"][uuid]["extension"] = id 

                resultsorted["data"][uuid]["releaseDate"] = file["data"][id]["releaseDate"]

                resultsorted["data"][uuid]["rarity"] = file["data"][id]["cards"][card_count]["rarity"]
                
                resultsorted["data"][uuid]["manaValue"] = file["data"][id]["cards"][card_count]["manaValue"]

                if ("artist" in file["data"][id]["cards"][card_count] ):
                    resultsorted["data"][uuid]["artist"] = file["data"][id]["cards"][card_count]["artist"]

                if ("power" in file["data"][id]["cards"][card_count] ):
                    resultsorted["data"][uuid]["power"] = file["data"][id]["cards"][card_count]["power"]

                if ("toughness" in file["data"][id]["cards"][card_count] ):
                    resultsorted["data"][uuid]["toughness"] = file["data"][id]["cards"][card_count]["toughness"]
                
                if (file["data"][id]["cards"][card_count]["supertypes"] ):
                    resultsorted["data"][uuid]["supertypes"] = file["data"][id]["cards"][card_count]["supertypes"]
                
                if (file["data"][id]["cards"][card_count]["types"] ):
                    resultsorted["data"][uuid]["types"] = file["data"][id]["cards"][card_count]["types"]
                
                if (file["data"][id]["cards"][card_count]["subtypes"] ):
                    resultsorted["data"][uuid]["subtypes"] = file["data"][id]["cards"][card_count]["subtypes"]
                    
                if (file["data"][id]["cards"][card_count]["legalities"] ):
                    resultsorted["data"][uuid]["legalities"] = file["data"][id]["cards"][card_count]["legalities"]


with open('AllPrintingsSorted.json', 'w') as f:
    json.dump(resultsorted, f, indent=4)

