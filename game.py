__author__ = 'Eduard'
from objects import *
from tkinter import Label
from tkinter import font

class game:
    allobjects = []
    def __init__(self, parent):
        self.state = "menu" #game/over/pause/menu
        self.level = "001"
        self.parent = parent
        self.selection = None
        self.menubuttons = []
        self.font = font.Font(family='Helvetica', size=12, weight='bold')

    def create_level(self):
        x, y = 0, 1
        levelfile = open("levels/"+self.level)
        for line in levelfile:
            line = line.strip("\n")
            for elem in line:
                if elem == "#":
                    immov_obj([x*50+25,y*50+25], self.parent, immov_obj.wall_img)
                elif elem == "o":
                    immov_obj([x*50+25,y*50+25], self.parent, immov_obj.pellet_img, is_pellet=True)
                elif elem == "P":
                    moving_obj([x*50+25,y*50+25], self.parent, moving_obj.pac_imgs[0][0], att="player", coll_ghost=True, coll_pel=True)
                elif elem == "S":
                    moving_obj([x*50+25,y*50+25], self.parent, moving_obj.ghost_imgs[0])
                elif elem == "C":
                    moving_obj([x*50+25,y*50+25], self.parent, moving_obj.ghost_imgs[1])
                elif elem == "T":
                    moving_obj([x*50+25,y*50+25], self.parent, moving_obj.ghost_imgs[2])
                x += 1
            y += 1
            x = 0
        levelfile.close()

    def nextselection(self, dir):
        self.selection += dir
        if self.selection < 0:
            self.selection = 3
        if self.selection > 3:
            self.selection = 0
        self.selection_pointer.place(x=35, y=300+self.selection*40)

    def create_gamemenu(self):
        self.score = Label(self.parent, text="SCORE:"+str(moving_obj.pac.score), font=self.font, fg="white", bg="black")
        self.lives = Label(self.parent, text="LIVES:"+str(moving_obj.pac.score), font=self.font, fg="white", bg="black")
        self.lives.place(x=35, y=15)
        self.score.place(x=125, y=15)
        self.allobjects.append(self.score)
        self.allobjects.append(self.lives)

    def create_mainmenu(self):
        self.selection = 0
        self.menubuttons.append(Label(self.parent, text="PLAY", font=self.font, fg="white", bg="black"))
        self.menubuttons.append(Label(self.parent, text="LEVEL: 001", font=self.font, fg="white", bg="black"))
        self.menubuttons.append(Label(self.parent, text="HELP", font=self.font, fg="white", bg="black"))
        self.menubuttons.append(Label(self.parent, text="EXIT", font=self.font, fg="white", bg="black"))
        self.selection_pointer = Label(self.parent, text=">", font=self.font, fg="white", bg="black")
        for i in range(len(self.menubuttons)):
            self.menubuttons[i].place(x=50,y=300+i*40)
        self.selection_pointer.place(x=35, y=300+self.selection*40)

    def create_overmenu(self):
        pass


