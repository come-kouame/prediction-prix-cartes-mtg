import json;

with open("data/AllPrintings.json", 'r',errors="ignore") as f:
    file = json.load(f)

id_input=input('Saisir ID : ')

for set_id in file["data"]:                                     # Vérification si le set contient des cartes
    if "cards" in file["data"][set_id]:                         # Parcours de chaque carte dans le set
        for card in file["data"][set_id]["cards"]:              # Accéder à la carte courante
            if card["uuid"] == id_input:                        # Affiche le nom de la carte correspondante
                print(f"Le nom de l'artiste est : {card["artist"]}")
                break                                           # Sort de la boucle si la carte est trouvée
        else:
            continue                                            # Continue si aucun artiste ne correspond dans ce set
        break                                                   # Sort de la boucle principale si l'artiste est trouvé
else:
    print("Artiste non trouvé.")