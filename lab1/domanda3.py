from domanda1 import *
import random
import time

class DPATrial:
    def __init__(self,m):
        self.numNodes = m
        self.nodeNumbers = list()
        for i in range(m):
            for _ in range(m):
                self.nodeNumbers.append(i)

    def runTrial(self,m):
        V = []
        random.shuffle(self.nodeNumbers)
        for i in range(m):
            u = self.nodeNumbers.pop()
            V.append(u)
        self.nodeNumbers.append(self.numNodes)
        for v in V:
            self.nodeNumbers.append(v)
        self.numNodes = self.numNodes+1
        return V

def DPA_graph(m,n):
    graph = dict()
    for v in range(m):
        graph[v] = []
        for u in range(m):
            if u!=v:
                graph[v].append(u)
    trial = DPATrial(m)
    for u in range(m,n):
        V = trial.runTrial(m)
        graph[u] = []
        for v in V:
            graph[u].append(v)
    return graph

def outdegree_dist(graph):
    nvertex = float(len(graph.keys()))
    outdegree = dict()
    for v in graph.keys():
        deg = len(graph[v])
        if deg in outdegree:
            outdegree[deg] += 1.0/nvertex
        else:
            outdegree[deg] = 1.0/nvertex
    return outdegree

def compare_dists(dist1,dist2):
    xs = dist1.keys()
    ys = [dist1[v] for v in xs]
    plt.xscale('log')
    plt.yscale('log')
    plt.scatter(xs,ys,label="dist1")
    xs = dist2.keys()
    ys = [dist2[v] for v in xs]
    plt.scatter(xs,ys,label="dist2")
    plt.show()

if __name__ == '__main__':
    graph_cit = load_adj_list('Cit-HepTh.txt',directed=True)
    # inddist1 = indegree_dist(graph_cit)
    outdist1 = outdegree_dist(graph_cit)
    n = len(graph_cit.keys())
    m = 0.0
    for o in outdist1.keys():
        m += o*outdist1[o]
    m = int(round(m))
    print "m=",m,"n=",n
    t = time.time()
    graph_dpa = DPA_graph(m,n)
    print "Grafo generato in",time.time()-t,"s"
    inddist2 = indegree_dist(graph_dpa)
    # compare_dists(inddist1,inddist2)
    plot_dist(inddist2)
