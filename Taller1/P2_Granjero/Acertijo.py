import networkx as nx
import matplotlib.pyplot as plt


G = nx.DiGraph()


estados = [
    (('granjero', 'lobo', 'cabra', 'col'), ()),                      
    (('lobo', 'col'), ('granjero', 'cabra')),                        
    (('granjero', 'lobo', 'col'), ('cabra',)),                       
    (('col',), ('granjero', 'lobo', 'cabra')),                       
    (('granjero', 'cabra', 'col'), ('lobo',)),                       
    (('cabra',), ('granjero', 'lobo', 'col')),                       
    (('granjero', 'cabra'), ('lobo', 'col')),                        
    ((), ('granjero', 'lobo', 'cabra', 'col'))                       
]


for i, estado in enumerate(estados):
    G.add_node(i, label=f"Izq:{estado[0]} | Der:{estado[1]}")


for i in range(len(estados) - 1):
    G.add_edge(i, i + 1)


pos = nx.spring_layout(G, seed=42) 

labels = nx.get_node_attributes(G, 'label')

plt.figure(figsize=(14, 8))
nx.draw(G, pos, with_labels=True, node_size=2000, node_color="lightblue", arrows=True)
nx.draw_networkx_labels(G, pos, labels, font_size=8)

plt.title("Acertijo del granjero y el bote - Representación gráfica")
plt.show()