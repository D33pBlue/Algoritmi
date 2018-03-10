import numpy as np
from matplotlib import pyplot as plt
import math

"""
Legge i dati da file e restituisce la lista delle adiacenze del grafo
"""
def load_adj_list(file):
    with open(file,'r') as f:
        adj_list = []
        for line in f.readlines():
            if line[0] != '#':
                adj_list.append(line.split())
        return np.array(adj_list)

def indegree_dist(graph):
    indeg = dict()
    degsum = float(graph.shape[0])
    for arch in graph:
        v = arch[1]
        if v in indeg:
            indeg[v] += 1.0/degsum
        else:
            indeg[v] = 1.0/degsum
        u = arch[0]
        if not (u in indeg):
            indeg[u] = 0.0
    nnodes = float(len(indeg))
    indegdist = dict()
    for v in indeg:
        ind = indeg[v]
        if ind in indegdist:
            indegdist[ind] += 1.0/nnodes
        else:
            indegdist[ind] = 1.0/nnodes
    return indegdist

adj_list = load_adj_list('Cit-HepTh.txt')
print adj_list.shape
inddist = indegree_dist(adj_list)
print len(inddist)
xs = sorted(inddist.keys())
logxs = []
for x in xs:
    if x <= 0.0:
        logxs.append(x)
    else:
        logxs.append(math.log(x))
ys = [math.log(inddist[v]) for v in xs]
plt.plot(xs,ys)
plt.show()
