import json

class AllPricesSorter:
    tree = {}
    def __init__(self, all_prices_path : str):
        with open(all_prices_path, 'r') as file:
            f = json.load(file)
        self.tree = {}
        self.tree['meta'] = {}
        self.tree['meta']['seller'] = 'cardkingdom'
        self.tree['data'] = {}
        # Réaranger le fichier
        for id in f['data']:
            if ('paper' in f['data'][id] and
                'cardkingdom' in f['data'][id]['paper'] and
                'retail' in f['data'][id]['paper']['cardkingdom']):
                data = f['data'][id]['paper']['cardkingdom']['retail']
                self.tree['data'][id] = {}
                self.tree['data'][id]['prices'] = {}
                if 'normal' in data:
                    self.tree['data'][id]['prices']['normal'] = data['normal']
                if 'foil' in data:
                    self.tree['data'][id]['prices']['foil'] = data['foil']
                if 'etched' in data:
                    self.tree['data'][id]['prices']['etched'] = data['etched']


    def save(self, output_path : str) -> None :
        with open(output_path, 'w') as file:
            file.write(json.dumps(self.tree, indent=4))

    def normalize_prices(self) -> None:
        for id in self.tree['data']:
            for t in self.tree['data'][id]['prices']:
                dates = list(self.tree['data'][id]['prices'][t].keys())
                prices = list(self.tree['data'][id]['prices'][t].values())

                rst = {}

                for p in range(1, len(prices)):
                    rst[dates[p]] = (prices[p] - prices[p - 1]) / (prices[p] + prices[p - 1])
                self.tree['data'][id]['prices'][t] = rst
            


    def keep_price_variations(self, accumulator_func, check_func) -> None:
        tree = {}
        for id in self.tree['data']:
            prices = self.tree['data'][id]['prices']
            
            if 'normal' in prices:
                vals = list(prices['normal'].values())
                rst = accumulator_func(vals)
                if check_func(rst) == False:
                    del self.tree['data'][id]['prices']['normal']
            if 'foil' in prices:
                vals = list(prices['foil'].values())
                rst = accumulator_func(vals)
                if check_func(rst) == False:
                    del self.tree['data'][id]['prices']['foil']
            if 'etched' in prices:
                vals = list(prices['etched'].values())
                rst = accumulator_func(vals)
                if check_func(rst) == False:
                    del self.tree['data'][id]['prices']['etched']
            
            if len(self.tree['data'][id]['prices']) > 0:
                tree[id] = self.tree['data'][id]
        self.tree['data'] = tree
    


sorter = AllPricesSorter("Data/AllPrices.json")

sorter.normalize_prices()

sorter.keep_price_variations(lambda prices : sum(abs(p) for p in prices), lambda result : result > 0)

sorter.save("result.json")