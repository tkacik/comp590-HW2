# candyGame.py
# Created by T. J. Tkacik for Assignment 2 of COMP 590
# Spring of 2014 at the University of North Carolina
import util

class candyGame(object):
    
    def __init__(self, scoreBoard="game_boards/AlmondJoy.txt"):
        sourceBoard = open(scoreBoard)
        self.scoreBoard = []
        self.gameBoard = []
        for line in sourceBoard:
            self.scoreBoard.append(line.strip().split("\t"))
        sourceBoard.close()
        for i in range(0, len(self.scoreBoard)):
            self.gameBoard.append([])
            for j in range(0, len(self.scoreBoard[i])):
                self.gameBoard[i].append("_")
        
        self.backTracked = 0
        
        '''if input == "stdin":
            self.N = eval(raw_input("How many friends?: "))
            self.T = eval(raw_input("How many trees?: "))
            self.heuristic = raw_input("Heuristic to use?: ")
            for i in range(0, self.T):
                self.trees.append(eval(raw_input("Next tree? (X,Y): ")))
                self.trees[i] = (self.trees[i][0]-1, self.trees[i][1]-1)
            self.assignment = self.recursiveHide(self.assignment)
            print self.expanded, " nodes expanded."
            print self.backTracked, " times back-tracked."'''
                
    def printLayout(self):
        layout = []
        for i in range(0, len(self.scoreBoard)):
            layout.append([])
            for j in range(0, len(self.scoreBoard[i])):
                layout[i].append(self.gameBoard[i][j] + "(" + self.scoreBoard[i][j] + ")")
        for row in layout:
            print row
            
    '''def runHeuristic(self, position, assignment):
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
            return 0 - dx - dy'''

    #recursiveHid takes a dictionary of variables to values    
    
         
if  __name__ =='__main__':
    candyGame().printLayout()