# Priority queue using a minheap

class Item:
    def __init__(self,key,value):
        self.value = value
        self.key = key

class PriorityQueue:

    def __init__(self,graph=None):
        self.q = []
        if graph!=None:
            for x in graph.keys():
                self.addItem(x,graph[x]['d'])
            # print [(x.key,x.value) for x in self.q[:10]]

    def addItem(self,value,key):
        x = Item(key,value)
        self.q.append(x)
        self.minHeapfyR(len(self.q)-1)

    def changeKey(self,item,key):
        for i in range(len(self.q)):
            if self.q[i].value==item:
                if key>self.q[i].key:
                    self.q[i].key = key
                    self.minHeapfy(i)
                else:
                    self.q[i].key = key
                    self.minHeapfyR(i)
                break

    def extractMin(self):
        hmin = self.q[0]
        self.q[0] = self.q[len(self.q)-1]
        del self.q[len(self.q)-1]
        self.minHeapfy(0)
        return hmin.value

    def minHeapfy(self,i):
        stop = False
        while not stop:
            l = 2*i
            r = 2*i+1
            m = i
            if l<len(self.q) and self.q[l].key<self.q[m].key:
                m = l
            if r<len(self.q) and self.q[r].key<self.q[m].key:
                m = r
            if m != i:
                t = self.q[i]
                self.q[i] = self.q[m]
                self.q[m] = t
                #self.minHeapfy(m)
                i = m
            else:
                stop = True

    def minHeapfyR(self,i):
        while i>=0 and self.q[i/2].key>self.q[i].key:
            t = self.q[i/2]
            self.q[i/2] = self.q[i]
            self.q[i] = t
            i = i/2

    def empty(self):
        return len(self.q)<=0
