from MTGFiles import MTGFile

# Step 1: Initialize the MTGFile class with paths to your JSON files
mtg_file = MTGFile(all_prices_path='data/AllPrices.json', all_printings_path='data/AllPrintings.json')

# Step 2: Access the merged data
# merged_data = mtg_file.get_tree()
# print("Merged Data Sample:", list(merged_data.items())[:5])

# Step 3: Save the merged data to a file
# mtg_file.save('data/AllPricesSorted2.json')

# Step 4: Extract and save transactions organized by card name

transactions_by_name = mtg_file.save_transactions('data/AllTransactions.json', 'index', True, False)
print("Saved transactions to file.")
