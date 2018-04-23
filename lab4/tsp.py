import time
import math
import os

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


def held_karp(graph):
    d = dict()
    p = dict()
    dist = hk_visit('1',graph,graph.keys(),d,p,time.time(),30)
    return dist

def hashlist(S):
    return ",".join(sorted([x for x in S]))

def hk_visit(v,graph,S,d,p,start,limit):
    S_h = hashlist(S)
    if len(S) == 1 and S[0]==v:
        return graph[v]['dist']['1']
    if (v,S_h) in d:
        return d[(v,S_h)]
    mindist = 99999999999999999999999
    minprec = None
    for u in S:
        if time.time()-start>limit:
            break
        if u!=v:
            dist = hk_visit(u,graph,[x for x in S if x!=v],d,p,start,limit)
            if (dist+graph[u]['dist'][v]) < mindist:
                mindist = dist+graph[v]['dist'][u]
                minprec = u
    # print v,S_h
    d[(v,S_h)] = mindist
    p[(v,S_h)] = minprec
    return mindist

def nearest_neighbour(graph):
    d = dict()
    p = dict()
    S = [x for x in graph.keys() if x!='1']
    v = '1'
    d[v] = 0
    last = '1'
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
    d['1'] = d[last]+graph[last]['dist']['1']
    p['1'] = last
    return d['1']


def two_approximation(graph):
    pass

if __name__ == '__main__':
    for data in ['burma14.tsp','ulysses16.tsp','berlin52.tsp','kroA100.tsp',
        'ch150.tsp','gr202.tsp','pcb442.tsp']:#os.listdir("./Data"):
        graph,name,weight_type,dim = load_data("./Data/"+data)
        print("Name:",name,"Dist:",weight_type,"Dim:",dim)
        t = time.time()
        print "Optimal:",held_karp(graph),"Time:",time.time()-t,"s"
        t = time.time()
        print "nearest-Neighbour:",nearest_neighbour(graph),"Time:",time.time()-t,"s"
        print ""
