# Priority queue using a minheap

class Item:
    def __init__(self,key,value,pos,handler):
        self.value = value
        self.key = key
        self.pos = pos
        self.h = handler
        self.set_pos(pos)

    def set_pos(self,pos):
        self.pos = pos
        self.h[self.value]['pos'] = pos

class PriorityQueue:

    def __init__(self,graph=None):
        self.NC = 10
        self.q = []
        if graph!=None:
            for x in graph.keys():
                self.addItem(x,graph[x]['d'],graph)

    def addItem(self,value,key,graph):
        x = Item(key,value,len(self.q),graph)
        self.q.append(x)
        self.minHeapfyR(len(self.q)-1)

    def changeKey(self,i,item,key):
        if i >= len(self.q):
            i = -1
            for j in range(len(self.q)):
                if self.q[j].value == item:
                    i=j
                    break
        # for i in range(len(self.q)):
        # if self.q[i].value==item:
        if key>self.q[i].key:
            self.q[i].key = key
            self.minHeapfy(i)
        else:
            self.q[i].key = key
            self.minHeapfyR(i)
        # break

    def extractMin(self):
        hmin = self.q[0]
        # hmin.set_pos(-1)
        self.q[0] = self.q[len(self.q)-1]
        del self.q[len(self.q)-1]
        self.minHeapfy(0)
        return hmin.value

    def minHeapfy(self,i):
        stop = False
        while not stop:
            childs = [self.NC*i+x for x in range(self.NC)]
            # l = 2*i
            # r = 2*i+1
            m = i
            for x in childs:
                if x<len(self.q) and self.q[x].key<self.q[m].key:
                    m = x
            # if l<len(self.q) and self.q[l].key<self.q[m].key:
            #     m = l
            # if r<len(self.q) and self.q[r].key<self.q[m].key:
            #     m = r
            if m != i:
                t = self.q[i]
                post = t.pos
                self.q[i] = self.q[m]
                self.q[m] = t
                self.q[m].set_pos(self.q[i].pos)
                self.q[i].set_pos(post)
                i = m
            else:
                stop = True

    def minHeapfyR(self,i):
        while i>=0 and self.q[i/self.NC].key>self.q[i].key:
            t = self.q[i/self.NC]
            post = t.pos
            self.q[i/self.NC] = self.q[i]
            self.q[i] = t
            self.q[i].set_pos(self.q[i/self.NC].pos)
            self.q[i/self.NC].set_pos(post)
            i = i/self.NC

    def empty(self):
        return len(self.q)<=0
