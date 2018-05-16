import time
import math
import os
from heapq import *

HEADER = "NODE_COORD_SECTION"
WTYPE = "EDGE_WEIGHT_TYPE:"
DIMENSION = "DIMENSION:"
NAME = "NAME:"
FOOTER = "EOF"
RRR = 6378.388

def geo_to_rad(lat,lon):
    dlat,dlon = math.floor(lat),math.floor(lon)
    mlat,mlon = lat-dlat,lon-dlon
    lat_rad = math.pi*(dlat+5.0*mlat/3.0)/180.0
    lon_rad = math.pi*(dlon+5.0*mlon/3.0)/180.0
    return lat_rad,lon_rad

# receive tuples (x,y) for z1 and z2 coordinates
def distance(z1,z2,wtype="GEO"):
    if wtype == "GEO":
        z1la,z1lo = geo_to_rad(z1[0],z1[1])
        z2la,z2lo = geo_to_rad(z2[0],z2[1])
        q1 = math.cos(z1lo-z2lo)
        q2 = math.cos(z1la-z2la)
        q3 = math.cos(z1la+z2la)
        return math.floor(RRR*math.acos(0.5*((1.0+q1)*q2-(1.0-q1)*q3))+1.0)
    return math.sqrt((z1[0]-z2[0])**2+(z1[1]-z2[1])**2)

def load_data(file):
    lines = []
    graph = dict()
    with open(file,'r') as f:
        lines = f.readlines()
    header = True
    weight_type = "GEO"
    name = ""
    dim = 0
    for line in lines:
        words = line.split()
        if header:
            if words[0] == WTYPE:
                weight_type = words[1]
            elif words[0] == NAME:
                name = words[1]
            elif words[0] == DIMENSION:
                dim = int(words[1])
            elif words[0] == HEADER:
                header = False
        else:
            if words[0] == FOOTER:
                break
            idn,x,y = words[0],float(words[1]),float(words[2])
            # x = lat, y = lon
            graph[idn] = {'x':x,'y':y}
    if dim != len(graph.keys()):
        raise Exception("Not same node number as declared in DIMENSION")
    for u in graph.keys():
        graph[u]['dist'] = dict()
        for v in graph.keys():
            z1 = (graph[u]['x'],graph[u]['y'])
            z2 = (graph[v]['x'],graph[v]['y'])
            graph[u]['dist'][v] = distance(z1,z2,weight_type)
    return graph,name,weight_type,dim


def get_path(p,endp):
    path = ['1']
    stop = False
    while not stop:
        if endp in p:
            prec = p[endp]
            path.insert(0,prec[0])
            endp = prec
        else:
            stop = True
        if endp[0]=='1':
            stop = True
    return path

def check_distance(path,graph):
    i = '1'
    distance = 0.0
    for j in path:
        distance += graph[i]['dist'][j]
        i = j
    return distance

def held_karp(graph):
    d = dict()
    p = dict()
    bound = nearest_neighbour(graph)
    print "BOUND:",bound
    dist = hk_visit2('1',graph,graph.keys(),d,p,time.time(),30,bound)
    # path = get_path(p,('1',hashlist(graph.keys())))
    # print path
    return dist

def hashlist(S):
    return ",".join(sorted([x for x in S]))

def hk_visit(v,graph,S,d,p,start,limit):
    S_h = hashlist(S)
    if len(S) == 1 and S[0]==v:
        return graph['1']['dist'][v]
    if (v,S_h) in d:
        return d[(v,S_h)]
    mindist = 99999999999999999999999
    minprec = None
    for u in S:
        if time.time()-start>limit:
            break
        if u!=v:
            S2 = [x for x in S if x!=v]
            S2.sort(key=lambda x: graph[u]['dist'][x])
            dist = hk_visit(u,graph,S2,d,p,start,limit)
            if (dist+graph[u]['dist'][v]) < mindist:
                mindist = dist+graph[v]['dist'][u]
                minprec = (u,hashlist(S2))
    # print v,S_h
    d[(v,S_h)] = mindist
    p[(v,S_h)] = minprec
    return mindist


