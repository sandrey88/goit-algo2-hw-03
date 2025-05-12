import csv
import random
from BTrees.OOBTree import OOBTree
import timeit

# Завантаження даних 
def load_items_from_csv(filename):
    items = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row['ID'] = int(row['ID'])
            row['Price'] = float(row['Price'])
            items.append(row)
    return items

# Додавання товарів 
def add_item_to_tree(tree, item):
    # Ключ — Price, значення — список товарів з такою ціною
    price = item['Price']
    if price not in tree:
        tree[price] = []
    tree[price].append({
        'ID': item['ID'],
        'Name': item['Name'],
        'Category': item['Category'],
        'Price': price
    })

def add_item_to_dict(d, item):
    d[item['ID']] = {
        'Name': item['Name'],
        'Category': item['Category'],
        'Price': item['Price']
    }

# Діапазонний запит 
def range_query_tree(tree, min_price, max_price):
    # OOBTree
    result = []
    for price, items in tree.items(min_price, max_price):
        result.extend(items)
    return result

def range_query_dict(d, min_price, max_price):
    # dict
    return [
        {'ID': id_, **value}
        for id_, value in d.items()
        if min_price <= value['Price'] <= max_price
    ]

# Основна логіка 
def main():
    items = load_items_from_csv('generated_items_data.csv')
    tree = OOBTree()
    d = dict()

    for item in items:
        add_item_to_tree(tree, item)
        add_item_to_dict(d, item)

    # Вибираємо випадкові діапазони цін для 100 запитів
    prices = [item['Price'] for item in items]
    min_price, max_price = min(prices), max(prices)
    queries = [
        (
            random.uniform(min_price, max_price - 10),
            random.uniform(min_price + 10, max_price)
        ) for _ in range(100)
    ]
    queries = [(min(a, b), max(a, b)) for a, b in queries]

    def run_tree_queries():
        for qmin, qmax in queries:
            range_query_tree(tree, qmin, qmax)

    def run_dict_queries():
        for qmin, qmax in queries:
            range_query_dict(d, qmin, qmax)

    tree_time = timeit.timeit(run_tree_queries, number=1)
    dict_time = timeit.timeit(run_dict_queries, number=1)

    print(f"Total range_query time for OOBTree: {tree_time:.6f} seconds")
    print(f"Total range_query time for Dict: {dict_time:.6f} seconds")

if __name__ == "__main__":
    main()