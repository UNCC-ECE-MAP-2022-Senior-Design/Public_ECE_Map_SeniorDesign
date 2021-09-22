#!/usr/bin/env python
# coding: utf-8

# In[58]:


import math
from heapq import heapify, heappush, heappop # This is for the min heap library
import numpy as np
import sys
import random
import time

numNodes = 1000
edgeMatrix = np.zeros(shape = [numNodes, numNodes], dtype = float)
weightMatrix = np.zeros(shape = [numNodes, numNodes], dtype = float)
nodes = []
nodeCost = []
nodeCounter = 0
explored = [False] * numNodes
openList = []

def setup():
    global nodes
    global nodeCost
    global numNodes
    
    for i in range(numNodes):
        nodeCost.append(sys.maxsize)
    
    nodes.append(Node(0,0))
    numConnections = 10
    for i in range(numNodes-2):
        #xCoord = random.randint(i // numConnections, numConnections + i // numConnections)
        #yCoord = random.randint(i // numConnections, numConnections + i // numConnections)
        xCoord = random.randint(0, numNodes // 100)
        yCoord = random.randint(0, numNodes // 100)
        nodes.append(Node(xCoord, yCoord))
        
    nodes.append(Node(numNodes, numNodes))
    #nodes.append(Node(numConnections + numNodes // numConnections, numConnections + numNodes // numConnections))
    
    for node1 in range(numNodes):
        for node2 in range(numConnections):
            connect = node1 + node2
            if connect < numNodes:
                connectNodes(node1, connect)
    
    calcWeights()

def edgeCost(node1, node2): # defining the edges using the distance formula
    xdist = node1.xCoord - node2.xCoord
    ydist = node1.yCoord - node2.yCoord
    dist = math.sqrt(pow(xdist, 2) + pow(ydist, 2))
    return dist

def connectNodes(node1, node2):
    global edgeMatrix
    edgeMatrix[node1, node2] = 1
    edgeMatrix[node2, node1] = 1

def calcWeights():
    global edgeMatrix
    global weightMatrix
    global nodes
    for i in range(numNodes):
        for j in range(numNodes):
            if edgeMatrix[i, j] == 1:
                cost = edgeCost(nodes[i], nodes[j])
                weightMatrix[i, j] = cost

def setStart(node):
    global nodeCost
    global openList
    
    nodeCost[node.nodeID] = 0
    explored[node.nodeID] = True
    heappush(openList, node)

def explore(node):
    global weightMatrix
    global nodeCost
    global numNodes
    global nodes
    global openList
    
    currentNode = node.nodeID
    
    for nextNode in range(numNodes):
        if not explored[nextNode]:
            if weightMatrix[currentNode][nextNode] != 0:
                newCost = weightMatrix[currentNode][nextNode] + nodeCost[currentNode]
                
                if newCost < nodeCost[nextNode]:
                    nodeCost[nextNode] = newCost
                    nodes[nextNode].setPrevNode(node)
                    heappush(openList, nodes[nextNode])

class Node(): # defining nodes
    nodeID = -1
    xCoord = 0
    yCoord = 0
    prevNode = None
    
    def __init__ (self, xCoord, yCoord):
        global nodeCounter
        self.xCoord = xCoord
        self.yCoord = yCoord
        self.nodeID = nodeCounter
        nodeCounter += 1
    
    def __lt__(self, other):
        global nodeCost
        if nodeCost[self.nodeID] < nodeCost[other.nodeID]:
            return True
        else:
            return False
        
    def setPrevNode(self, node):
        self.prevNode = node

setup()

print("Started:", time.ctime(time.time()))

setStart(nodes[0])
destination = nodes[numNodes-1]

heapify(openList)

node = heappop(openList)

while node != destination:
    explore(node)
    explored[node.nodeID] = True
    node = heappop(openList)

print("Finished:", time.ctime(time.time()))

print(node.nodeID)
print(nodeCost[node.nodeID])

#while node.prevNode != None:
    #print(node.prevNode.nodeID)
    #node = node.prevNode


# In[ ]:



