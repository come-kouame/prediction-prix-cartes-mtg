import matplotlib.pyplot as plt
from enum import Enum
import json

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
    TGC_PLAYER = "tcgplayer"

class CardTypes(Enum):
    ALL = 0
    NORMAL = "normal"
    FOIL = "foil"
    ETCHED = "etched"


class DataSort:
    content = {}

    #Constructeur
    def __init__(self, file_path : str):
        with open(file_path, "r") as file:
            self.content = json.load(file)
    
    #Ecrit le fichir
    def write_json(self, file_path : str, json_dict, replace_content : bool) -> None:
        #Serialize
        json_object = json.dumps(json_dict, indent=4)
        #Write
        with open(file_path, 'w') as outfile:
            outfile.write(json_object)
        #Replace the class content
        if replace_content:
            self.content = json_dict
    
    def __is_card_exists(self, id_card : str,  product : Products, seller : Sellers, cardtype : CardTypes) -> bool:
        try:
            dic = self.content["data"][id_card][product.value][seller.value]["retail"][cardtype.value]
            return True
        except:
            return False
        
    #Récupérer les valeurs des cartes avec les dates
    def __get_card_evolution(self, id_card : str,  product : Products, seller : Sellers, cardtype : CardTypes):
        if self.__is_card_exists(id_card, product, seller, cardtype):
            return self.content["data"][id_card][product.value][seller.value]["retail"][cardtype]
        return None

    #Compte le nombre de cartes grâce à un tri
    def count(self, categories : list[(Products, Sellers, CardTypes)]) -> list[int]:
        rst : list[int] = []
        rst = rst + [0] * len(categories)   #Fill list with 0

        #Get a list with all enum values then remove myEnum.ALL in every list
        products : list[Products] = [p for p in Products]
        products.pop(0)
        sellers : list[Sellers] = [s for s in Sellers]
        sellers.pop(0)
        cardtypes : list[CardTypes] = [t for t in CardTypes]
        cardtypes.pop(0)

        #Process on the file
        for id in self.content["data"]:
            for i in range(len(categories)):
                cat = categories[i]

                product : Products = cat[0]
                seller : Sellers = cat[1]
                cardtype : CardTypes = cat[2]

                if product == Products.ALL:
                    for p in products:
                        if seller == Sellers.ALL:
                            for s in sellers:
                                if cardtype == CardTypes.ALL:
                                    for ct in cardtypes:
                                            rst[i] += int(self.__is_card_exists(id, p, s, ct))
                                else:
                                    rst[i] += int(self.__is_card_exists(id, p, s, cardtype))
                        else:
                            if cardtype == CardTypes.ALL:
                                for ct in cardtypes:
                                    rst[i] += int(self.__is_card_exists(id, p, seller, ct))
                            else:
                                rst[i] += int(self.__is_card_exists(id, p, seller, cardtype))
                else:
                    if seller == Sellers.ALL:
                        for s in sellers:
                            if cardtype == CardTypes.ALL:
                                for ct in cardtypes:
                                    rst[i] += int(self.__is_card_exists(id, product, s, ct))
                            else:
                                rst[i] += int(self.__is_card_exists(id, product, s, cardtype))
                    else:
                        if cardtype == CardTypes.ALL:
                            for ct in cardtypes:
                                rst[i] += int(self.__is_card_exists(id, product, seller, ct))
                        else:
                            rst[i] += int(self.__is_card_exists(id, product, seller, cardtype)) 

        return rst

    #Inclue les cartes qui valide le filtre product-seller-cardtype
    #Retourne un json
    def include(self, product : Products, seller : Sellers, cardtype : CardTypes):
        rst = {}
        rst["meta"] = self.content["meta"]
        rst["data"] = {}

        #Get a list with all enum values then remove myEnum.ALL in every list
        products : list[Products] = [p for p in Products]
        products.pop(0)
        sellers : list[Sellers] = [s for s in Sellers]
        sellers.pop(0)
        cardtypes : list[CardTypes] = [t for t in CardTypes]
        cardtypes.pop(0)

        #Process on the file
        for id in self.content["data"]:
            if product == Products.ALL:
                for p in products:
                    if seller == Sellers.ALL:
                        for s in sellers:
                            if cardtype == CardTypes.ALL:
                                for ct in cardtypes:
                                    if self.__is_card_exists(id, p, s, ct):
                                        rst["data"][id] = {}
                                        rst["data"][id][p.value] = {}
                                        rst["data"][id][p.value][s.value] = {}
                                        rst["data"][id][p.value][s.value]["retail"] = {}
                                        rst["data"][id][p.value][s.value]["retail"][ct.value] = self.content["data"][id][p.value][s.value]["retail"][ct.value]
                            else:
                                if self.__is_card_exists(id, p, s, cardtype):
                                    rst["data"][id] = {}
                                    rst["data"][id][p.value] = {}
                                    rst["data"][id][p.value][s.value] = {}
                                    rst["data"][id][p.value][s.value]["retail"] = {}
                                    rst["data"][id][p.value][s.value]["retail"][cardtype.value] = self.content["data"][id][p.value][s.value]["retail"][cardtype.value]
                    else:
                        if cardtype == CardTypes.ALL:
                            for ct in cardtypes:
                                if self.__is_card_exists(id, p, seller, ct):
                                        rst["data"][id] = {}
                                        rst["data"][id][p.value] = {}
                                        rst["data"][id][p.value][seller.value] = {}
                                        rst["data"][id][p.value][seller.value]["retail"] = {}
                                        rst["data"][id][p.value][seller.value]["retail"][ct.value] = self.content["data"][id][p.value][seller.value]["retail"][ct.value]
                        else:
                            if self.__is_card_exists(id, p, seller, cardtype):
                                rst["data"][id] = {}
                                rst["data"][id][p.value] = {}
                                rst["data"][id][p.value][seller.value] = {}
                                rst["data"][id][p.value][seller.value]["retail"] = {}
                                rst["data"][id][p.value][seller.value]["retail"][cardtype.value] = self.content["data"][id][p.value][seller.value]["retail"][cardtype.value]
            else:
                if seller == Sellers.ALL:
                    for s in sellers:
                        if cardtype == CardTypes.ALL:
                            for ct in cardtypes:
                                if self.__is_card_exists(id, product, s, ct):
                                    rst["data"][id] = {}
                                    rst["data"][id][product.value] = {}
                                    rst["data"][id][product.value][s.value] = {}
                                    rst["data"][id][product.value][s.value]["retail"] = {}
                                    rst["data"][id][product.value][s.value]["retail"][ct.value] = self.content["data"][id][product.value][s.value]["retail"][ct.value]
                        else:
                            if self.__is_card_exists(id, product, s, cardtype):
                                rst["data"][id] = {}
                                rst["data"][id][product.value] = {}
                                rst["data"][id][product.value][s.value] = {}
                                rst["data"][id][product.value][s.value]["retail"] = {}
                                rst["data"][id][product.value][s.value]["retail"][cardtype.value] = self.content["data"][id][product.value][s.value]["retail"][cardtype.value]           
                else:
                    if cardtype == CardTypes.ALL:
                        for ct in cardtypes:
                            if self.__is_card_exists(id, product, seller, ct):
                                rst["data"][id] = {}
                                rst["data"][id][product.value] = {}
                                rst["data"][id][product.value][seller.value] = {}
                                rst["data"][id][product.value][seller.value]["retail"] = {}
                                rst["data"][id][product.value][seller.value]["retail"][ct.value] = self.content["data"][id][product.value][seller.value]["retail"][ct.value]   

                    else:
                        if self.__is_card_exists(id, product, seller, cardtype):
                            rst["data"][id] = {}
                            rst["data"][id][product.value] = {}
                            rst["data"][id][product.value][seller.value] = {}
                            rst["data"][id][product.value][seller.value]["retail"] = {}
                            rst["data"][id][product.value][seller.value]["retail"][cardtype.value] = self.content["data"][id][product.value][seller.value]["retail"][cardtype.value] 
        return rst
    
    #Normalize les variations de prix des cartes en -1 et 1
    #Retourne un json
    def normalize_prices(self):

        rst = {}
        rst["meta"] = self.content["meta"]
        rst["data"] = {}

        for id in self.content["data"]:
            for product in self.content["data"][id]:
                for seller in self.content["data"][id][product]:
                    if "retail" in self.content["data"][id][product][seller]:
                        for cardtype in self.content["data"][id][product][seller]["retail"]:
                            rst["data"][id] = {}
                            rst["data"][id][product] = {}
                            rst["data"][id][product][seller] = {}
                            rst["data"][id][product][seller]["retail"] = {}

                            records = self.content["data"][id][product][seller]["retail"][cardtype]
                            dates = list(records.keys())
                            prices = list(records.values())
                            normalized_prices = {}

                            for i in range(1, len(records.values())):
                                price = (prices[i] - prices[i - 1]) / (prices[i] + prices[i - 1])
                                normalized_prices[dates[i]] = price
                            
                            rst["data"][id][product][seller]["retail"][cardtype] = normalized_prices

        return rst

    #Exclue les cartes dont la variation des prix ne vérifie pas les conditions des méthodes delegate en paramètre
    #accumulator_func = fonction delegate qui donne un résultat
    #check_func = fonction delegate qui valide le résultat de la fonction précédente (si la fonction retourne True, la carte est concervée)
    #Retourne un json filtré
    def exclude_with_prices_variation(self, accumulator_func, check_func):

        rst = {}
        rst["meta"] = self.content["meta"]
        rst["data"] = {}

        for id in self.content["data"]:
            for product in self.content["data"][id]:
                for seller in self.content["data"][id][product]:
                    if "retail" in self.content["data"][id][product][seller]:
                        for cardtype in self.content["data"][id][product][seller]["retail"]:
                            records = self.content["data"][id][product][seller]["retail"][cardtype]
                            prices = list(records.values())

                            resultat = accumulator_func(prices)
                            valid = check_func(resultat)

                            if valid:
                                rst["data"][id] = {}
                                rst["data"][id][product] = {}
                                rst["data"][id][product][seller] = {}
                                rst["data"][id][product][seller]["retail"] = {}
                                rst["data"][id][product][seller]["retail"][cardtype] = records
        
        return rst




#endregion

ds = DataSort("normalized_filtered_all_prices.json")

filtered_json = ds.exclude_with_prices_variation(lambda prices : sum(abs(p) for p in prices), lambda result : result > 0)

ds.write_json('filterd_normalied_prices.json', filtered_json, True)