# candyGame.py
# Created by T. J. Tkacik for Assignment 2 of COMP 590
# Spring of 2014 at the University of North Carolina
import util, sys

class candyGame(object):
    
    def __init__(self, scoreBoard="game_boards/ReesesPieces.txt"):
        self.scoreBoard = []
        self.gameBoard = []
        self.player1 = alphabetaPlayer(self, "A", 4)
        self.player2 = minimaxPlayer(self, "B", 3)
        
        sourceBoard = open(scoreBoard)        
        for line in sourceBoard:
            self.scoreBoard.append(line.strip().split("\t"))
        sourceBoard.close()
        for i in range(0, len(self.scoreBoard)):
            self.gameBoard.append([])
            for j in range(0, len(self.scoreBoard[i])):
                self.gameBoard[i].append("_")

        turn1 = True
        while not self.isGameOver(self.gameBoard):
            if turn1: self.move(self.player1)
            else: self.move(self.player2)
            turn1 = not turn1 
            self.printLayout()
        
        score = self.score(self.gameBoard)
        print "Game Over!"
        print "Player", self.player1.ID, ":", score[0], "points,", self.player1.nodesExpanded, "nodes expanded"
        print "Player", self.player2.ID, ":", score[1], "points,", self.player2.nodesExpanded, "nodes expanded"
        if score[0] > score[1]: print "Player", self.player1.ID, "wins!"
        elif score[0] < score[1]: print "Player", self.player2.ID, "wins!"
        else: print "Tied game!"
    
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
    
    def score(self, gameBoard):
        score1, score2 = 0,0
        for i in range(0, len(gameBoard)):
            for j in range(0, len(gameBoard[i])):
                if gameBoard[i][j] == self.player1.ID:
                    score1 += eval(self.scoreBoard[i][j])
                if gameBoard[i][j] == self.player2.ID:
                    score2 += eval(self.scoreBoard[i][j])
        return (score1, score2)
    
    #If a player asks for a score, their score is returned first in the tuple
    def myScore(self, gameBoard, playerID):
        if playerID == self.player1.ID: return self.score(gameBoard)
        elif playerID == self.player2.ID:
            score = self.score(gameBoard)
            return (score[1],score[0])
        else: return False
        
    def isGameOver(self, gameBoard):
        vacant = 0
        for row in gameBoard:
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
            
    def duplicateBoard(self, board=None):
        newBoard = []
        if board == None: board = self.gameBoard
        for row in board:
            newBoard.append(list(row))
        return newBoard
    
    def otherPlayer(self, player):
        if player == self.player1: return self.player2
        return self.player1
    
class candyPlayer(object):
    def __init__(self, candyGame, ID="X", searchDepth=3):
        self.ID = ID
        self.candyGame = candyGame
        self.searchDepth = searchDepth
        self.nodesExpanded = 0
        
    def evaluate(self, gameBoard):
        score = self.candyGame.myScore(gameBoard, self.ID)
        if score[0]+score[1] == 0: return .5
        return float(score[0])/float(score[0]+score[1])
         
class humanPlayer(candyPlayer):
    def move(self):
        return eval(raw_input("Player " + self.ID + ": "))      
         
