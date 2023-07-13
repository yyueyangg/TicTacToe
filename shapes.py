# try drawing out just X and O shapes and writing text for the tictactoe game 

from tkinter import *

BOARD_SIZE = 600
SYMBOL_X_COLOR = 'red'
SYMBOL_O_COLOR = 'blue'
BLACK_COLOR = 'black'

class Shapes():
    def __init__(self):
        self.window = Tk()
        self.window.title('SHAPES')
        self.canvas = Canvas(self.window, width=BOARD_SIZE, height=BOARD_SIZE)
        self.canvas.pack()
        self.drawO()
        self.drawX()
        self.text()

    def start(self):
        self.window.mainloop()

    def drawO(self):
        # o1 
        self.canvas.create_oval(35, 50, 165, 180, width=40, outline=SYMBOL_O_COLOR)
        # o2
        self.canvas.create_oval(235, 50, 365, 180, width=40, outline=SYMBOL_O_COLOR)
        # o3 
        self.canvas.create_oval(435, 50, 565, 180, width=40, outline=SYMBOL_O_COLOR)

    def drawX(self):
        # x1 
        self.canvas.create_line(35, 230, 165, 380, width=40, fill=SYMBOL_X_COLOR)
        self.canvas.create_line(165, 230, 30, 380, width=40, fill=SYMBOL_X_COLOR)

        # x2 
        self.canvas.create_line(235, 230, 365, 380, width=40, fill=SYMBOL_X_COLOR)
        self.canvas.create_line(365, 230, 235, 380, width=40, fill=SYMBOL_X_COLOR)

        # x3
        self.canvas.create_line(435, 230, 565, 380, width=40, fill=SYMBOL_X_COLOR)
        self.canvas.create_line(565, 230, 435, 380, width=40, fill=SYMBOL_X_COLOR)

    def text(self):
        # write a text at the bottom 
        self.canvas.create_text(300, 490, font="arial 40 bold", fill=BLACK_COLOR, text='shapes')



s = Shapes()
s.start()