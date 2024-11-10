import json

class Merger:
    all_prices = {}
    all_printings = {}
    tree = {}

    def __init__(self, all_prices_sorted_path : str, all_printings_sorted_path : str):
        with open(all_prices_sorted_path, 'r') as file:
            self.all_prices = json.load(file)
        with open(all_printings_sorted_path, 'r') as file:
            self.all_printings = json.load(file)

    def merge(self) -> None:
        self.tree = {}
        # Merge le champ 'meta'
        self.tree['meta'] = self.all_prices['meta']
        for m in self.all_printings['meta']:
            self.tree['meta'][m] = self.all_printings['meta'][m]
        # Merge le champ 'data'
        self.tree['data'] = self.all_prices['data']
        for id in self.all_printings['data']:
            if id in self.all_prices['data']:
                for f in self.all_printings['data'][id]:
                    self.tree['data'][id][f] = self.all_printings['data'][id][f]

    
    def save(self, output_path : str) -> None:
        with open(output_path, 'w') as file:
            file.write(json.dumps(self.tree, indent=4))
        

merger = Merger('AllPricesSorted.json', 'AllPrintingsSorted.json')

merger.merge()

merger.save('merged.json')