class minimaxPlayer(candyPlayer):  
    def move(self):
        spot = self.minimax(self.candyGame.duplicateBoard())
        print self.ID, "will take", spot
        return spot
    
    def minimax(self, gameBoard):
        nodes = self.nodesExpanded
        x,y = None, None
        max = float("-inf")
        for i in range(0, len(gameBoard)):
            for j in range(0, len(gameBoard[i])):
                if gameBoard[i][j] == "_":
                    newBoard = self.candyGame.updateState(i, j, self, self.candyGame.duplicateBoard(gameBoard))
                    #print "If I start with", (i,j), "..."
                    value = self.minvalue(newBoard, 1)
                    #print "So optimal play after", (i,j), "gives me", value, "odds."
                    if value > max:
                        #print "Taking", (i,j), "is the best move I see so far..."
                        max = value
                        x,y = i,j
        print "Expanded", (self.nodesExpanded - nodes), "nodes."
        return (x, y)
    
    def minvalue(self,gameBoard, depth):
        self.nodesExpanded+=1
        if depth == self.searchDepth:
            #print "then my chance of winning is", self.evaluate(gameBoard)
            return self.evaluate(gameBoard)
        if self.candyGame.isGameOver(gameBoard):
            score = self.candyGame.myScore(gameBoard, self.ID)
            if score[0] > score[1]:
                #print "I could win!"
                return 1
            #print "This is your game to lose..."
            return 0
        min = float("inf")
        for i in range(0, len(gameBoard)):
            for j in range(0, len(gameBoard[i])):
                if gameBoard[i][j] == "_":
                    #print "and you take", (i,j)
                    newBoard = self.candyGame.updateState(i, j, self.candyGame.otherPlayer(self), self.candyGame.duplicateBoard(gameBoard))
                    value = self.maxvalue(newBoard, depth+1)
                    if value < min:
                        min = value
        return min
    
    def maxvalue(self,gameBoard, depth):
        self.nodesExpanded+=1
        if depth == self.searchDepth:
            #print "then my chance of winning is", self.evaluate(gameBoard)
            return self.evaluate(gameBoard)
        if self.candyGame.isGameOver(gameBoard):
            score = self.candyGame.myScore(gameBoard, self.ID)
            if score[0] > score[1]:
                #print "I will win!"
                return 1
            #print "I mustn't lose..."
            return 0
        max = float("-inf")
        for i in range(0, len(gameBoard)):
            for j in range(0, len(gameBoard[i])):
                if gameBoard[i][j] == "_":
                    #print "then I take", i,j
                    newBoard = self.candyGame.updateState(i, j, self, self.candyGame.duplicateBoard(gameBoard))
                    value = self.minvalue(newBoard, depth+1)
                    if value > max:
                        max = value
        return max
        
class alphabetaPlayer(candyPlayer):
    def move(self):
        spot = self.minimax(self.candyGame.duplicateBoard())
        print self.ID, "will take", spot
        return spot
    
    def minimax(self, gameBoard):
        nodes = self.nodesExpanded
        x,y = None, None
        max = float("-inf")
        for i in range(0, len(gameBoard)):
            for j in range(0, len(gameBoard[i])):
                if gameBoard[i][j] == "_":
                    newBoard = self.candyGame.updateState(i, j, self, self.candyGame.duplicateBoard(gameBoard))
                    #print "If I start with", (i,j), "..."
                    value = self.minvalue(newBoard, 1, float("-inf"), float("inf"))
                    #print "So optimal play after", (i,j), "gives me", value, "odds."
                    if value > max:
                        #print "Taking", (i,j), "is the best move I see so far..."
                        max = value
                        x,y = i,j
        print "Expanded", (self.nodesExpanded - nodes), "nodes."
        return (x, y)
    
    def minvalue(self,gameBoard, depth, alpha, beta):
        self.nodesExpanded+=1
        if depth == self.searchDepth:
            #print "then my chance of winning is", self.evaluate(gameBoard)
            return self.evaluate(gameBoard)
        if self.candyGame.isGameOver(gameBoard):
            score = self.candyGame.myScore(gameBoard, self.ID)
            if score[0] > score[1]:
                #print "I could win!"
                return 1
            #print "This is your game to lose..."
            return 0
        min = float("inf")
        for i in range(0, len(gameBoard)):
            for j in range(0, len(gameBoard[i])):
                if gameBoard[i][j] == "_":
                    #print "and you take", (i,j)
                    newBoard = self.candyGame.updateState(i, j, self.candyGame.otherPlayer(self), self.candyGame.duplicateBoard(gameBoard))
                    value = self.maxvalue(newBoard, depth+1, alpha, beta)
                    if value < min:
                        min = value
                    if value < beta: beta = value
                    if value <= alpha: return value
        return min
    
    def maxvalue(self,gameBoard, depth, alpha, beta):
        self.nodesExpanded+=1
        if depth == self.searchDepth:
            #print "then my chance of winning is", self.evaluate(gameBoard)
            return self.evaluate(gameBoard)
        if self.candyGame.isGameOver(gameBoard):
            score = self.candyGame.myScore(gameBoard, self.ID)
            if score[0] > score[1]:
                #print "I will win!"
                return 1
            #print "I mustn't lose..."
            return 0
        max = float("-inf")
        for i in range(0, len(gameBoard)):
            for j in range(0, len(gameBoard[i])):
                if gameBoard[i][j] == "_":
                    #print "then I take", (i,j)
                    newBoard = self.candyGame.updateState(i, j, self, self.candyGame.duplicateBoard(gameBoard))
                    value = self.minvalue(newBoard, depth+1, alpha, beta)
                    if value > max:
                        max = value
                    if value > alpha: alpha = value
                    if value >= beta: return value
        return max       
         
if  __name__ =='__main__':
    candyGame().printLayout()