import json;

with open("Tests_Python/AllPrintings.json", 'r',errors="ignore") as f:
    file = json.load(f)

id_saisi=input('Saisir ID : ')

for set_id in file["data"]:                                     # Vérification si le set contient des cartes
    if "cards" in file["data"][set_id]:                         # Parcours de chaque carte dans le set
        for card in file["data"][set_id]["cards"]:        # Accéder à la carte courante
            if card["uuid"] == id_saisi:                        # Affiche le nom de la carte correspondante
                print(f'Le nom de la carte est : {card["name"]}')
                break                                           # Sort de la boucle si la carte est trouvée
        else:
            continue                                            # Continue si aucune carte ne correspond dans ce set
        break                                                   # Sort de la boucle principale si la carte est trouvée
else:
    print("Carte non trouvée.")
