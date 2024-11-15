import json
from datetime import datetime, timedelta

class MTGFiles:
    tree = {}       # Contient le fichier fusionné

    #region Contructeur
    def __init__(self, *, all_printings_path : str = None, all_prices_path : str = None, merged_path : str = None):
        if all_printings_path != None and all_prices_path != None and merged_path == None:
            with open(all_printings_path, 'r', errors='ignore') as f:
                all_printings_raw = json.load(f)

            with open(all_prices_path, 'r', errors='ignore') as f_:
                all_prices_raw = json.load(f_)

            all_printings = self.__all_printings_sorting(all_prices_raw)
            all_prices = self.__all_prices_sorting(all_prices_raw)
            self.tree = self.__merge(all_prices, all_printings)
        elif all_printings_path == None and all_prices_path == None and merged_path != None:
            with open(merged_path, 'r', errors='ignore') as f:
                self.tree = json.load(f)
        else:
            raise ValueError('Les arguments possibles sont (AllPrintings.json et AllPrices.json) ou (Merged.json)')
        # Ajouter le champ 'is_normalized' dans 'meta' qui indique si les prix sont normalisés ou non
        self.tree['meta']['is_normalized'] = False
        
    def __all_printings_sorting(self, ap):

        resultsorted= {}
        resultsorted["meta"] = ap["meta"]
        resultsorted["data"] = {}

        for id in ap["data"]:
            if ("cards" in ap["data"][id]):
                for card_count in range(totalSetCards) :        # on parcourt la liste de carte
                    if ("uuid" in ap["data"][id]["cards"][card_count] ):      
                        uuid = ap["data"][id]["cards"][card_count]["uuid"]
                        resultsorted["data"][uuid] = {}

                        resultsorted["data"][uuid]["name"]  = ap["data"][id]["cards"][card_count]["name"]

                        resultsorted["data"][uuid]["extension"] = id 

                        resultsorted["data"][uuid]["releaseDate"] = ap["data"][id]["releaseDate"]

                        resultsorted["data"][uuid]["rarity"] = ap["data"][id]["cards"][card_count]["rarity"]
                        
                        resultsorted["data"][uuid]["manaValue"] = ap["data"][id]["cards"][card_count]["manaValue"]

                        if ("artist" in ap["data"][id]["cards"][card_count] ):
                            resultsorted["data"][uuid]["artist"] = ap["data"][id]["cards"][card_count]["artist"]

                        if ("power" in ap["data"][id]["cards"][card_count] ):
                            resultsorted["data"][uuid]["power"] = ap["data"][id]["cards"][card_count]["power"]

                        if ("toughness" in ap["data"][id]["cards"][card_count] ):
                            resultsorted["data"][uuid]["toughness"] = ap["data"][id]["cards"][card_count]["toughness"]
                        
                        if (ap["data"][id]["cards"][card_count]["supertypes"] ):
                            resultsorted["data"][uuid]["supertypes"] = ap["data"][id]["cards"][card_count]["supertypes"]
                        
                        if (ap["data"][id]["cards"][card_count]["types"] ):
                            resultsorted["data"][uuid]["types"] = ap["data"][id]["cards"][card_count]["types"]
                        
                        if (ap["data"][id]["cards"][card_count]["subtypes"] ):
                            resultsorted["data"][uuid]["subtypes"] = ap["data"][id]["cards"][card_count]["subtypes"]
                            
                        if (ap["data"][id]["cards"][card_count]["legalities"] ):
                            resultsorted["data"][uuid]["legalities"] = ap["data"][id]["cards"][card_count]["legalities"]
        return resultsorted
    
    def __all_prices_sorting(self, ap):
        rst = {}
        rst['meta'] = {}
        rst['meta']['seller'] = 'cardkingdom'
        rst['data'] = {}
        # Réaranger le fichier
        for id in ap['data']:
            if ('paper' in ap['data'][id] and
                'cardkingdom' in ap['data'][id]['paper'] and
                'retail' in ap['data'][id]['paper']['cardkingdom']):
                data = ap['data'][id]['paper']['cardkingdom']['retail']
                rst['data'][id] = {}
                rst['data'][id]['cards'] = {}
                if 'normal' in data:
                    rst['data'][id]['cards']['normal'] = {}
                    rst['data'][id]['cards']['normal']['is_cste'] = None
                    rst['data'][id]['cards']['normal']['prices'] = data['normal']
                if 'foil' in data:
                    rst['data'][id]['cards']['foil'] = {}
                    rst['data'][id]['cards']['foil']['is_cste'] = None
                    rst['data'][id]['cards']['foil']['prices'] = data['foil']
                if 'etched' in data:
                    rst['data'][id]['cards']['etched'] = {}
                    rst['data'][id]['cards']['etched']['is_cste'] = None
                    rst['data'][id]['cards']['etched']['prices'] = data['etched']
        return rst

    def __merge(self, prices, prints):
        tree = {}
        # Merge le champ 'meta'
        tree['meta'] = prices['meta']
        for m in prints['meta']:
            tree['meta'][m] = prints['meta'][m]
        # Merge le champ 'data'
        tree['data'] = prices['data']
        for id in prints['data']:
            if id in prices['data']:
                for f in prints['data'][id]:
                    tree['data'][id][f] = prints['data'][id][f]
        return tree
    #endregion

    # Sauvegarder l'état actuel du ficheir
    def save(self, output_path : str) -> None:
        """Sauvegarde du fichier actuel"""
        with open(output_path, 'w') as file:
            file.write(json.dumps(self.tree, indent=4))

    # Récupère la première date enregistrée dans le prix de chaque carte
    def first_date(self) -> datetime:
        """Récupère la première date enregistrée dans le prix de chaque carte"""
        min_date = datetime.today()
        for id in self.tree['data']:
            for ct in self.tree['data'][id]['cards']:
                dates = list(self.tree['data'][id]['cards'][ct]['prices'].keys())
                dates_converties = [datetime.strptime(date, "%Y-%m-%d") for date in dates]
                md = min(dates_converties)
                if md < min_date:
                    min_date = md
        return min_date
    
    # Récupère la dernière date enregistrée dans le prix de chaque carte
    def last_date(self) -> datetime:
        """Récupère la dernière date enregistrée dans le prix de chaque carte"""
        max_date = datetime(1900, 1, 1)
        for id in self.tree['data']:
            for ct in self.tree['data'][id]['cards']:
                dates = list(self.tree['data'][id]['cards'][ct]['prices'].keys())
                dates_converties = [datetime.strptime(date, "%Y-%m-%d") for date in dates]
                md = max(dates_converties)
                if md > max_date:
                    max_date = md
        return max_date

    # Complète les dates manquantes
    def complete_missing_dates(self) -> None:
        """
        Complète les dates manquantes dans les prix de chaque carte
        """
        if self.tree['meta']['is_normalized']:
            raise ValueError("Des dates ne peuvent pas être ajoutés lorsqu'elles sont normalisées")
        # Compléter les dates de la première à la dernière pour chaque carte
        fd = self.first_date().date()
        ld = self.last_date().date()

        dates = []
        this_day = fd
        while this_day <= ld:
            dates.append(str(this_day))
            this_day += timedelta(days=1)
        
        for id in self.tree['data']:
            for ct in self.tree['data'][id]['cards']:
                for d in dates:
                    if d not in self.tree['data'][id]['cards'][ct]['prices']:
                        self.tree['data'][id]['cards'][ct]['prices'][d] = 0.0
    

        


        
        

mtgf = MTGFiles(merged_path='result.json')
mtgf.complete_missing_dates()
mtgf.save('result.json')
