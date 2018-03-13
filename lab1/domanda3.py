from domanda1 import *
import random

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
    inddist1 = indegree_dist(graph_cit)
    n = float(len(graph_cit.keys()))
    m = 0.0
    for v in graph_cit.keys():
        m += float(len(graph_cit[v]))/n
    print "m=",m,"n=",n
    graph_dpa = DPA_graph(int(m),int(n))
    inddist2 = indegree_dist(graph_dpa)
    compare_dists(inddist1,inddist2)
