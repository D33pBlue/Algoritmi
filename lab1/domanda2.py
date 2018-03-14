from domanda1 import *
import random

"""
Implementazione dell'algoritmo ER per la generazione di un grafo casuale
n = numero nodi
p = probabilita
"""
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
