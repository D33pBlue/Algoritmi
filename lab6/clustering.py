import sys
import math
import time
import cv2
import pickle
from matplotlib import pyplot as plt

COLORS = [
    (255, 0, 0),
    (60, 180, 75),
    (255, 225, 25),
    (0, 130, 200),
    (245, 130, 48),
    (145, 30, 180),
    (70, 240, 240),
    (0, 102, 51),
    (255,153,153),
    (128, 0, 0),
    (0, 128, 128),
    (128, 128, 128),
    (0,0,0),
    (0, 0, 128),
    (135,80,96),
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

def first_centroids(P,k):
    centroids = sorted(P,key=lambda x: x[3],reverse=True)[:k]
    return [(c[1],c[2]) for c in centroids]

def kmeans(P,k,q):
    n = len(P)
    centroids = first_centroids(P,k)
    clusters = []
    for i in range(q):
        clusters = [[] for w in range(k)]
        for j in range(n):
            l = 0
            d = sys.maxint
            for f in range(len(centroids)):
                d2 = math.sqrt((P[j][1]-centroids[f][0])**2+(P[j][2]-centroids[f][1])**2)
                if d2<d:
                    d = d2
                    l = f
            clusters[l].append(P[j])
        for f in range(k):
            x,y = 0,0
            for point in clusters[f]:
                x += point[1]
                y += point[2]
            x = float(x)/float(len(clusters[f]))
            y = float(y)/float(len(clusters[f]))
            centroids[f] = (x,y)
    return clusters




def plot(base,imgname,clusters,colors=COLORS):
    im = cv2.imread(base)
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
        color = (color[2],color[1],color[0])
        for c in cluster:
            point = (int(c[1]),int(c[2]))
            cv2.circle(im,point,radius=radius,color=color,thickness=-2)
            cv2.line(im,centroid,point,color=color,thickness=2)
    cv2.imwrite(imgname,im)

def describe(clusters):
    s = 0
    for i,c in enumerate(clusters):
        print "cluster",i,"size:",len(c)
        s += len(c)
    print "num clusters",len(clusters)
    print "sum elems",s

def time_graph(dataset):
    times_hier = []
    times_kmeans = []
    for i in range(len(dataset)):
        try:
            k = len(dataset)-i
            print k
            t = time.time()
            clusters = hierarchical_clustering(dataset,k)
            times_hier.append((time.time()-t,k))
            t = time.time()
            clusters_kmeans = kmeans(dataset,k,5)
            times_kmeans.append((time.time()-t,k))
        except:
            pass
    plt.plot([x[1] for x in times_hier],[x[0] for x in times_hier])
    plt.show()
    plt.plot([x[1] for x in times_kmeans],[x[0] for x in times_kmeans])
    plt.show()

def error(C):
    x,y = 0,0
    for point in C:
        x += point[1]
        y += point[2]
    x = float(x)/float(len(C))
    y = float(y)/float(len(C))
    centroid = (x,y)
    s = 0.0
    for p in C:
        s += p[3]*((centroid[0]-p[1])**2+(centroid[1]-p[2])**2)
    return s

def distortion(L):
    return sum([error(c) for c in L])

def distortion_graph(dataset,name):
    disth = []
    distk = []
    for k in range(6,21):
        clusters_hier = hierarchical_clustering(dataset,k)
        clusters_kmeans = kmeans(dataset,k,5)
        disth.append((k,distortion(clusters_hier)))
        distk.append((k,distortion(clusters_kmeans)))
    plt.title("Dataset: unifiedCancerData_"+name+".csv")
    plt.plot([x[0] for x in disth],[x[1] for x in disth],label="hierarchical")
    plt.plot([x[0] for x in distk],[x[1] for x in distk],label="kmeans")
    plt.legend()
    plt.show()


if __name__ == '__main__':
    # NAME = "111"
    # CLUSTERS = 9
    # LOAD = False # if True load clusters from file,
    # # without calculating another time (if file esists)
    # clusters = []
    # # start computation
    # print "hierarchical_clustering"
    # t = time.time()
    # if LOAD:
    #     with open("Saves/clusters_"+NAME+".pickle","r") as f:
    #         clusters = pickle.load(f)
    # else:
    #     dataset = load_data("Data/unifiedCancerData_"+NAME+".csv")
    #     clusters = hierarchical_clustering(dataset,CLUSTERS)
    #     with open("Saves/clusters_"+NAME+".pickle","w") as f:
    #         pickle.dump(clusters,f)
    # print "time",time.time()-t
    # describe(clusters)
    # plot("Images/USA_Counties.png","Images/clusters_"+NAME+".png",clusters)
    # print "\n\nK-MEANS"
    # t = time.time()
    # dataset = load_data("Data/unifiedCancerData_"+NAME+".csv")
    # clusters_kmeans = kmeans(dataset,CLUSTERS,5)
    # plot("Images/USA_Counties.png","Images/clusters_kmeans_"+NAME+".png",clusters_kmeans)
    # describe(clusters_kmeans)
    # print "time",time.time()-t
    # # time_graph(dataset)
    # print "dist hierarchical_clustering",distortion(clusters)
    # print "dist kmeans",distortion(clusters_kmeans)
    for NAME in ['111','290','896']:
        dataset = load_data("Data/unifiedCancerData_"+NAME+".csv")
        distortion_graph(dataset,NAME)
