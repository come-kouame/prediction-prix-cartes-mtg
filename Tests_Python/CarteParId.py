import json;

with open("data/AllPrintings.json", 'r',errors="ignore") as f:
    file = json.load(f)

id_input=input('Saisir ID : ')

for set_id in file["data"]:                                         
    if "cards" in file["data"][set_id]:                             # Vérification si le set contient des cartes
        for card in file["data"][set_id]["cards"]:                  # Parcours de chaque carte dans le set
            if card["uuid"] == id_input:                            # Accéder à la carte courante
                print(f'Le nom de la carte est : {card["name"]}')   # Affiche le nom de la carte correspondante
                break                                               # Sort de la boucle si la carte est trouvée
        else:
            continue                                                # Continue si aucune carte ne correspond dans ce set
        break                                                       # Sort de la boucle principale si la carte est trouvée
else:
    print("Carte non trouvée.")
