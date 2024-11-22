import json
import pandas as ps
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori

transactions = [('carte1', 'carte2', 'carte3'),
                ('carte1', 'carte2', 'carte4'),
                ('carte3', 'carte2', 'carte5')]

#itemsets, rules = apriori(transactions, min_support=0.5,  min_confidence=1)
#print(rules)  
#print(itemsets)


with open("AllPricesSorted.json", 'r',errors="ignore") as f:
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



listOfDays = ["2024-07-17","2024-07-18","2024-07-19","2024-07-20","2024-07-21","2024-07-22","2024-07-23","2024-07-24","2024-07-26","2024-07-27","2024-07-28",
              "2024-07-29","2024-07-30","2024-07-31","2024-08-01","2024-08-02","2024-08-03","2024-08-04","2024-08-05","2024-08-06","2024-08-07","2024-08-08",
              "2024-08-09","2024-08-10","2024-08-11","2024-08-12","2024-08-13","2024-08-14","2024-08-15","2024-08-16","2024-08-20","2024-08-21","2024-08-22",
              "2024-08-23","2024-08-24","2024-08-25","2024-08-26","2024-08-28","2024-08-29","2024-08-30","2024-08-31","2024-09-01","2024-09-02","2024-09-04",
              "2024-09-05","2024-09-06","2024-09-07","2024-09-08","2024-09-09","2024-09-10","2024-09-11","2024-09-12","2024-09-13","2024-09-14","2024-09-15",
              "2024-09-16","2024-09-17","2024-09-19","2024-09-20","2024-09-21","2024-09-22","2024-09-23","2024-09-24","2024-09-25","2024-09-25","2024-09-26",
              "2024-09-27","2024-09-28","2024-09-29","2024-09-30","2024-10-02","2024-10-03","2024-10-04","2024-10-05","2024-19-06","2024-10-07","2024-10-08",
              "2024-10-09","2024-10-10","2024-10-11","2024-10-12","2024-10-13","2024-10-14","2024-10-15","2024-10-16","2024-10-17","2024-10-18","2024-10-19",
              "2024-10-20","2024-10-21","2024-10-22","2024-10-23","2024-10-24","2024-10-25","2024-10-26","2024-10-27","2024-10-28","2024-10-29","2024-10-30",
              "2024-10-31"]


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
df.head(10)

print(apriori(df, min_support=0.1, use_colnames=True))

# itemsets, rules = apriori(transactionsPrices, min_support=0.08,  min_confidence=0.5)
# print(rules)

# for i in range (2,10):
#     try:
#         print(itemsets[i])
#     except:
#         pass
#     print(i)
