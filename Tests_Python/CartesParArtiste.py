import json

with open("data/AllPrintings.json", 'r',errors="ignore") as f:
    file = json.load(f)

artist_input=input('Saisir artiste : ')
found_ids=[]


# Parcours de tous les sets
for set_id in file["data"]:
    # Vérification si le set contient des cartes
    if "cards" in file["data"][set_id]:
        # Parcours de chaque carte dans le set
        for card in file["data"][set_id]["cards"]:
            if "artist" in card and card["artist"] == artist_input:
                found_ids.append(card["uuid"])

if found_ids:
    print(f'Les cartes correspondants au nom "{artist_input}" sont :')
    for card_id in found_ids:
        print(card_id)
else:
    print("Aucune carte trouvée avec ce nom.")