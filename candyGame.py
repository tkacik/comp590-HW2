# candyGame.py
# Created by T. J. Tkacik for Assignment 2 of COMP 590
# Spring of 2014 at the University of North Carolina
import util

class candyGame(object):
    
    def __init__(self, scoreBoard="game_boards/AlmondJoy.txt"):
        self.scoreBoard = []
        self.gameBoard = []
        self.player1 = humanPlayer(self, "A")
        self.player2 = humanPlayer(self, "B")
        
        sourceBoard = open(scoreBoard)        
        for line in sourceBoard:
            self.scoreBoard.append(line.strip().split("\t"))
        sourceBoard.close()
        for i in range(0, len(self.scoreBoard)):
            self.gameBoard.append([])
            for j in range(0, len(self.scoreBoard[i])):
                self.gameBoard[i].append("_")

        turn1 = True
        while not self.isGameOver():
            if turn1: self.move(self.player1)
            else: self.move(self.player2)
            turn1 = not turn1 
            self.printLayout()
            
        
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
    
    def move(self, player):
        while True:
            x,y = player.move()
            if self.gameBoard[x][y] == "_":
                self.gameBoard = self.updateState(x, y, player, self.gameBoard)
                return True
            else: print "Invalid position"
    
    def updateState(self, x, y, player, gameBoard):
        gameBoard[x][y] = player.ID
        neighbors = {(i,j) for i,j in set([(x-1,y),(x+1,y),(x,y-1),(x,y+1)]) if self.inBounds(i,j)}
        for i,j in neighbors:
            if gameBoard[i][j] == player.ID:
                for k,l in neighbors:
                    if gameBoard[k][l] is not "_":
                        gameBoard[k][l] = player.ID
        return gameBoard
        
    def isGameOver(self):
        vacant = 0
        for row in self.gameBoard:
            vacant += row.count('_')
        if vacant==0: return True
        return False
                
    def inBounds(self, x, y):
        if x >= (len(self.gameBoard)): return False
        if y >= (len(self.gameBoard[x])): return False
        if x < 0 or y < 0: return False
        return True
        
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
    
class candyPlayer(object):
    def __init__(self, candyGame, ID="X"):
        self.ID = ID
        self.candyGame = candyGame
         
class humanPlayer(candyPlayer):
    def move(self):
        return eval(raw_input("Where next?: "))      
         
#class minimaxPlay(candyPlayer): #TODO
         
#class alphabetaPlayer(candyPlayer): #TODO         
         
if  __name__ =='__main__':
    candyGame().printLayout()