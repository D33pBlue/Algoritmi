# Priority queue using a minheap
class PriorityQueue:

    def __init__(self,graph=None):
        self.q = []
        if graph!=None:
            for x in graph.keys():
                self.addItem(x,graph[x]['d'])

    def addItem(self,item,key):
        pass

    def decreaseKey(self,item,key):
        pass

    def extractMin(self):
        pass

    def empty(self):
        return len(self.q)>0
