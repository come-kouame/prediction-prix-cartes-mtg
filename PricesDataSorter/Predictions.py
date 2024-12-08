import pandas as ps
import json
import datetime
import random
import matplotlib.pyplot as plt

class Event:
    date: datetime.datetime
    all_cards: dict
    concerned_cards: list = []
    participants:int = 0

    def __init__(self, date: datetime.datetime, all_cards: dict, participants: int):
        self.date = date
        self.all_cards = all_cards
        self.participants = participants
    
    def add_set(self, *, set_name: str = None, set_code: str = None):
        if set_name != None and set_code == None:
            for c in self.all_cards:
                sname = self.all_cards[c]['setName']
                if sname == set_name:
                    for k in self.all_cards[c]['prices'].keys():
                        self.concerned_cards.append(f'{c}.{k}')
        elif set_name == None and set_code != None:
            for c in self.all_cards:
                scode = self.all_cards[c]['setCode']
                if scode == set_code:
                    for k in self.all_cards[c]['prices'].keys():
                        self.concerned_cards.append(f'{c}.{k}') 

class Predictions:
    rules: ps.DataFrame
    transactions: dict
    cards_data: dict = {}
    event: Event
    last_transaction: datetime.datetime

    def __init__(self, 
                 rules_path: str, 
                 merged_file_path: str, 
                 transactions_path: str, 
                 event_date: datetime.datetime, 
                 event_participants: int,
                 *,
                 used_sets_names: list[str] = [],
                 used_sets_codes: list[str] = []):

        self.rules = ps.read_json(rules_path)

        with open(merged_file_path, 'r') as file:
            self.cards_data = json.load(file)
        
        # Récupérer la date de la dernière mise à jour des données
        with open(transactions_path, 'r') as f:
            self.transactions = json.load(f)

        self.last_transaction = datetime.datetime.strptime(ps.DataFrame.from_dict(self.transactions).index.max(), '%Y-%m-%d')

        self.event = Event(event_date, self.cards_data, event_participants)

        delta_time = (event_date - self.last_transaction).days

        if delta_time < 1 or delta_time > 7:
            raise ValueError(f'La prediction doit se faire entre 1 et 7 jours avec la derniere transaction effectuee {self.last_transaction.date()}')
        
        for s in used_sets_codes:
            self.event.add_set(set_code=s)
        for s in used_sets_names:
            self.event.add_set(set_name=s)
        

    def get_last_transaction(self, card_id: str) -> datetime.datetime:
        date = max(self.transactions[card_id].keys(), key=lambda d: datetime.datetime.strptime(d, '%Y-%m-%d'))
        return self.transactions[card_id][date]

    def get_predictions(self) -> list:
        """
        Prédit les cartes grâce à l'évènement enregistré\n
        Retournes les cartes concernées par la prévision
        """
        # Récupérer les cartes du prochain events
        cards_in_event = self.event.concerned_cards
        # Récupérer les cartes impactées par l'évènement (hors celles de l'évènement)
        impacted_cards = {}
        antecedants = self.rules['antecedents'].to_list()
        consequents = self.rules['consequents'].to_list()
        for i in range(len(antecedants)):
            # Vérifier que toutes les cartes de l'antécédent sont dans les cartes de l'évènement
            care_about = True
            for a in antecedants[i]:
                if a[1:] not in cards_in_event:
                    care_about = False
                    break
            if care_about:
                for c in consequents[i]:
                    card = c[1:]
                    if card not in cards_in_event:
                        if card in impacted_cards:
                            impacted_cards[card].append({
                                'confidence' : float(self.rules.iloc[i]['confidence']),
                                'lift' : float(self.rules.iloc[i]['lift']),
                                'mult' : 1.0 if c[0] == '+' else -1.0
                            })
                        else:
                            impacted_cards[card] = [{
                                'confidence' : float(self.rules.iloc[i]['confidence']),
                                'lift' : float(self.rules.iloc[i]['lift']),
                                'mult' : 1.0 if c[0] == '+' else -1.0
                            }]

        ndays = (self.event.date - self.last_transaction).days  # Nombre de jours avant l'event
        # Augmenter toutes les cartes jouées à l'évenement jusqu'à l'évenement
        for c in cards_in_event:
            last_known_price = self.get_last_transaction(c)
            # Estimer le prix qu'aura la carte jusqu'au jour de l'event
            reach_value = last_known_price / 100.0          # Prendre en compte le dernier prix enregistré
            reach_value *= self.event.participants / 100.0  # Prendre en compte le nombre de participant à l'event

            for d in range(1, ndays + 1):
                # Augmenter la valeur chaque jour des cartes de l'évenemnt
                add_price = float(d) / ndays * reach_value
                # Ajouter du bruit
                add_price += reach_value / 10.0 * (random.randint(0, 1) * 2 - 1)
                date = str((self.last_transaction + datetime.timedelta(days=d)).date())
                self.transactions[c][date] = round(last_known_price + add_price, 2)
                
        # Faire eveoluer le prix des cartes hors event
        for card in impacted_cards:
            last_known_price = self.get_last_transaction(card)
            for d in range(1, ndays + 1):
                date = str((self.last_transaction + datetime.timedelta(days=d)).date())
                add = 0
                for r in range(len(impacted_cards[card])):
                    confidence = float(impacted_cards[card][r]['confidence'] > random.uniform(0.0, 1.0))
                    lift = impacted_cards[card][r]['lift']
                    mult = impacted_cards[card][r]['mult']
                    add += mult * last_known_price / 1450.0 * confidence * lift
                new_price = round(last_known_price + (add / len(impacted_cards[card])), 2)
                self.transactions[card][date] = new_price
                last_known_price = new_price
        return cards_in_event + list(impacted_cards.keys())
    
    def save_predictions(self, predictions_path: str) -> list[str]:
        """
        Appelle la méthode get_predictions()\n
        Sauvegarde les prédictions dans le fichier voulu\n
        Retournes les cartes concernées par la prévision
        """
        impacted_cards = self.get_predictions()
        with open(predictions_path, 'w') as file:
            file.write(json.dumps(self.transactions))
        return impacted_cards
    
    def separate(self, card_uuid: str):
        """
        Récupère les transaction d'une carte et retourne deux tuples :\n
            - Dictionnaire avec les transactions connues\n
            - Dictionnaire avec les transactions attendues
        """
        transactions = {datetime.datetime.strptime(d, '%Y-%m-%d') : p for d, p in self.transactions[card_uuid].items()}
        olds = {d : p for d, p in transactions.items() if d <= self.last_transaction}
        news = {d : p for d, p in transactions.items() if d >= self.last_transaction}
        return olds, news

    def show_predictions(self, card_uuid: str):
        """
        Affiche un graphique avec les transactions connues (bleu) et attendues (rouge)
        """
        olds, news = self.separate(card_uuid)
        plt.title(card_uuid)
        plt.plot(olds.keys(), olds.values(), 'b')
        plt.plot(news.keys(), news.values(), 'r')
        plt.show()



