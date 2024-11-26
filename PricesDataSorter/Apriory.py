import json
import pandas as ps
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, fpmax, fpgrowth
from mlxtend.frequent_patterns import association_rules


transactions = [('carte1', 'carte2', 'carte3'),
                ('carte1', 'carte2', 'carte4'),
                ('carte3', 'carte2', 'carte5')]

#itemsets, rules = apriori(transactions, min_support=0.5,  min_confidence=1)
#print(rules)  
#print(itemsets)


with open("data/AllPricesSorted.json", 'r',errors="ignore") as f:
        file = json.load(f)


def transactionsFill(day):
    transactionsDay = []
    for uuid in file["data"]:
        if ("prices" in file["data"][uuid]):
             for card in file["data"][uuid]["prices"]:
                if day in file["data"][uuid]["prices"][card]:
                    value = file["data"][uuid]["prices"][card][day]
                    if value > 0.0:
                        transactionsDay.append('+' + uuid)
                    if value < 0.0:
                        transactionsDay.append('-' + uuid)

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

frequent_itemsets = apriori(df, min_support=0.05, use_colnames=True)

rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.5, num_itemsets=600)
print(rules["confidence"])

# itemsets, rules = apriori(transactionsPrices, min_support=0.08,  min_confidence=0.5)
# print(rules)

# for i in range (2,10):
#     try:
#         print(itemsets[i])
#     except:
#         pass
#     print(i)
