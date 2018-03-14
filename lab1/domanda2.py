from domanda1 import *
import random

def ER_graph(n,p):
    graph = dict()
    for u in range(n):
        graph[u] = []
        for v in range(n):
            if v!=u:
                 a = random.random()
                 if a<p:
                     graph[u].append(v)
    return graph

if __name__ == '__main__':
    graph = ER_graph(2770,0.5)
    inddist = indegree_dist(graph)
    plot_dist(inddist)

"""
La distribuzione del grado entrante del grafo generato dall'algoritmo ER
e' a campana. E' quindi diversa da quella del grafo delle citazioni
ARGOMENTARE..
"""
