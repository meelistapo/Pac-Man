__author__ = 'Meelis Tapo'
__author__ = 'Eduard'

#TODO game over graafika, pluss mängu uuesti laadimine pärast elude kaotust
#TODO tondid loogika (chaser, ambusher, fickle, stupid)
#TODO menüü taoline asjandus/hiscore/etc
#TODO helid (kaustas olemas die.ogg, intro.ogg)
#TODO powerupid

from tkinter import *
from game import *
from objects import *

# akna loomine
raam = Tk()
raam.title("Pacman")
raam.geometry("850x850")
tahvel = Canvas(raam, width=850, height=850, bg="black")
tahvel.grid_forget()
menu = Canvas(raam, width=850, height=850, bg="black")
menu.grid()
over = Canvas(raam, width=850, height=850, bg="black")
over.grid_forget()

# meedia sisselugemine
immov_obj.wall_img = PhotoImage(file="media/wall.png")
immov_obj.pellet_img = PhotoImage(file="media/pellet.png")
moving_obj.pac_imgs.append([PhotoImage(file="media/pacs/pac_e_1.png"),
                            PhotoImage(file="media/pacs/pac_e_2.png"),
                            PhotoImage(file="media/pacs/pac_e_3.png"),
                            PhotoImage(file="media/pacs/pac_e_4.png")])
moving_obj.pac_imgs.append([PhotoImage(file="media/pacs/pac_n_1.png"),
                            PhotoImage(file="media/pacs/pac_n_2.png"),
                            PhotoImage(file="media/pacs/pac_n_3.png"),
                            PhotoImage(file="media/pacs/pac_n_4.png")])
moving_obj.pac_imgs.append([PhotoImage(file="media/pacs/pac_s_1.png"),
                            PhotoImage(file="media/pacs/pac_s_2.png"),
                            PhotoImage(file="media/pacs/pac_s_3.png"),
                            PhotoImage(file="media/pacs/pac_s_4.png")])
moving_obj.pac_imgs.append([PhotoImage(file="media/pacs/pac_w_1.png"),
                            PhotoImage(file="media/pacs/pac_w_2.png"),
                            PhotoImage(file="media/pacs/pac_w_3.png"),
                            PhotoImage(file="media/pacs/pac_w_4.png")])
moving_obj.ghost_imgs = [PhotoImage(file="media/ghosts/ghost_red.png"),
                             PhotoImage(file="media/ghosts/ghost_green.png"),
                             PhotoImage(file="media/ghosts/ghost_orange.png"),
                             PhotoImage(file="media/ghosts/ghost_pink.png"),
                             PhotoImage(file="media/ghosts/ghost_blue.png"),
                             PhotoImage(file="media/ghosts/ghost_eyes.png")]
thisgame = game(tahvel)
thisgame.parent=menu
thisgame.create_mainmenu()

def nool_üles(event):
    if thisgame.state == "game":
        moving_obj.pac.new_dir = [0,-10]
        moving_obj.pac.new_dir_imgs = moving_obj.pac_imgs[1]
    elif thisgame.state == "menu":
        thisgame.nextselection(-1)

def nool_alla(event):
    if thisgame.state == "game":
        moving_obj.pac.new_dir = [0,10]
        moving_obj.pac.new_dir_imgs = moving_obj.pac_imgs[2]
    elif thisgame.state == "menu":
        thisgame.nextselection(1)

def nool_vasakule(event):
    if thisgame.state == "game":
        moving_obj.pac.new_dir = [-10,0]
        moving_obj.pac.new_dir_imgs = moving_obj.pac_imgs[3]

def nool_paremale(event):
    if thisgame.state == "game":
        moving_obj.pac.new_dir = [10,0]
        moving_obj.pac.new_dir_imgs = moving_obj.pac_imgs[0]

def spacebar_press(event):
    if thisgame.state == "menu":
        if thisgame.selection == 0:
            menu.grid_forget()
            thisgame.parent = tahvel
            tahvel.grid()
            thisgame.create_level()
            thisgame.create_gamemenu()
            thisgame.state = "game"
        elif thisgame.selection == 1:
            pass
        elif thisgame.selection == 2:
            pass
        elif thisgame.selection == 3:
            raam.destroy()
    elif thisgame.state == "game":
        thisgame.state = "pause"
    elif thisgame.state == "pause":
        thisgame.state = "game"
    elif thisgame.state == "over":
        pass #tagasi algmenüüsse

def escape_press(event):
    if thisgame.state == "menu":
        raam.destroy()
    elif thisgame.state != "menu":
        thisgame.state = "menu"
        for elem in immov_obj.walls:
            tahvel.delete(elem)
        for elem in immov_obj.pellets:
            tahvel.delete(elem)
        for elem in moving_obj.ghosts:
            tahvel.delete(elem.id)
        tahvel.delete(moving_obj.pac.id)
        immov_obj.walls = {}
        immov_obj.pellets = {}
        moving_obj.pac = None
        moving_obj.ghosts = []
        moving_obj.moving = []
        for elem in game.allobjects:
            elem.config(text="")
        thisgame.parent = menu
        tahvel.grid_forget()
        menu.grid()

# seon nooleklahvid vastavate funktsioonidega
raam.bind_all("<Up>", nool_üles)
raam.bind_all("<Down>",  nool_alla)
raam.bind_all("<Left>",  nool_vasakule)
raam.bind_all("<Right>", nool_paremale)
raam.bind_all("<space>", spacebar_press)
raam.bind_all("<Escape>", escape_press)

def uuenda():
    if thisgame.state == "game":
        for elem in moving_obj.ghosts:
            elem.move()
        moving_obj.pac.move()
        thisgame.score.config(text="SCORE:"+str(moving_obj.pac.score))
        thisgame.lives.config(text="LIVES:"+str(moving_obj.pac.lives))
    # ootame 0,1 sekundit ja siis uuendame positsiooni
    raam.after(80, uuenda)

uuenda()
raam.mainloop()