def hk_visit2(v,graph,S,d,p,start,limit,bound):
    S_h = hashlist(S)
    if len(S) == 1 and S[0]==v:
        return graph['1']['dist'][v]
    if (v,S_h) in d:
        return d[(v,S_h)]
    mindist = 99999999999999999999999
    minprec = None
    # if bound<0:
    #     return mindist
    for u in S:
        if time.time()-start>limit:
            break
        if u!=v:
            S2 = [x for x in S if x!=v]
            S2.sort(key=lambda x: graph[u]['dist'][x])
            dist = hk_visit2(u,graph,S2,d,p,start,limit,bound-graph[u]['dist'][v])
            if (dist+graph[u]['dist'][v]) < mindist:
                mindist = dist+graph[v]['dist'][u]
                minprec = (u,hashlist(S2))
    # print v,S_h
    d[(v,S_h)] = mindist
    p[(v,S_h)] = minprec
    return mindist


def nearest_neighbour(graph,v0='1',S0=None):
    d = dict()
    p = dict()
    S = [x for x in graph.keys() if (x!=v0 and (S0==None or x in S0))]
    v = v0
    d[v] = 0
    last = v0
    while len(S)>0:
        mindist = 9999999999999999999
        u = '-1'
        for x in S:
            if x!=v and graph[v]['dist'][x]<mindist:
                mindist = graph[v]['dist'][x]
                u = x
        d[u] = d[v]+mindist
        p[u] = v
        v = u
        last = u
        S = [x for x in S if x!=u]
        # print "dist",d[u],"u",u,"p",p[u]
    d[v0] = d[last]+graph[last]['dist'][v0]
    p[v0] = last
    return d[v0]

def best_nn(graph,S):
    nn_best = 999999999999999
    v_best = S[0]
    for v in S:
        nn = nearest_neighbour(graph,v,S)
        if nn<nn_best:
            nn_best = nn
            v_best = v
    return nn_best,v_best

def prim_mst(graph,r):
    p = dict()
    for v in graph.keys():
        graph[v]['extract'] = False
        graph[v]['d'] = 999999999999999999999999
        p[v] = None
    graph[r]['d'] = 0
    q = PriorityQueue(graph)
    while not q.empty():
        u = q.extractMin()
        graph[u]['extract'] = True
        for v in graph[u]['dist'].keys():
            if (not graph[v]['extract']) and graph[u]['dist'][v]<graph[v]['d']:
                graph[v]['d'] = graph[u]['dist'][v]
                p[v] = u
                q.changeKey(graph[v]['pos'],v,graph[v]['d'])
    return [(v,p[v]) for v in graph.keys() if v!=r]

def infix_visit(tree,v0,path):
    if not tree[v0]['visited']:
        path.append(v0)
        tree[v0]['visited'] = True
        for c in tree[v0]['adj']:
            infix_visit(tree,c,path)


def two_approximation(graph):
    v0 = '1'
    mst = prim_mst(graph,v0)
    tree = dict()
    for v in mst:
        if not v[0] in tree:
            tree[v[0]]={'adj':[]}
        if not v[1] in tree:
            tree[v[1]]={'adj':[]}
        tree[v[0]]['adj'].append(v[1])
        tree[v[1]]['adj'].append(v[0])
    for v in tree.keys():
        tree[v]['visited'] = False
    path = []
    infix_visit(tree,v0,path)
    path.append(v0)
    dist = 0.0
    u = v0
    for v in path[1:]:
        dist += graph[u]['dist'][v]
        u = v
    return dist

if __name__ == '__main__':
    results = []
    for data in [
        ('burma14.tsp',3323.0),
        ('ulysses16.tsp',6747.0),#6859.0),
        ('berlin52.tsp',7542.0),
        ('kroA100.tsp',21282.0),
        ('ch150.tsp',6528.0),
        ('gr202.tsp',40160.0),
        ('pcb442.tsp',50778.0)
        ]:
        res = []
        graph,name,weight_type,dim = load_data("./Data/"+data[0])
        print("Name:",name,"Dist:",weight_type,"Dim:",dim)
        for f in [
            ('Held-Karp',held_karp),
            ('Nearest-Neighbour',nearest_neighbour),
            ('2-Approximation',two_approximation)
            ]:
            print f[0],"[dist][time][error]"
            t = time.time()
            sol = f[1](graph)
            t = time.time()-t
            e = float(sol-data[1])/data[1]
            print sol,',',t,',',e
            res.append(sol)
            res.append(t)
            res.append(e)
        results.append(res)
        print ""
    print "----------------------------------"
    for r in results:
        print "\t".join([str(x) for x in r])
