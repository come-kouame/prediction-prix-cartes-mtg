import json

class MTGFile:
    tree = {}

    def __init__(self, *, all_prices_path:str=None, all_printings_path:str=None, merged_file:str=None):
        if all_prices_path != None and all_printings_path != None and merged_file == None:
            all_prices = self.__get_all_prices(all_prices_path)
            all_printings = self.__get__all_printings(all_printings_path)
            keys = list(all_prices.keys())
            count = 1
            for i in range(len(keys)):
                uuid = keys[i]
                if uuid in all_prices:
                    if uuid not in all_printings:
                        all_prices.pop(uuid)
                    else:
                        for k in all_printings[uuid]:
                            all_prices[uuid][k] = all_printings[uuid][k]
                        all_prices[uuid]['uuid'] = uuid
                        all_prices[count] = all_prices.pop(uuid)
                        count += 1
            self.tree = all_prices
        elif all_prices_path == None and all_printings_path == None and merged_file != None:
            with open(merged_file, 'r') as f:
                mg = json.load(f)
            self.tree = mg
        else:
            raise ValueError('Erreur de paramètre')

    def __get_all_prices(self, all_prices_path:str):
        with open(all_prices_path, 'r') as f:
            ap = json.load(f)
        all_prices = {}
        for id in ap['data']:
            if 'paper' in ap['data'][id] and 'cardkingdom' in ap['data'][id]['paper'] and 'retail' in ap['data'][id]['paper']['cardkingdom']:
                all_prices[id] = {}
                all_prices[id]['prices'] = {}

                if 'normal' in ap['data'][id]['paper']['cardkingdom']['retail']:
                    all_prices[id]['prices']['normal'] = ap['data'][id]['paper']['cardkingdom']['retail']['normal']
                
                if 'foil' in ap['data'][id]['paper']['cardkingdom']['retail']:
                    all_prices[id]['prices']['foil'] = ap['data'][id]['paper']['cardkingdom']['retail']['foil']

                if 'etched' in ap['data'][id]['paper']['cardkingdom']['retail']:
                    all_prices[id]['prices']['etched'] = ap['data'][id]['paper']['cardkingdom']['retail']['etched']
        return all_prices

    def __get__all_printings(self, all_printings_path:str):
        with open(all_printings_path, 'r',errors="ignore") as f:
            ap = json.load(f)
        prints = {}
        for id in ap['data']:
            totalSetCards = ap['data'][id]['totalSetSize']
            if 'cards' in ap['data'][id]:
                for card_count in range(totalSetCards):
                    if 'uuid' in ap['data'][id]['cards'][card_count]:
                        uuid = ap['data'][id]['cards'][card_count]['uuid']
                        prints[uuid] = {}
                        prints[uuid]['name'] = ap['data'][id]['cards'][card_count]['name']
                        prints[uuid]['extension'] = id
                        prints[uuid]['releaseDate'] = ap['data'][id]['releaseDate']
                        prints[uuid]["rarity"] = ap["data"][id]["cards"][card_count]["rarity"]
                
                        prints[uuid]["manaValue"] = ap["data"][id]["cards"][card_count]["manaValue"]

                        if ("artist" in ap["data"][id]["cards"][card_count] ):
                            prints[uuid]["artist"] = ap["data"][id]["cards"][card_count]["artist"]

                        if ("power" in ap["data"][id]["cards"][card_count] ):
                            prints[uuid]["power"] = ap["data"][id]["cards"][card_count]["power"]

                        if ("toughness" in ap["data"][id]["cards"][card_count] ):
                            prints[uuid]["toughness"] = ap["data"][id]["cards"][card_count]["toughness"]
                        
                        if (ap["data"][id]["cards"][card_count]["supertypes"] ):
                            prints[uuid]["supertypes"] = ap["data"][id]["cards"][card_count]["supertypes"]
                        
                        if (ap["data"][id]["cards"][card_count]["types"] ):
                            prints[uuid]["types"] = ap["data"][id]["cards"][card_count]["types"]
                        
                        if (ap["data"][id]["cards"][card_count]["subtypes"] ):
                            prints[uuid]["subtypes"] = ap["data"][id]["cards"][card_count]["subtypes"]
                            
                        if (ap["data"][id]["cards"][card_count]["legalities"] ):
                            prints[uuid]["legalities"] = ap["data"][id]["cards"][card_count]["legalities"]

        return prints

    def save(self, path:str) -> None:
        with open(path, 'w') as file:
            file.write(json.dumps(self.tree, indent=4))

mtgf = MTGFile(all_prices_path='Data/AllPrices.json', all_printings_path='Data/AllPrintings.json')
mtgf.save('merged_file.json')
