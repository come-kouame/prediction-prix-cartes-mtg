import json

with open("data/AllPrintings.json", 'r',errors="ignore") as f:
    file = json.load(f)

card_input=input('Saisir carte : ')
found_ids=[]


for set_id in file["data"]:                                     
    if "cards" in file["data"][set_id]:                         # Vérification si le set contient des cartes
        for card in file["data"][set_id]["cards"]:              # Parcours de chaque carte dans le set
            if card["name"] == card_input:                      # Accéder à la carte courante
                found_ids.append(card["uuid"])

if found_ids:
    print(f'Les identifiants des cartes correspondants au nom "{card_input}" sont :')
    for card_id in found_ids:
        print(card_id)
else:
    print("Aucune carte trouvée avec ce nom.")