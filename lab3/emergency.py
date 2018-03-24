from matplotlib import pyplot as plt
import numpy as np
import math

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
                graph[info[0]][info[1]] = [road_time,cap]
    return graph

if __name__ == '__main__':
    graph = load_graph("SFroad.txt")
    print graph
