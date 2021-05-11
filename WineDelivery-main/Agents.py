from Problems import *
from Algorithms import *
import math
import random

class ItalyBFSAgent(BFS):
    
    def __init__(self,initial_state='Torino',goal_state='Roma'):
        self.graph = ItalyProblems.graph
        super().__init__(initial_state=initial_state,goal_state=goal_state)
        
            
    def getAdjacents(self,node):
        temp = []
        adjacents = self.graph[node.name]
        for pair in adjacents:
             temp.append(list(pair.keys())[0])

        return temp


       
class ItalyDFSAgent(DFS):
    
    def __init__(self,initial_state='Torino',goal_state='Roma'):
        self.graph = ItalyProblems.graph
        super().__init__(initial_state=initial_state,goal_state=goal_state)
        
            
    def getAdjacents(self,node):
        temp = []
        adjacents = self.graph[node.name]
        for pair in adjacents:
             temp.append(list(pair.keys())[0])

        return temp



class ItalyUCSAgent(UCS):
    
    def __init__(self,initial_state='Torino',goal_state='Roma'):
        self.graph = ItalyProblems.graph
        super().__init__(initial_state=initial_state,goal_state=goal_state)
        
            
    def getAdjacents(self,node):
        temp = []
        adjacents = self.graph[node.name]
        for pair in adjacents:
            name = list(pair.keys())[0]
            g_value = list(pair.values())[0]
            temp.append([name,g_value])
        
        return temp



class ItalyAStarAgent(AStar):
    
    def __init__(self,initial_state='Torino',goal_state='Roma'):
        self.graph = ItalyProblems.graph
        self.h = ItalyProblems.defalut_h_values
        initial_state_h_value = self.h[initial_state]
        super().__init__(initial_state_h_value,initial_state=initial_state,goal_state=goal_state)
        
            
    def getAdjacents(self,node):
        temp = []
        adjacents = self.graph[node.name]
        for pair in adjacents:
            name = list(pair.keys())[0]
            g_value = list(pair.values())[0]
            h_value = self.h[list(pair.keys())[0]]
            temp.append([name,g_value,h_value])
        
        return temp



class ItalyDLSAgent(DLS):
    
    def __init__(self,initial_state='Torino',goal_state='Roma',max_depth=0):
        self.graph = ItalyProblems.graph
        super().__init__(initial_state=initial_state,goal_state=goal_state,max_depth=max_depth)
        
            
    def getAdjacents(self,node):
        temp = []
        adjacents = self.graph[node.name]
        for pair in adjacents:
             temp.append(list(pair.keys())[0])

        return temp



class ItalyIDSAgent:
    
    def __init__(self,initial_state='Torino',goal_state='Roma'):
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.depth = 0
        self.Italy_dls_agent = None
    
    def run(self):
        while(True):
            self.Italy_dls_agent = ItalyDLSAgent(max_depth=self.depth)
            found_answer = self.Italy_dls_agent.run()
            if found_answer:
                return found_answer
            else:
                self.depth += 1
   
    def makeGraph(self):
        graph = {}
        for i in range(9):
            for j in range(9):
                graph['A_' + str(i) + str(j)] = []

        for i in range(9):
            for j in range(9):
                index = 'A_' + str(i) + str(j)
                subtable_row = i // 3
                subtable_col = j // 3

                for row in range(9):
                    if i != row:
                        graph[index].append('A_' + str(row) + str(j))

                for col in range(9):
                    if j != col:
                        graph[index].append('A_' + str(i) + str(col))
                
                subtable_row = subtable_row * 3
                subtable_col = subtable_col * 3
                for k in range(subtable_row,subtable_row + 3):
                    for t in range(subtable_col,subtable_col + 3):
                        if i != k or j != t:
                            if 'A_' + str(k) + str(t) not in graph[index]:
                                graph[index].append('A_' + str(k) + str(t))
                                
        return graph



