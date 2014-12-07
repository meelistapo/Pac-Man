__author__ = 'Eduard'
__author__ = 'Meelis Tapo'
from tkinter import ttk
from tkinter import font

class menu:
    def __init__(self, parent):
        self.parent = parent
        self.y = 815
        self.font = font.Font(family='Helvetica', size=12, weight='bold')
        self.score = ttk.Label(self.parent, text="Score:", font=self.font)
        self.lives = ttk.Label(self.parent, text="Lives:", font=self.font)
        self.score_var = ttk.Label(self.parent, text="", font=self.font)
        self.lives_var = ttk.Label(self.parent, text="", font=self.font)
        self.score.place(x=175, y=self.y)
        self.lives.place(x=275, y=self.y)
        self.score_var.place(x=230, y=self.y)
        self.lives_var.place(x=330, y=self.y)