

def load_data(path):
    dataset = []
    with open(path,'r') as f:
        for x in f.readlines():
            dataset.append(x.split(","))
    return dataset

def get_centroids(clusters):
    centroids = []
    for cluster in clusters:
        x,y = 0,0
        for point in cluster:
            x += point[3]
            y += point[4]
        x = float(x)/float(len(cluster))
        y = float(y)/float(len(cluster))
        centroids.append((x,y))
    return centroids

def hierarchical_clustering(P,k):
    n = len(P)
    clusters = [[x] for x in P]
    while len(clusters)>k:
        centroids = get_centroids(clusters)
        i,j = getClosestPair(centroids)
        c = clusters[i][:]+clusters[j][:]
        clusters.append(c)
        del clusters[i]
        del clusters[j]
    return clusters


def getClosestPair(P):
    P = sorted(P)
    S = [(i,P[i][1]) for i in range(len(P))]
    S = sorted(S,key= lambda x: x[1])
    d,i,j fastClosestPair(P,S)
    return i,j

def slowClosestPair(P):
    pass

def vector_split(S,Pl,Pr):
    pass

def closestPairStrip(S,mid,d):
    pass

def fastClosestPair(P,S):
    n = len(P)
    if n<3:
        return slowClosestPair(P)
    else:
        m = n/2
        Pl = [P[i] for i in range(m)]
        Pr = [P[i] for i in range(m,n)]
        Sl,Sr = vector_split(S,Pl,Pr)
        k1 = fastClosestPair(Pl,Sl)
        k2 = fastClosestPair(Pr,Sr)
        k = k1
        if k2<k1:
            k = k2
        mid = 0.5*(P[m-1][0]+P[m][0])
        k3 = closestPairStrip(S,mid,k[0])
        if k3<k:
            k = k3
        return k




if __name__ == '__main__':
    dataset = load_data("Data/unifiedCancerData_3108.csv")
    # getClosestPair(dataset)
