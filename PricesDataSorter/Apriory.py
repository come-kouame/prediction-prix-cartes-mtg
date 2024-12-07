import json
import pandas as ps
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, fpmax, fpgrowth
from mlxtend.frequent_patterns import association_rules


with open("data/AllTransactions.json", 'r',errors="ignore") as f:
        file = json.load(f)


def transactionsFill(day):
    transactionsDay = []
    for name in file:
        if day in file[name]:
            value = file[name][day]
            if value > 0.0:
                transactionsDay.append('+' + name)
            if value < 0.0:
                transactionsDay.append('-' + name)

    return transactionsDay

def fillListOfDays(start,finish):
    
    dates = []
    
    for month in range (start,finish+1):
        match month:
            case 1 | 3 | 5 | 7 | 8:
                for day in range (1,32):
                    dates.append("2024-"+"0"+str(month)+"-"+str(day))
            case 2:
                for day in range (1,30):
                    dates.append("2024-"+"0"+str(month)+"-"+str(day))
            case 4 | 6 | 9:
                for day in range (1,31):
                    dates.append("2024-"+"0"+str(month)+"-"+str(day))
            case 10 | 12:
                for day in range (1,32):
                    dates.append("2024-"+str(month)+"-"+str(day))
            case 11:
                for day in range (1,31):
                    dates.append("2024-"+str(month)+"-"+str(day))
    
    return dates

listOfDays = fillListOfDays(7,11)



def transactionFillAllDays():
    transactionsPrices = []
    for date in listOfDays:
        a = list( transactionsFill(str(date)) )
        transactionsPrices.append(a)
    return transactionsPrices

transactionsPrices= transactionFillAllDays()
#support = nb of transactions containing A / total nb of transactions
#confidence = nb of transactions containing A and B / nb of transactions containing A


te = TransactionEncoder()
te_ary = te.fit(transactionsPrices).transform(transactionsPrices)
df = ps.DataFrame(te_ary, columns=te.columns_)

frequent_itemsets = apriori(df, min_support=0.035, use_colnames=True)

rules = association_rules(frequent_itemsets, metric="conviction", min_threshold=3, num_itemsets=1)


###############################################################################
# Prediction des prix



def get_associated_cards(df, num_of_card):

    associated_in_antecedents = df[df['antecedents'].apply(lambda x: num_of_card in x)]['consequents']
    associated_in_consequents = df[df['consequents'].apply(lambda x: num_of_card in x)]['antecedents']

    associated_cards = []
    
    for cards in associated_in_antecedents:
        associated_cards.append(cards)
    for cards in associated_in_consequents:
        associated_cards.append(cards)
    

    return associated_cards

def clean_duplicates(cards):
    cleaned_cards = set(card.replace("-", "").replace("+", "") for card in cards)

    cleaned_cards_list = list(cleaned_cards)

    return cleaned_cards_list


def priceHasVaried(cardlist,day):
    boolList = []
    for card in cardlist:
        if card in file:
            print(card)
            if day in file[card]:
                value = file[card][day]
                print(value)
                if value > 0.0:
                    boolList.append(True)
                if value < 0.0:
                    boolList.append(True)

    print(boolList)
    return boolList

    
def variationLikelyhood(cardlist):
    variedCount = 0
    if (len(cardlist)==0):
        return -1.0
    for i in range(0,len(cardlist)):
        variedCount+=1

    return (variedCount/len(cardlist))


def predictPrice(num_of_card,day_of_prediction,boolFoil):
    
    if boolFoil:
        num_of_card_plus = '+'+str(num_of_card)+".foil"
        num_of_card_minus = '-'+str(num_of_card)+".foil"
    else:
        num_of_card_plus = '+'+str(num_of_card)+".normal"
        num_of_card_minus = '-'+str(num_of_card)+".normal"

    associated_list = get_associated_cards(rules,num_of_card_minus)
    associated_list2 = get_associated_cards(rules,num_of_card_plus)

    associated_list_minus = [" ".join(item) for item in associated_list]
    associated_list_plus = [" ".join(item) for item in associated_list2]
    

    no_duplicate_list_minus = clean_duplicates(associated_list_minus)
    no_duplicate_list_plus = clean_duplicates(associated_list_plus)


    boolListMinus = priceHasVaried(no_duplicate_list_minus,day_of_prediction)
    boolListPlus = priceHasVaried(no_duplicate_list_plus,day_of_prediction)


    predictFractionMinus = variationLikelyhood(boolListMinus)
    predictFractionPlus = variationLikelyhood(boolListPlus)

    print("La carte a "+str(predictFractionMinus)+" chances de baisser en prix")
    print("La carte a "+str(predictFractionPlus)+" chances d'augmenter en prix")


print(rules)
# print(get_associated_cards(rules,'+81382.normal'))
# predictPrice(81382,"2024-10-10",False)



#####################################################################################################
# PYVIS 


from pyvis.network import Network


def rulesVisuals():
    

    frequent_itemsets = apriori(df, min_support=0.035, use_colnames=True)
    rules = association_rules(frequent_itemsets, metric="conviction", min_threshold=3, num_itemsets=1)

    rules["antecedents"]=rules["antecedents"].astype(str)
    rules["consequents"]=rules["consequents"].astype(str)

    print(rules)
    card_Network=Network(height="1000px", width="1000px", directed=True, notebook=True)
    card_Network.force_atlas_2based()
    #card_Network.barnes_hut()
    #card_Network.hrepulsion()
    #card_Network.repulsion()

    rules_zip=zip(rules["antecedents"],
                        rules["consequents"],
                        rules["antecedent support"],
                        rules["consequent support"],
                        rules["confidence"])


    for i in rules_zip:
        FromItem=i[0].replace("frozenset({'","").replace("'})","").replace("',　'",",")
        ToItem=i[1].replace("frozenset({'","").replace("'})","").replace("',　'",",")
        FromWeight=i[2]
        ToWeight=i[3]
        EdgeWeight=i[4]

        card_Network.add_node(n_id=FromItem, shape="dot", value=FromWeight, title=FromItem + "<br>Support: " + str(FromWeight))
        card_Network.add_node(n_id=ToItem, shape="dot", value=ToWeight, title=ToItem + "<br>Support: " + str(ToWeight))
        card_Network.add_edge(source=FromItem, to=ToItem, value=EdgeWeight, arrowStrikethrough=False, title=FromItem + " --> " + ToItem + "<br>Confidence:" + str(EdgeWeight))




    card_Network.set_edge_smooth(smooth_type="continuous")
    card_Network.toggle_hide_edges_on_drag(True)
    card_Network.show_buttons(filter_=False)

    card_Network.save_graph("Card_Network.html")
    card_Network.show("Card_Network.html")


    #card_Network.get_adj_list()
    #card_Network.get_edges()
    #card_Network.get_network_data()

rulesVisuals()