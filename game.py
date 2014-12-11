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
    def __init__(self, parent):
        self.state = "menu"         #mängu seisund, võib olla game/pause/menu
        self.parent = parent        #määrab, kuhu joonistatakse
        self.level = None           #level, võib olla bak/mag/dok
        self.selection = None       #peamenüü valik, 0-4
        self.menubuttons = []       #peamenüü nupud
        self.textobjects = []       #mängumenüü tekstiobjektid
        self.menu_font = font.Font(family='Helvetica', size=12, weight='bold')  #menüü tekstide kirjastiil
        self.warning_font = font.Font(family="Helvetica", size=10)              #hoiatuste kirjastiil
        self.highestlevelcompleted =                                            #raskeim läbitud level
        self.turns_to_show_warning = 0                                          #hoiatuse kuva aeg

    #----------------------------------------------------------------
    #leveli loomine
    #----------------------------------------------------------------
    def create_level(self):
        x, y = 0, 1
        #leveli failist sisselugemine
        levelfile = open("levels/"+ str(self.level))
        for line in levelfile:
            line = line.strip("\n")
            #leveli rea sümbolite objektideks muutmine
            for elem in line:
                if elem == "#":
                    immov_obj([x*50+25,y*50+25], self.parent, immov_obj.wall_bak_img, is_wall=True)
                if elem == "@":
                    immov_obj([x*50+25,y*50+25], self.parent, immov_obj.wall_mag_img, is_wall=True)
                if elem == "$":
                    immov_obj([x*50+25,y*50+25], self.parent, immov_obj.wall_dok_img, is_wall=True)
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
            if self.level != "bak": #kui level ei ole baka siis muudame tondid targemaks
                elem.att = "ai"
            elem.parent.tag_raise(elem.id)  #tontide tõstmine kuvamisel (enne tekkis konflikt pelletitega)

    #----------------------------------------------------------------
    #peamenüü selekteeriva noole liikumine
    #----------------------------------------------------------------
    def nextselection(self, dir):
        self.selection += dir
        if self.selection < 0:
            self.selection = 4
        if self.selection > 4:
            self.selection = 0
        self.selection_pointer.place(x=35, y=100+self.selection*40)

    #----------------------------------------------------------------
    #mängumenüü loomine (kuvatakse mänguakna päises)
    #----------------------------------------------------------------
    def create_gamemenu(self):
        self.eap = Label(self.parent, text="EAP:"+str(moving_obj.pac.eap), font=self.menu_font, fg="white", bg="black")
        self.warnings = Label(self.parent, text="HOIATUSI:"+str(moving_obj.pac.eap), font=self.menu_font, fg="white", bg="black")
        self.last_warning = Label(self.parent, text=None, font=self.warning_font, fg="red", bg="black")
        self.last_warning.place(x=200, y=10)
        self.warnings.place(x=5, y=10)
        self.eap.place(x=110, y=10)
        self.textobjects.append(self.eap)
        self.textobjects.append(self.warnings)
        self.textobjects.append(self.last_warning)

    #----------------------------------------------------------------
    #peamenüü loomine
    #----------------------------------------------------------------
    def create_mainmenu(self):
        self.selection = 0
        self.menubuttons.append(Label(self.parent, text="BAKLAUREUSEÕPE", font=self.menu_font, fg="white", bg="gray22"))
        self.menubuttons.append(Label(self.parent, text="MAGISTRANTUUR", font=self.menu_font, fg="white", bg="gray22"))
        self.menubuttons.append(Label(self.parent, text="DOKTORANTUUR", font=self.menu_font, fg="white", bg="gray22"))
        self.menubuttons.append(Label(self.parent, text="ABI", font=self.menu_font, fg="white", bg="gray22"))
        self.menubuttons.append(Label(self.parent, text="SULGE", font=self.menu_font, fg="white", bg="gray22"))
        self.selection_pointer = Label(self.parent, text=">", font=self.menu_font, fg="white", bg="gray22")
        for i in range(len(self.menubuttons)):
            self.menubuttons[i].place(x=50,y=100+i*40)
        self.selection_pointer.place(x=35, y=100+self.selection*40)
        immov_obj([425,425], self.parent, immov_obj.menu_img)

    #----------------------------------------------------------------
    #kaotussõnumi loomine (kuvatakse kui kogud levelis kolm hoiatust)
    #----------------------------------------------------------------
    def create_game_over_message(self):
        if self.level == 'bak':
            messagebox.showinfo(message="Eksmatt!\n"
                                        "Sinu koht pole ülikoolis, mine kutsekooli või küsi emme käest Austraalia pileti raha.")
        elif self.level == 'mag':
            messagebox.showinfo(message="Eksmatt!\n"
                                        "Ma ütlesin ju, et sa ei saa hakkama. Mine tööle ahv!")
        elif self.level == 'dok':
            messagebox.showinfo(message="Eksmatt!\n"
                                        "Meie riik on liiga vaene, et sinusuguseid luusereid siin aastate kaupa koolitada.")

    #----------------------------------------------------------------
    #võidusõnumi loomine (kuvatakse leveli läbimisel)
    #----------------------------------------------------------------
    def create_victory_message(self):
        if self.level == 'bak':
            messagebox.showinfo(message="Palju õnne! Omandasid bakalaureuse kraadi!\n"
                                        "Yesss! Oled nüüd paberitega mees. Piduuu!")
        elif self.level == 'mag':
            messagebox.showinfo(message="Palju õnne! Omandasid magistrikraadi!\n"
                                        "Respect! Igaüks nii kaugele ei jõua.")
        elif self.level == 'dok':
            messagebox.showinfo(message="Palju õnne! Omandasid doktorikraadi!\n"
                                        "You win! See ülikool ei ole sinu vääriline.")

    #----------------------------------------------------------------
    #tähelepanusõnumi loomine (kuvatakse kui üritad mängida levelit, milleks sul pole õigusi)
    #----------------------------------------------------------------
    def create_attention_message(self):
        if self.selection == 1:
            messagebox.showwarning(message = "Oot, oot, enne pead ikka baka kraadi kätte saama!")
        else:
            messagebox.showwarning(message = "Mingi eilane oled vä? Doktorantuuri saad ainult magistrikraadiga!")

    #----------------------------------------------------------------
    #abisõnumi loomine (kuvatakse peamenüüst 'Abi' valimisel)
    #----------------------------------------------------------------
    def create_help_message(self):
        messagebox.showinfo(message="Juhend:\n"
                                    "Pacversity on mäng, milles sinu poolt juhitud Pacman proovib omandada kõrgharidust. Mängu eesmärk on kokku korjata kõik "
                                    "õppeastmes jagatavad ainepunktid (rohelised rõngad) ja vältida seejuures konflikte teenindava personaliga. "
                                    "Käitu korralikult, sest juba kolm hoiatust toovad kaasa eksmatrikuleerimise.\nVaata järgi, kas sinus on PhD materjali!\n"
                                    "\n"
                                    "Disclaimer:\n"
                                    "Pacversity loomel on vaadatud läbi huumoriprisma. Kõik dialoogid on fiktsionaalsed, ega oma mingisugust"
                                    "isiklikku tähendust väljaspool selle mängu konteksti.\n"
                                    "\n"
                                    "Nupud:\n"
                                    "Menüü - üles-alla liikumiseks kasuta nooli, selekteerimiseks vajuta 'Space' või 'Enter', mängu sulgemiseks 'Esc'.\n"
                                    "Mäng - liikumiseks kasuta nooli, vahepausi alustamiseks või lõpetamiseks vajuta 'Space' või 'Enter', 'Esc' viib sind tagasi peamenüüsse.\n"
                                    "\n"
                                    "Mängu autorid:\n"
                                    "Eduard Šengals, Meelis Tapo 2014")