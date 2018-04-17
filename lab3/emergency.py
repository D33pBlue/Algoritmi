from matplotlib import pyplot as plt
import numpy as np
import math
from heapq import PriorityQueue
import time
import pickle

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

# initialize graph for dijkstra
def initSSSP(graph,sourc):
    for x in graph:
        graph[x]['d'] = INF
        graph[x]['p'] = None
    graph[sourc]['d'] = 0

# update weights for dijkstra
def relax(graph,u,v):
    graph[v]['d'] = graph[u]['d']+graph[u][v]["time"]
    graph[v]['p'] = u

# find minimal paths from source to all nodes
def dijkstra(graph,sourc):
    t = time.time()
    initSSSP(graph,sourc)
    q = PriorityQueue(graph)
    stop = False
    while (not q.empty()) and (not stop):
        u = q.extractMin()
        if graph[u]['d'] >= INF:
            stop = True
        else:
            for v in graph[u].keys():
                if not v in ['d','p']:
                    if ((graph[u]['d'])+(graph[u][v]["time"]))<(graph[v]['d']):
                        relax(graph,u,v)
                        q.changeKey(v,graph[v]['d'])
    print("[ Dijkstra Time:",time.time()-t,"s ]")

# extract the minimal path from source to destination if it is executed
# after the function dijkstra
def find_min_path(graph,sourc,dest):
    if graph[dest]['p'] == None:
        return None,INF
    path = [dest]
    path_time = graph[dest]['d']
    current = dest
    while current != None:
        current = graph[current]['p']
        if current != None:
            path.insert(0,current)
    return path,path_time

# return a plan that maximize the flow from a set of resources and
# a set of destination (considering capacity)
def ccrp(graph,sourc,dest):
    s0 = 's0'
    graph[s0] = dict()
    for x in sourc:
        graph[s0][x] = {"time":0.0,"cap":9999999999999999999999999}
    plan = []
    while True:
        path = None
        road_time = INF
        dijkstra(graph,s0)
        for vk in dest:
            p,t = find_min_path(graph,s0,vk)
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

# plot capacity and time of a plan in function of
# the number of paths considered
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

def cap_sourc(graph,sources):
    cap_tot = 0
    cap = dict()
    for x in sources:
        cap[x] = 0
        for v in graph[x].keys():
            cap[x] += graph[x][v]['cap']
            cap_tot += graph[x][v]['cap']
    return cap_tot,cap

def cap_dest(graph,dest):
    cap_tot = 0
    cap = dict()
    for x in graph:
        for d in dest:
            if d in graph[x]:
                if d in cap:
                    cap[d] += graph[x][d]['cap']
                else:
                    cap[d] = graph[x][d]['cap']
                cap_tot += graph[x][d]['cap']
    return (cap_tot,cap)

def cap_plan(plan):
    cap = 0
    for j in range(len(plan)):
        cap += plan[j][1]
    return cap

def find_bottlenek(sources,dests,plan):
    scap = dict()
    dcap = dict()
    for path in range(len(plan)):
        s = plan[path][0][1]
        d = plan[path][0][len(plan[path][0])-1]
        if s in scap:
            scap[s] += plan[path][1]
        else:
            scap[s] = plan[path][1]
        if d in dcap:
            dcap[d] += plan[path][1]
        else:
            dcap[d] = plan[path][1]
    return scap,dcap



if __name__ == '__main__':
    # graph = load_graph("SFroad.txt")
    sources = ['3718987342','915248218','65286004']
    destinations = ['261510687','3522821903','65319958','65325408','65295403','258913493']
    t = time.time()
    # sctot,sc = cap_sourc(graph,sources)
    # dctot,dc = cap_dest(graph,destinations)
    # print("Sources capacity:",sctot)
    # print(sc)
    # print("Destinations capacity:",dctot)
    # print(dc)
    # plan = ccrp(graph,sources,destinations)
    with open("plan.pickle",'rb') as f:
        plan = pickle.load(f)
    # print("Plan:",plan)
    print("Plan capacity:",cap_plan(plan))
    scb,dcb = find_bottlenek(sources,destinations,plan)
    print("Plan Sources Capacity Distribution:")
    print(scb)
    print("Plan Destinations Capacity Distribution:")
    print(dcb)
    print("[ Execution Time:",(time.time()-t)/60.0,"min ]")
    plot_plan_stats(plan)