# Instantie un objet prédiction
# Les trois premiers arguments sont pour 
#   - Les règles d'association (antecedants, consequents, confidence, lift)
#   - Le fichier fusionné d'AllPrintings et de AllPrices
#   - Les transactions non normalisées (doit contenir les cartes à valeurs constantes)
# La date de l'évènement servant à la prédiction (1 à 7 jours après la dernière transaction connue)
# Le nombre de participants à l'évènement servant à la prédiction
# Le nom des sets utilisés pendant l'évènement
predictions =  Predictions(
    'Data/regles.json', 
    'Data/merged_file.json', 
    'Data/AllTransactions.json',
    datetime.datetime(2024, 11, 21),
    1000,
    used_sets_names=['Kaldheim Promos']
    )
# Appel de la fonction de prédiction 
# Sauvegarde toutes les transactions (connues + attentues) dans un nouveau fichier
# Retourne une liste avec toutes les cartes impactées par les prédictions
impacted_cards = predictions.save_predictions('Data/AllPredictions.json')
# La méthode separate() renvoie les transactions connues puis les transactions attendues
knowns, expecteds = predictions.separate('45925.foil')
# La méthode show_prediction() affiche un graph qui montre les transactions connues et attendues
predictions.show_predictions('45926.foil')          # Carte jouée à l'évènement
predictions.show_predictions('45987.normal')        # Carte jouée à l'évènement
predictions.show_predictions('16440.normal')        # Carte non jouée à l'évènement
predictions.show_predictions('1777.normal')         # Carte non jouée à l'évènement
