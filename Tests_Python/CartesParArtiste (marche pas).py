import json

with open("data/AllPrintings.json", 'r',errors="ignore") as f:
    file = json.load(f)

artist_input=input('Saisir artiste : ')
found_ids=[]


for set_id in file["data"]:
    totalCards = file["data"][set_id]["totalSetSize"]
    if "cards" in file["data"][set_id]:                         # Vérification si le set contient des cartes
        for card in range(totalCards):              # Parcours de chaque carte dans le set
            if "artist" in file["data"][set_id]["cards"]:
                if file["data"][set_id]["cards"][card]["artist"] == artist_input:
                    found_ids.append(card["uuid"])

if found_ids:
    print(f'Les cartes correspondants au nom "{artist_input}" sont :')
    for card_id in found_ids:
        print(card_id)
else:
    print("Aucune carte trouvée avec ce nom.")