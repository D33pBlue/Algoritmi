from matplotlib import pyplot as plt
import math
import numpy as np

"""
Legge i dati da file e restituisce la lista delle adiacenze del grafo
"""
def load_adj_list(file,directed=False):
    """Aggiunge un vertice adj alla lista dei vertici adiacenti a v in adj_list"""
    def add_vertex(adj_list,v,adj):
        if v in adj_list and adj!=None:
            adj_list[v].append(adj)
        elif adj != None:
            adj_list[v] = [adj]
        elif adj==None and v not in adj_list:
            adj_list[v] = []

    with open(file,'r') as f:
        adj_list = dict()
        for line in f.readlines():
            if line[0] != '#':
                edge = line.split()
                u,v = edge[0],edge[1]
                add_vertex(adj_list,u,v)
                if directed:
                    u = None
                add_vertex(adj_list,v,u)
        # print adj_list
        return adj_list

def indegree_dist(graph):
    nvertex = float(len(graph.keys()))
    indegrees = dict()
    for v in graph.keys():
        if not v in indegrees:
            indegrees[v] = 0.0
        for u in graph[v]:
            if not u in indegrees:
                indegrees[u] = 1.0
            else:
                indegrees[u] += 1.0
    # print indegrees
    dist = dict()
    for v in indegrees.keys():
        deg = indegrees[v]
        if deg != 0:
            if deg in dist:
                dist[deg] += 1.0/nvertex
            else:
                dist[deg] = 1.0/nvertex
    # print dist
    return dist

def degree_dist(graph):
    nvertex = float(len(graph.keys()))
    degree = dict()
    for v in graph.keys():
        deg = len(graph[v])
        if deg in degree:
            degree[deg] += 1.0/nvertex
        else:
            degree[deg] = 1.0/nvertex
    return degree

def plot_dist(dist):
    xs = dist.keys()
    ys = [dist[v] for v in xs]
    plt.xscale('log')
    plt.yscale('log')
    plt.scatter(xs,ys)
    plt.show()


if __name__ == '__main__':#Cit-HepTh
    adj_list = load_adj_list('Cit-HepTh.txt',directed=True)
    print len(adj_list.keys())
    inddist = indegree_dist(adj_list)
    plot_dist(inddist)
