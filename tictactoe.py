# tictactoe game

# other versions of r, b, and g
# SYMBOL_X_COLOR = '#EE4035'
# SYMBOL_O_COLOR = '#0492CF'
# GREEN_COLOR = '#7BC043

# self.canvas
# The Canvas is a rectangular area intended for drawing pictures or other complex layouts. 
# You can place graphics, text, widgets or frames on a Canvas.
# w = Canvas ( master, option=value, ... )
# this will be where we will be playing the tictactoe at, the rectangular area 

# self.canvas.pack()
# This geometry manager organizes widgets in blocks before placing them in the parent widget.
# try removing this and u will only have a small white blank screen 
# because widgets are not placed in the parent widget 

# self.window.bind()
# widget.bind(event, handler)

from tkinter import *
import numpy as np 

# define constants 
BOARD_SIZE = 600
SYMBOL_SIZE = BOARD_SIZE / 9
SYMBOL_WIDTH = 40
SYMBOL_X_COLOR = 'red'
SYMBOL_O_COLOR = 'blue'
GREEN_COLOR = 'green'
BLACK_COLOR = 'black'


class TicTacToe():
    def __init__(self):
        # create platform to play at 
        self.window = Tk()
        self.window.title('TICTACTOE')
        self.canvas = Canvas(self.window, width=BOARD_SIZE, height=BOARD_SIZE)
        self.canvas.pack()
        self.window.bind('<Button-1>', self.click)

        # creating board and the grid 
        self.initializeBoard() 
        self.boardStatus = np.zeros(shape=(3, 3))

        # create starting situation
        self.playerXTurn = True
        self.playerOTurn = False
        self.resetBoard = False
        self.gameover = False 
        self.tie = False 
        self.xWins = False 
        self.oWins = False 
        self.xScore = 0
        self.oScore = 0
        self.tieScore = 0


    # runs a loop so the game will forever be there (essentially starting and continuing the game)
    def start(self):
        self.window.mainloop()


    # drawing the grid
    # draw it at 200 and 400 on both the x and y axis respectively to split board into 9 squares
    # since both width and height = BOARD_SIZE = 600
    def initializeBoard(self):
        for i in range(1, 3):
            # vertical 
            self.canvas.create_line(i*200, 0, i*200, BOARD_SIZE)
            # horizontal
            self.canvas.create_line(0, i*200, BOARD_SIZE, i*200)


    # convert the position on the grid to a logical one set by myself 
    def convertGridToLogicalPosition(self, grid_position):
        grid_position = np.array(grid_position, dtype=int)
        return np.array(grid_position//200)
    

    # convert the position set by myself to a position on the grid 
    def ConvertLogicalToGridPosition(self, logical_position):
        logical_position = np.array(logical_position, dtype=int)
        return (logical_position*200 + 100)
    

    # check if grid is occupied
    # how to check? 
    # the board status started with np.zeros with shape(3, 3), 3 x 3 of zeros 
    # so if its not occupied it will still be a 0, return false for isGridOccupied
    # if its occupied, meaning shape X (-1), shape O (1), != 0 so return grid is occupied
    def isGridOccupied(self, logical_position):
        if self.boardStatus[logical_position[0]][logical_position[1]] == 0:
            return False
        else:
            return True 
    

    # create oval x1 y1 x2 y2 options
    def drawO(self, logical_position):
        grid_position = self.ConvertLogicalToGridPosition(logical_position)
        self.canvas.create_oval(grid_position[0] - SYMBOL_SIZE, grid_position[1] - SYMBOL_SIZE, 
                                grid_position[0] + SYMBOL_SIZE, grid_position[1] + SYMBOL_SIZE, 
                                width=SYMBOL_WIDTH, outline=SYMBOL_O_COLOR)
    

    # Canvas.create_line(x1, y1, x2, y2, ...., options = ...)
    def drawX(self, logical_position):
        grid_position = self.ConvertLogicalToGridPosition(logical_position)
        self.canvas.create_line(grid_position[0] - SYMBOL_SIZE, grid_position[1] - SYMBOL_SIZE, 
                                grid_position[0] + SYMBOL_SIZE, grid_position[1] + SYMBOL_SIZE, 
                                width=SYMBOL_WIDTH, fill=SYMBOL_X_COLOR)
        self.canvas.create_line(grid_position[0] - SYMBOL_SIZE, grid_position[1] + SYMBOL_SIZE, 
                                grid_position[0] + SYMBOL_SIZE, grid_position[1] - SYMBOL_SIZE, 
                                width=SYMBOL_WIDTH, fill=SYMBOL_X_COLOR)     
    

    # check who is the winner 
    def isWinner(self, player):
        if player == 'X':
            player = -1
        # shape 'O' => 1 
        else:
            player = 1
        
        # if the same shapes form a line, win 
        for i in range(3):
            if self.boardStatus[i][0] == self.boardStatus[i][1] == self.boardStatus[i][2] == player:
                return True 
            if self.boardStatus[0][i] == self.boardStatus[1][i] == self.boardStatus[2][i] == player:
                return True 
            
        # check diagonals 
        if self.boardStatus[0][0] == self.boardStatus[1][1] == self.boardStatus[2][2] == player:
            return True 
        if self.boardStatus[0][2] == self.boardStatus[1][1] == self.boardStatus[2][0] == player:
            return True 
        
        # if no one won yet return false 
        return False 
    

    # check if game is tied
    # numpy.where(condition, [x, y, ])
    # It returns a tuple of indices if an only condition is given, the indices where the condition is True.
    # np.where(self.boardStatus==0), only a condition is given, so it will return a tuple of indices of which the condition is true 
    # but dont forget, boardStatus is a 2d array with shape(3, 3), so there will be 2 tuples of indices returned
    # which is why a, b = np.where(self.boardStatus==0)
    # and condition given here is your boardstatus = 0, but if the grid is occupied fully and the game is tied 
    # meaning self.boardstatus will be filled with -1 and 1 for shape X and O, 
    # so condition is false 
    # there will be no indices in both tuples
    # length of each tuple will be 0 
    # if length of tuple = 0, meaning grid is already filled and no one has won, self.tie = true 
    def isTie(self):
        self.tie = False 
        a, b = np.where(self.boardStatus==0) 
        if len(b) == 0:
            self.tie = True 
        return self.tie  
    
    
    # when there is a winner or when grid is filled and players are tied, gameover
    def isGameover(self):
        self.xWins = self.isWinner('X')
        self.oWins = self.isWinner('O')
        self.tie = self.isTie()

        # out of this 3, 1 of it must be true
        # since (or) is being used, self.gameover will eventually be true
        self.gameover = self.xWins or self.oWins or self.tie

        return self.gameover
    

    # display page after gameover 
    # create_text(x,y,font, text, options….)
    def displayGameover(self):
        if self.xWins:
            self.xScore+=1
            texts = 'Winner: Player (X)'
            color = SYMBOL_X_COLOR
        elif self.oWins:
            self.oScore+=1
            texts = 'Winner: Player (O)'
            color = SYMBOL_O_COLOR
        else:
            self.tieScore+=1
            texts = "It's a tie"
            color = GREEN_COLOR

        # delete the previous round, display match summary 
        self.canvas.delete("all")
        self.canvas.create_text(300, 200, font="cmr 60 bold", fill=color, text=texts)

        score_text = 'Scores:\n'
        self.canvas.create_text(300, 320, font="cmr 40 bold", fill=BLACK_COLOR, text=score_text)
        score_text = 'Player (X):' + str(self.xScore) + '\nPlayer (O):' + str(self.oScore) + '\nTie:' + str(self.tieScore)
        self.canvas.create_text(300, 400, font="cmr 30 bold", fill=BLACK_COLOR, text=score_text)

        # after displaying match summary, make resetting the board and playing again true 
        reset_text = 'Click to play again\n'
        self.canvas.create_text(480, 600, font="cmr 20 bold", fill=BLACK_COLOR, text=reset_text)
        self.resetBoard = True 

    def playAgain(self):
        # reset board by drawing grid 
        self.initializeBoard()
        # reset board by restarting array(back to 0)
        self.boardStatus = np.zeros(shape=(3, 3))
        
        # winner lets loser click first
        # if that match is tied, player with lower score clicks first for next round 
        if self.xWins == True:
            self.playerOTurn = True
            self.playerXTurn = False 
        elif self.oWins == True:
            self.playerXTurn = True
            self.playerOTurn = False
        else: # tie 
            if self.xScore < self.oScore:
                self.playerXTurn = True 
                self.playerOTurn = False 
            elif self.xScore > self.oScore:
                self.playerOTurn = True 
                self.playerXTurn = False
            else: # self.xScore same as self.oScore, default x turn
                self.playerXTurn = True 
                self.playerOTurn = False 
            
    # clicking, and then binding it to the window 
    def click(self, event):
        # take in grid position 
        # it refers to the x/y coordinate of the mouse at the time of the event, 
        # relative to the upper left corner of the widget.
        grid_position = [event.x, event.y] 
        # convert it to logical 
        logical_position = self.convertGridToLogicalPosition(grid_position)

        # if game is still on 
        if self.resetBoard == False & self.gameover == False:
            if self.playerXTurn:
                if not self.isGridOccupied(logical_position):
                    self.drawX(logical_position)
                    self.boardStatus[logical_position[0]][logical_position[1]] = -1
                    self.playerXTurn = not self.playerXTurn
            else:
                if not self.isGridOccupied(logical_position):
                    self.drawO(logical_position)
                    self.boardStatus[logical_position[0]][logical_position[1]] = 1
                    self.playerXTurn = not self.playerXTurn
               
            # cant put before drawing  
            # if put before drawing, ure checking whether if its gameover, then draw. 
            # for eg if clicking the third 'X' were to form a line, u will be checking whether the 2nd 'X' will be gameover
            # which will be false, then u draw the third 'X'
            # only when u click the next shape 'O' then it will check for gameover = true and then draw 'O' 
            # so this must put at the last, immediately after u draw, u check for gameover 
            if self.isGameover():
                self.displayGameover()

        # if the game has ended 
        else:
            self.canvas.delete("all")
            self.playAgain()
            self.resetBoard = False 

# instance the class 
ttt = TicTacToe()
# start running the game 
ttt.start()
