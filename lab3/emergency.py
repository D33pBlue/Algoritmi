from matplotlib import pyplot as plt
import numpy as np
import math
from heapq import PriorityQueue

INF = 99999999999999999999999.0

# return the journey time of a road and its capacity
def get_time_cap(road,length):
    road = int(road)
    speed = 30.0
    cap = 500
    if road == 2:
        speed = 50.0
        cap = 750
    if road == 3:
        speed = 50.0
        cap = 1000
    if road == 4:
        speed = 70.0
        cap = 1500
    if road == 5:
        speed = 70.0
        cap = 2000
    if road == 6:
        speed = 90.0
        cap = 4000
    length = float(length)/1000.0
    road_time = length/speed
    return road_time,cap

# load a weighted directed graph from file
# [u][v][time,cap]
def load_graph(file):
    graph = dict()
    with open(file,'r') as f:
        for line in f.readlines():
            if line[0] != '#':
                info = line.split()
                if info[0] not in graph:
                    graph[info[0]] = dict()
                if info[1] not in graph:
                    graph[info[1]] = dict()
                road_time,cap = get_time_cap(info[3],info[2])
                graph[info[0]][info[1]] = {"time":road_time,"cap":cap}
    return graph

def initSSSP(graph,sourc):
    for x in graph:
        graph[x]['d'] = INF
        graph[x]['p'] = None
    graph[sourc]['d'] = 0

def relax(graph,u,v):
    graph[v]['d'] = graph[u]['d']+graph[u][v]["time"]
    graph[v]['p'] = u

def dijkstra(graph,sourc):
    initSSSP(graph,sourc)
    q = PriorityQueue(graph)
    while not q.empty():
        u = q.extractMin()
        # print u,graph[u]['d'],graph['s0']['d']
        # break
        for v in graph[u].keys():
            if not v in ['d','p']:
                # print (graph[u]['d'])+(graph[u][v]["time"]),graph[v]['d']
                if ((graph[u]['d'])+(graph[u][v]["time"]))<(graph[v]['d']):
                    # print graph[v]
                    relax(graph,u,v)
                    q.changeKey(v,graph[v]['d'])

def find_min_path(graph,sourc,dest):
    dijkstra(graph,sourc)
    if graph[dest]['p'] == None:
        return None,INF
    path = [dest]
    path_time = graph[dest]['d']
    current = dest
    while current != None:
        current = graph[current]['p']
        path.insert(0,current)
    return path,path_time

def ccrp(graph,sourc,dest):
    s0 = 's0'
    graph[s0] = dict()
    for x in sourc:
        graph[s0][x] = {"time":0.0,"cap":9999999999999999999999999}
    plan = []
    while True:
        path = None
        road_time = INF
        for vk in dest:
            p,t = find_min_path(graph,s0,vk)
            print p
            print t
            if t<road_time:
                path = p
                road_time = t
        if path == None:
            return plan
        flow = min([graph[path[i]][path[i+1]]["cap"] for i in range(len(path)-1)])
        plan.append((path,flow,road_time))
        for i in range(len(path)-1):
            graph[path[i]][path[i+1]]["cap"] -= flow
            if graph[path[i]][path[i+1]]["cap"] == 0:
                graph[path[i]].pop(path[i+1],None)

def plot_plan_stats(plan):
    captot = []
    timetot = []
    for i in range(1,len(plan)):
        cap = 0
        tm = 0
        for j in range(i):
            cap += plan[j][1]
            t = plan[j][2]
            if t > tm:
                tm = t
        captot.append(cap)
        timetot.append(tm)
    plt.plot(captot,timetot)
    plt.show()


if __name__ == '__main__':
    graph = load_graph("SFroad.txt")
    #print graph['261510687']
    sources = ['3718987342','915248218','65286004']
    destinations = ['261510687','3522821903','65319958','65325408','65295403','258913493']
    plan = ccrp(graph,sources,destinations)
    print "plan:",plan
    plot_plan_stats(plan)
