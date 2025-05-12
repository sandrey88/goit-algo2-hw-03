import networkx as nx
import matplotlib.pyplot as plt

# Вершини: 1,2 - термінали; 3-6 - склади; 7-20 - магазини
# Для зручності: 0 - суперджерело (додаємо для розрахунку максимального потоку)
G = nx.DiGraph()

# Додаємо ребра термінал-склад
G.add_edge(1, 3, capacity=25)
G.add_edge(1, 4, capacity=20)
G.add_edge(1, 5, capacity=15)
G.add_edge(2, 5, capacity=15)
G.add_edge(2, 6, capacity=30)
G.add_edge(2, 4, capacity=10)

# Ребра склад-магазин
G.add_edge(3, 7, capacity=15)
G.add_edge(3, 8, capacity=10)
G.add_edge(3, 9, capacity=20)
G.add_edge(4, 10, capacity=15)
G.add_edge(4, 11, capacity=10)
G.add_edge(4, 12, capacity=25)
G.add_edge(5, 13, capacity=20)
G.add_edge(5, 14, capacity=15)
G.add_edge(5, 15, capacity=10)
G.add_edge(6, 16, capacity=20)
G.add_edge(6, 17, capacity=10)
G.add_edge(6, 18, capacity=15)
G.add_edge(6, 19, capacity=5)
G.add_edge(6, 20, capacity=10)

# Додаємо ребра магазин-стік
for m in range(7, 21):
    G.add_edge(m, 100, capacity=1000)  # 100 - стік

# Додаємо суперджерело (0), якщо треба рахувати потік від обох терміналів разом
G.add_edge(0, 1, capacity=1000)
G.add_edge(0, 2, capacity=1000)

# Назви для звітності
node_names = {1: 'Термінал 1', 2: 'Термінал 2', 3: 'Склад 1', 4: 'Склад 2', 5: 'Склад 3', 6: 'Склад 4'}
for i in range(7, 21):
    node_names[i] = f'Магазин {i-6}'
node_names[100] = 'Стік'

# Розрахунок максимального потоку
flow_value, flow_dict = nx.maximum_flow(G, 0, 100, capacity='capacity')

# Формуємо таблицю результатів
print("Термінал\tМагазин\tФактичний Потік (одиниць)")
for terminal in [1, 2]:
    for sklad in G.successors(terminal):
        for magaz in G.successors(sklad):
            if magaz in range(7, 21):
                flow = flow_dict[sklad][magaz]
                if flow > 0:
                    print(f"{node_names[terminal]}\t{node_names[magaz]}\t{flow}")

print(f"\nЗагальний максимальний потік: {flow_value}")

# Аналіз
# 1. Потоки з терміналів
print("\nПотоки з терміналів:")
for t in [1, 2]:
    print(f"{node_names[t]}: {sum(flow_dict[t][s] for s in G.successors(t))}")

# 2. Маршрути з мінімальною пропускною здатністю (<=10):
print("\nМаршрути з мінімальною пропускною здатністю (<=10):")
for u, v, d in G.edges(data=True):
    if 0 < d['capacity'] <= 10:
        print(f"{node_names.get(u, u)} -> {node_names.get(v, v)}: {d['capacity']}")

# 3. Магазини з мінімальним постачанням
magazin_flows = {node_names[m]: flow_dict[m][100] for m in range(7, 21)}
min_flow = min(magazin_flows.values())
print("\nМагазини з мінімальним постачанням:")
for m, f in magazin_flows.items():
    if f == min_flow:
        print(f"{m}: {f}")

# 4. Вузькі місця (ребра, заповнені на 100%)
print("\nВузькі місця (ребра, заповнені на 100%):")
for u, v, d in G.edges(data=True):
    if u in flow_dict and v in flow_dict[u]:
        if d['capacity'] > 0 and flow_dict[u][v] == d['capacity']:
            print(f"{node_names.get(u, u)} -> {node_names.get(v, v)}: {flow_dict[u][v]}")

# ВІЗУАЛІЗАЦІЯ ГРАФА З ПОТОКАМИ
plt.figure(figsize=(12, 6))
# Позиції для вершин (групуємо для логістики)
pos = {}
pos[0] = (0, 2)
pos[1] = (1, 4)
pos[2] = (1, 0)
pos[3] = (3, 5)
pos[4] = (3, 3)
pos[5] = (3, 1)
pos[6] = (3, -1)
for i, y in zip(range(7, 21), range(6, -8, -1)):
    pos[i] = (5, y)
pos[100] = (7, 0)

# Малюємо вершини
nx.draw_networkx_nodes(G, pos, node_size=1000, node_color='skyblue')
# Малюємо ребра
nx.draw_networkx_edges(
    G,
    pos,
    arrows=True,
    arrowstyle='-|>',
    arrowsize=20,
    width=1,
    edge_color='gray',
    min_source_margin=25,
    min_target_margin=25
)
# Підписи вершин
nx.draw_networkx_labels(G, pos, labels=node_names, font_size=10, font_weight='bold', font_color='black')
# Підписи ребер: потік/пропускна здатність
edge_labels = {}
for u, v, d in G.edges(data=True):
    if u in flow_dict and v in flow_dict[u]:
        edge_labels[(u, v)] = f"{flow_dict[u][v]}/{d['capacity']}"
    else:
        edge_labels[(u, v)] = f"0/{d['capacity']}"
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, label_pos=0.45)
plt.title("Логістична мережа: потоки/пропускні здатності на ребрах")
plt.axis('off')
plt.tight_layout()
plt.show()