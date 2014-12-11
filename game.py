__author__ = 'Meelis Tapo'
__author__ = 'Eduard Šengals'
from objects import *
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import Label
from tkinter import font
import random

class game:
    allobjects = []
    def __init__(self, parent):
        self.state = "menu" #game/over/pause/menu
        self.parent = parent
        self.level = None
        self.selection = None
        self.menubuttons = []
        self.font = font.Font(family='Helvetica', size=12, weight='bold')
        self.warning_font = font.Font(family="Helvetica", size=10)
        self.highestlevelcompleted = None
        self.turns_to_show_warning = 0

    def create_level(self):
        x, y = 0, 1
        levelfile = open("levels/"+ str(self.level))
        for line in levelfile:
            line = line.strip("\n")
            for elem in line:
                if elem == "#":
                    immov_obj([x*50+25,y*50+25], self.parent, immov_obj.wall_img, is_wall=True)
                elif elem == "o":
                    immov_obj([x*50+25,y*50+25], self.parent, immov_obj.pellet_img, is_pellet=True)
                elif elem == "P":
                    moving_obj([x*50+25,y*50+25], self.parent, moving_obj.pac_imgs[0][0], att="player", coll_ghost=True, coll_pel=True)
                elif elem == "V":
                    moving_obj([x*50+25,y*50+25], self.parent, moving_obj.ghost_imgs[0], name='vilo')
                elif elem == "W":
                    moving_obj([x*50+25,y*50+25], self.parent, moving_obj.ghost_imgs[1], name='vene')
                elif elem == "R":
                    moving_obj([x*50+25,y*50+25], self.parent, moving_obj.ghost_imgs[2], name='prank')
                elif elem == "N":
                    moving_obj([x*50+25,y*50+25], self.parent, moving_obj.ghost_imgs[3], name='niitsoo')
                elif elem == "H":
                    moving_obj([x*50+25,y*50+25], self.parent, moving_obj.ghost_imgs[4], name='hein')
                elif elem == "L":
                    moving_obj([x*50+25,y*50+25], self.parent, moving_obj.ghost_imgs[5], name='plank')
                elif elem == "T":
                    moving_obj([x*50+25,y*50+25], self.parent, moving_obj.ghost_imgs[6], name='tamm')
                elif elem == "O":
                    moving_obj([x*50+25,y*50+25], self.parent, moving_obj.ghost_imgs[7], name='nolv')
                elif elem == "U":
                    moving_obj([x*50+25,y*50+25], self.parent, moving_obj.ghost_imgs[8], name='pungas')
                elif elem == "E":
                    moving_obj([x*50+25,y*50+25], self.parent, moving_obj.ghost_imgs[9], name='paales')
                elif elem == "A":
                    moving_obj([x*50+25,y*50+25], self.parent, moving_obj.ghost_imgs[10], name='annamaa')
                elif elem == "M":
                    moving_obj([x*50+25,y*50+25], self.parent, moving_obj.ghost_imgs[11], name='palm')
                x += 1
            y += 1
            x = 0
        levelfile.close()
        for elem in moving_obj.ghosts:
            if self.level != "baka":
                elem.att = "ai"
            elem.parent.tag_raise(elem.id)

    def nextselection(self, dir):
        self.selection += dir
        if self.selection < 0:
            self.selection = 4
        if self.selection > 4:
            self.selection = 0
        self.selection_pointer.place(x=35, y=100+self.selection*40)

    def create_gamemenu(self):
        self.ainepunktid = Label(self.parent, text="EAP:"+str(moving_obj.pac.ainepunktid), font=self.font, fg="white", bg="black")
        self.hoiatused = Label(self.parent, text="HOIATUSI:"+str(moving_obj.pac.ainepunktid), font=self.font, fg="white", bg="black")
        self.viimanehoiatus = Label(self.parent, text=None, font=self.warning_font, fg="red", bg="black")
        self.viimanehoiatus.place(x=200, y=10)
        self.hoiatused.place(x=5, y=10)
        self.ainepunktid.place(x=110, y=10)
        self.allobjects.append(self.ainepunktid)
        self.allobjects.append(self.hoiatused)
        self.allobjects.append(self.viimanehoiatus)

    def create_mainmenu(self):
        self.selection = 0
        self.menubuttons.append(Label(self.parent, text="BAKALAUREUSEÕPE", font=self.font, fg="white", bg="gray22"))
        self.menubuttons.append(Label(self.parent, text="MAGISTRANTUUR", font=self.font, fg="white", bg="gray22"))
        self.menubuttons.append(Label(self.parent, text="DOKTORANTUUR", font=self.font, fg="white", bg="gray22"))
        self.menubuttons.append(Label(self.parent, text="ABI", font=self.font, fg="white", bg="gray22"))
        self.menubuttons.append(Label(self.parent, text="SULGE", font=self.font, fg="white", bg="gray22"))
        self.selection_pointer = Label(self.parent, text=">", font=self.font, fg="white", bg="gray22")
        for i in range(len(self.menubuttons)):
            self.menubuttons[i].place(x=50,y=100+i*40)
        self.selection_pointer.place(x=35, y=100+self.selection*40)
        immov_obj([425,425], self.parent, immov_obj.menu_img)

    def create_gameover_message(self):
        if self.level == 'baka':
            messagebox.showinfo(message="Eksmatt!\n"
                                        "Sinu koht pole ülikoolis, mine kutsekooli või küsi emme käest Austraalia pileti raha.")
        elif self.level == 'mag':
            messagebox.showinfo(message="Eksmatt!\n"
                                        "Ma ütlesin ju, et sa ei saa hakkama. Mine tööle ahv!")
        elif self.level == 'dok':
            messagebox.showinfo(message="Eksmatt!\n"
                                        "Meie riik on liiga vaene, et sinusuguseid luusereid siin aastate kaupa koolitada.")

    def create_victory_message(self):
        if self.level == 'baka':
            messagebox.showinfo(message="Palju õnne! Omandasid bakalaureuse kraadi!\n"
                                        "Yesss! Oled nüüd paberitega mees. Piduuu!")
        elif self.level == 'mag':
            messagebox.showinfo(message="Palju õnne! Omandasid magistrikraadi!\n"
                                        "Respect! Igaüks nii kaugele ei jõua.")
        elif self.level == 'dok':
            messagebox.showinfo(message="Palju õnne! Omandasid doktorikraadi!\n"
                                        "You win! See ülikool ei ole sinu vääriline.")

    def create_attention_message(self):
        if self.selection == 1:
            messagebox.showwarning(message = "Oot, oot, enne pead ikka baka kraadi kätte saama!")
        else:
            messagebox.showwarning(message = "Mingi eilane oled vä? Doktorantuuri saad ainult magistrikraadiga!")
    def create_help_message(self):
        messagebox.showinfo(message="Pacversity õpetus:\n"
                                    "\n"
                                    "Pacversity on mäng, milles sinu poolt juhitud Pacman proovib omandada kõrgharidust. Mängu eesmärk on kokku korjata kõik "
                                    "õppeastmes jagatavad ainepunktid (rohelised rõngad) ja vältida seejuures konflikte teenindava personaliga. "
                                    "Käitu korralikult, sest juba kolm hoiatust toovad kaasa eksmatrikuleerimise.\nVaata järgi, kas sinus on PhD materjali!\n"
                                    "\n"
                                    "Disclaimer: Pacversity loomel on vaadatud läbi huumoriprisma. Kõik dialoogid on fiktsionaalsed, ega oma mingisugust\n"
                                    "isiklikku tähendust väljaspool selle mängu konteksti."
                                    "\n"
                                    "\n"
                                    "Nupud:\n"
                                    "\n"
                                    "Menüü - üles-alla liikumiseks kasuta nooli, selekteerimiseks vajuta 'Space' või 'Enter', mängu sulgemiseks 'Esc'.\n"
                                    "Mäng - liikumiseks kasuta nooli, vahepausi alustamiseks või lõpetamiseks vajuta 'Space' või 'Enter', 'Esc' viib sind tagasi peamenüüsse.\n"
                                    "\n"
                                    "Mängu autorid:\n"
                                    "Eduard Šengals, Meelis Tapo 2014")



