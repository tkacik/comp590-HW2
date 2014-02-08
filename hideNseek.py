# hideNseek.py
# Created by T. J. Tkacik for Assignment 2 of COMP 590
# Spring of 2014 at the University of North Carolina
import util

class hideNseek(object):
    
    def __init__(self, input="stdin", heuristic="nullHeuristic"):
        self.trees = []
        self.N = 0
        self.T = 0
        self.expanded = 0
        self.assignment = []
        self.heuristic = heuristic
        self.backTracked = 0
        
        if input == "stdin":
            self.N = eval(raw_input("How many friends?: "))
            self.T = eval(raw_input("How many trees?: "))
            self.heuristic = raw_input("Heuristic to use?: ")
            for i in range(0, self.T):
                self.trees.append(eval(raw_input("Next tree? (X,Y): ")))
                self.trees[i] = (self.trees[i][0]-1, self.trees[i][1]-1)
            self.assignment = self.recursiveHide(self.assignment)
            print self.expanded, " nodes expanded."
            print self.backTracked, " times back-tracked."
                
    def printLayout(self):
        layout = []
        for i in range(0, self.N):
            layout.append([])
            for j in range(0, self.N):
                layout[i].append('0')
        for x,y in self.trees:        
            layout[x][y] = 'T'
        for x,y in self.assignment:
            layout[x][y] = 'P'
            
        for row in layout:
            print row
            
    def runHeuristic(self, position, assignment):
        if self.heuristic == "nullHeuristic" or self.heuristic == "":
            return 0
        if self.heuristic == "localManhattan":
            if len(assignment) == 0: return 0
            dx = abs(position[1] - assignment[len(assignment)-1][1])
            dy = abs(position[0] - assignment[len(assignment)-1][0])
            print position, ": ", dx + dy
            return 0 - dx - dy
        if self.heuristic == "globalManhattan":
            if len(assignment) == 0: return 0
            dx = 0
            dy = 0
            for i,j in assignment:
                dx += abs(position[1] - j)
                dy += abs(position[0] - i)
            print position, ": ", dx + dy
            return 0 - dx - dy

    #recursiveHid takes a dictionary of variables to values    
    def recursiveHide(self, assignment):
        positions = util.PriorityQueue()
        if len(assignment) == self.N:
            return assignment
        for i in range(0, self.N):
            for j in range(0, self.N):                          #for each i, j that is potential next assignment
                positions.push((i,j), self.runHeuristic((i,j), assignment))
        while not positions.isEmpty():
            i,j = positions.pop()
            self.expanded += 1
            print "checking position", (i, j)
            if (i, j) in self.trees + assignment:           #Alldiff 
                continue  
            seeFriend = False
            for x,y in assignment:                          #tree between friends
                if x == i:
                    seeFriend = True
                    for k in range(min(j, y)+1, max(j, y)):
                        if (i, k) in self.trees:
                            seeFriend = False
                            break
                if seeFriend: break
                if y == j:
                    seeFriend = True
                    for k in range(min(i, x)+1, max(i, x)):
                        if (k, j) in self.trees:
                            seeFriend = False
                            break
                if seeFriend: break
            if seeFriend:
                continue
            newAssignment = assignment + [(i, j)]
            print "position valid, continuing with ", newAssignment
            result = self.recursiveHide(newAssignment)
            if result != False: return result
        self.backtracked += 1
        return False
         
if  __name__ =='__main__':
    hideNseek("stdin", "globalManhattan").printLayout()