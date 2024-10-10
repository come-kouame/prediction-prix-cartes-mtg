import matplotlib.pyplot as plt
from enum import Enum
import json
import numpy as np

#region Classes & Enums
class Products(Enum):
    ALL = 0
    MTGO = "mtgo"
    PAPER = "paper"

class Sellers(Enum):
    ALL = 0
    CARD_HOARDER = "cardhoarder"
    CARD_KINGDOM = "cardkingdom"
    CARD_MARKET = "cardmarket"
    CARD_SHPERE = "cardsphere"
    TGC_PLAYER = "  "

class CardTypes(Enum):
    ALL = 0
    NORMAL = "normal"
    FOIL = "foil"
    ETCHED = "etched"


class AllPricesSorter:
    tree = {}

    # Prend en argument le chemin de AllPrices.json
    def __init__(self, all_prices_path : str):
        with open(all_prices_path, 'r') as file:
            raw_json = json.load(file)
            self.__change_to_tree(raw_json)

    # Changer l'architecture du fichier pour le rendre plus manipulable
    # Doit être appelé quand le fichier AllPrices n'a pas encore été modifié
    def __change_to_tree(self, raw_json) -> None:
        print(type(raw_json))
        self.tree = {}      #Réinitialiser tree
        index = 0
        raw_json = raw_json['data']
        for id in raw_json:
            for product in raw_json[id]:
                for seller in raw_json[id][product]:
                    if 'retail' in raw_json[id][product][seller]:
                        for cardtype in raw_json[id][product][seller]['retail']:
                            self.tree[index] = {}
                            self.tree[index]['uuid'] = id
                            self.tree[index]['product'] = product
                            self.tree[index]['seller'] = seller
                            self.tree[index]['cardtype'] = cardtype
                            self.tree[index]['currency'] = raw_json[id][product][seller]['currency']
                            self.tree[index]['prices'] = raw_json[id][product][seller]['retail'][cardtype]
                            index += 1

    # Compte le nombre de carte qui correspond aux différents filtres product-seller-cardtype
    def count(self, filter : list[(Products, Sellers, CardTypes)]) -> list[int]:
        rst = [0] * len(filter)
        
        for i in self.tree:
            for f in range(len(filter)):
                fproduct : Products = filter[f][0]
                fseller : Sellers = filter[f][1]
                fcardtype : CardTypes = filter[f][2]

                cproduct : str = self.tree[i]['product']
                cseller : str = self.tree[i]['seller']
                ccardtype : str = self.tree[i]['cardtype']

                product_correspond : bool = (fproduct == Products.ALL) or (fproduct.value == cproduct)
                seller_correspond : bool = (fseller == Sellers.ALL) or (fseller.value == cseller)
                cardtype_correspond : bool = (fcardtype == CardTypes.ALL) or (fcardtype.value == ccardtype)

                rst[f] += int(product_correspond and seller_correspond and cardtype_correspond)
        
        return rst

    # Filtre les cartes en ne laissant uniquement les cartes validant le filtre product-seller-cardtype
    def filter(self, product : Products, seller : Sellers, cardtype : CardTypes) -> None:
        rst = {}

        for i in self.tree:
            cproduct : str = self.tree[i]['product']
            cseller : str = self.tree[i]['seller']
            ccardtype : str = self.tree[i]['cardtype']

            product_correspond : bool = (product == Products.ALL) or (product.value == cproduct)
            seller_correspond : bool = (seller == Sellers.ALL) or (seller.value == cseller)
            cardtype_correspond : bool = (cardtype == CardTypes.ALL) or (cardtype.value == ccardtype)            

            if product_correspond and seller_correspond and cardtype_correspond:
                rst[i] = self.tree[i]
        self.tree = rst
        # self.__write_file()

    # Normalize l'évolution des prix entre -1 et 1 entre 2 jour
    def normalize_prices(self) -> None:
        for i in self.tree:
            dates = list(self.tree[i]['prices'].keys())
            prices = list(self.tree[i]['prices'].values())

            rst = {}

            for p in range(1, len(prices)):
                rst[dates[p]] = (prices[p] - prices[p - 1]) / (prices[p] + prices[p - 1])
            self.tree[i]['prices'] = rst
    
    # Ecrit le json en cours dans un fichier 'test.json'
    def write_file(self):
        with open('test.json', 'w') as file:
            file.write(json.dumps(self.tree, indent=4))

    def get_tree(self):
        return self.tree
    
    # Pour chaque carte, applique la fonctione accumulator_func sur les variations de prix de la carte
    # Le résultat de cette fonction sera vérifée grâce à la fonction booleenne check_func
    # Si cette dernière renvoie True, la carte est gardée
    def keep_price_variations(self, accumulator_func, check_func) -> None:
        rst = {}
        for i in self.tree:
            prices = list(self.tree[i]['prices'].values())
            result = accumulator_func(prices)
            if check_func(result):
                rst[i] = self.tree[i]
        self.tree = rst

    # Retourne le rang de chaque élément de la liste en paramètre (pour la corélation de Spearman)
    def __rank(self, elements : list) -> list[int]:
        #On trie la liste en gardant les indices originaux
        sorted_list = sorted(range(len(elements)), key=lambda x : elements[x])

        #Créer une liste pour les rangs
        ranks = [0] * len(elements)

        #Assigner le rang à chaque element
        for i, idx in enumerate(sorted_list):
            ranks[idx] = i

        return ranks
    
    # Calcul du coefficient de corélation de spearman pour les deux listes en paramètre
    def __spearman_corelation(self, prices_1 : list, prices_2 : list):
        if len(prices_1) != len(prices_2):
            raise Exception("Les deux cartes n'ont pas le même nombre d'échantillons de prix")
        
        #Récupérer les rangs des lists en paramètre
        rank_1 = self.__rank(prices_1)
        rank_2 = self.__rank(prices_2)

        # Calculer le coefficient de corélation de spearman
        n = len(prices_1)
        np1 = np.array(rank_1)
        np2 = np.array(rank_2)
        sum_squared = np.sum((np1 - np2) * (np1 - np2))
        spearman = 1 - (6 * sum_squared) / (n * (n * n - 1))

        return spearman
    
    # Calcul le coefficient de spearman pour chaque pair de carte
    def process_spearman(self, output_filename : str) -> None:
        rst = {}
        ids = list(self.tree.keys())
        for i in range(len(ids)):
            price_list_1 = list(self.tree[ids[i]]['prices'].values())
            uuid_1 = self.tree[ids[i]]['uuid']
            rst[uuid_1] = {}
            for j in range(1, len(ids)):
                price_list_2 = list(self.tree[ids[j]]['prices'].values())
                uuid_2 = self.tree[ids[j]]['uuid']
                # Caluler le coefficient de corélation de spearman
                try:
                    sc = self.__spearman_corelation(price_list_1, price_list_2)
                    rst[uuid_1][uuid_2] = sc
                except:
                    pass
        with open(output_filename, 'w') as file:
            file.write(json.dumps(rst, indent=4))

#endregion


all_prices_sorter = AllPricesSorter("AllPrices.json")
# counts1 = all_prices_sorter.count([(Products.ALL, Sellers.ALL, CardTypes.ALL)])
# counts2 = all_prices_sorter.count([(Products.ALL, Sellers.ALL, CardTypes.ALL), (Products.ALL, Sellers.CARD_KINGDOM, CardTypes.FOIL)])
# counts3 = all_prices_sorter.count([(Products.ALL, Sellers.ALL, CardTypes.NORMAL), (Products.MTGO, Sellers.ALL, CardTypes.NORMAL), (Products.PAPER, Sellers.ALL, CardTypes.NORMAL)])

# print(counts1)
# print(counts2)
# print(counts3)

# all_prices_sorter.normalize_prices()

# all_prices_sorter.keep_price_variations(lambda prices : sum(abs(p) for p in prices), lambda result : result > 0)