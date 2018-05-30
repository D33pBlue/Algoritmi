import sys
import math
import time
import cv2
import pickle

COLORS = [
    (230, 25, 75),
    (60, 180, 75),
    (255, 225, 25),
    (0, 130, 200),
    (245, 130, 48),
    (145, 30, 180),
    (70, 240, 240),
    (240, 50, 230),
    (210, 245, 60),
    (128, 0, 0),
    (170, 255, 195),
    (128, 128, 0),
    (0,0,0),
    (0, 0, 128),
    (170, 110, 40)]

def load_data(path):
    dataset = []
    with open(path,'r') as f:
        for line in f.readlines():
            dataset.append([float(x) for x in line.split(",")])
    return dataset

def get_centroids(clusters):
    centroids = []
    for i,cluster in enumerate(clusters):
        x,y = 0,0
        for point in cluster:
            x += point[1]
            y += point[2]
        x = float(x)/float(len(cluster))
        y = float(y)/float(len(cluster))
        centroids.append((x,y,i))
    centroids = sorted(centroids)
    return {k:centroids[k] for k in range(len(centroids))}

def hierarchical_clustering(P,k):
    n = len(P)
    clusters = [[x] for x in P]
    while len(clusters)>k:
        centroids = get_centroids(clusters)
        i,j = getClosestPair(centroids)
        c = clusters[centroids[i][2]][:]+clusters[centroids[j][2]][:]
        clusters.append(c)
        if centroids[i][2] > centroids[j][2]:
            del clusters[centroids[i][2]]
            del clusters[centroids[j][2]]
        else:
            del clusters[centroids[j][2]]
            del clusters[centroids[i][2]]
    return clusters


def getClosestPair(P):
    S = [(i,P[i][1]) for i in range(len(P.keys()))]
    S = sorted(S,key= lambda x: x[1])
    d,i,j = fastClosestPair(P,S)
    return i,j

def distance(p1,p2):
    return math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)

def slowClosestPair(P):
    d,i,j = sys.maxint,-1,-1
    for u in P.keys():
        for v in P.keys():
            if v>u:
                d2 = distance(P[u],P[v])
                if d2<d:
                    d = d2
                    i = u
                    j = v
    return d,i,j

def vector_split(S,Pl,Pr):
    n = len(S)
    Sl,Sr = [],[]
    for i in range(n):
        if S[i][0] in Pl:
            Sl.append(S[i])
        else:
            Sr.append(S[i])
    return Sl,Sr


def closestPairStrip(S,P,mid,d):
    n = len(S)
    S1 = []
    for i in range(n):
        if abs(P[S[i][0]][0]-mid)<d:
            S1.append(S[i])
    d,i,j = sys.maxint,-1,-1
    for u in range(len(S1)-1):
        for v in range(u+1,min(u+4,len(S1))):
            d1 = distance(P[S1[u][0]],P[S1[v][0]])
            if d1<d:
                d = d1
                i = S1[u][0]
                j = S1[v][0]
    return d,i,j



def fastClosestPair(P,S):
    n = len(P.keys())
    if n<3:
        return slowClosestPair(P)
    else:
        m = n/2
        indexes = sorted(P.keys())
        Pl = {indexes[i]:P[indexes[i]] for i in range(m)}
        Pr = {indexes[i]:P[indexes[i]] for i in range(m,n)}
        Sl,Sr = vector_split(S,Pl,Pr)
        k1 = fastClosestPair(Pl,Sl)
        k2 = fastClosestPair(Pr,Sr)
        k = k1
        if k2<k1:
            k = k2
        mid = 0.5*(P[indexes[m-1]][0]+P[indexes[m]][0])
        k3 = closestPairStrip(S,P,mid,k[0])
        if k3<k:
            k = k3
        return k


def plot(img,clusters,colors=COLORS):
    im = cv2.imread(img)
    radius = 3
    for i in range(len(clusters)):
        cluster = clusters[i]
        x,y = 0,0
        for point in cluster:
            x += point[1]
            y += point[2]
        x = float(x)/float(len(cluster))
        y = float(y)/float(len(cluster))
        centroid = (int(x),int(y))
        color = colors[i]
        for c in cluster:
            point = (int(c[1]),int(c[2]))
            cv2.circle(im,point,radius=radius,color=color,thickness=-2)
            cv2.line(im,centroid,point,color=color,thickness=2)
    cv2.imwrite("Images/plot.png",im)

def describe(clusters):
    s = 0
    for i,c in enumerate(clusters):
        print "cluster",i,"size:",len(c)
        s += len(c)
    print "num clusters",len(clusters)
    print "sum elems",s

if __name__ == '__main__':
    # dataset = load_data("Data/unifiedCancerData_3108.csv")
    t = time.time()
    # clusters = hierarchical_clustering(dataset,15)
    # with open("clusters","w") as f:
    #     pickle.dump(clusters,f)
    clusters = []
    with open("clusters","r") as f:
        clusters = pickle.load(f)
    print "time",time.time()-t
    describe(clusters)
    plot("Images/USA_Counties.png",clusters)
