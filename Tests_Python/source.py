import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

#Ouvrir le fichier json contenant tous les prix
with open(r"mtgo_cardhoarder_retail_normal.json", 'r') as f:
    file = json.load(f)

i = 0
result = {}
result["meta"] = file["meta"]
result["meta"]["price_format"] = "mtgo"
result["meta"]["seller"] = "cardhoarder"
result["meta"]["price_list"] = "retail"
result["meta"]["price_point"] = "normal"
result["data"] = {}
for id in file["data"]:
    if ("mtgo" in file["data"][id] 
        and "cardhoarder" in file["data"][id]["mtgo"]
        and "retail" in file["data"][id]["mtgo"]["cardhoarder"]
        and "normal" in file["data"][id]["mtgo"]["cardhoarder"]["retail"]):
            result["data"][id] = {}
            #Ajouter les prix
            result["data"][id]["prices"] = file["data"][id]["mtgo"]["cardhoarder"]["retail"]["normal"]
            #Ajouter la monaie
            result["data"][id]["currency"] = file["data"][id]["mtgo"]["cardhoarder"]["currency"]
            #Ajouter le taux de variation de la courbe
            prices = list(result["data"][id]["prices"].values())
            tx_var = 0
            for i in range(1, len(prices)):
                 tx_var += abs(prices[i] - prices[i - 1])
            result["data"][id]["tx_var"] = tx_var



#Créer le fichier json de sortie
with open('mtgo_cardhoarder_retail_normal.json', 'w') as f:
    json.dump(result, f, indent=4)
