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

frequent_itemsets = apriori(df, min_support=0.04, use_colnames=True)

rules = association_rules(frequent_itemsets, metric="conviction", min_threshold=3, num_itemsets=1)

def get_associated_cards(df, num_of_card):

    associated_in_antecedents = df[df['antecedents'].apply(lambda x: num_of_card in x)]['consequents']
    associated_in_consequents = df[df['consequents'].apply(lambda x: num_of_card in x)]['antecedents']

    associated_cards = []
    
    for cards in associated_in_antecedents:
        associated_cards.append(cards)
    for cards in associated_in_consequents:
        associated_cards.append(cards)
    
    
    return associated_cards

print(get_associated_cards(rules[["antecedents","consequents","confidence","conviction","leverage","zhangs_metric"]],'-10102.normal'))
