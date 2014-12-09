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
frame = Tk()
frame.title("Pacman")
frame.geometry("850x850")
tahvel = Canvas(frame, width=850, height=850, bg="black")
tahvel.grid_forget()
menu = Canvas(frame, width=850, height=850, bg="black")
menu.grid()
over = Canvas(frame, width=850, height=850, bg="black")
over.grid_forget()

# meedia sisselugemine
immov_obj.wall_img = PhotoImage(file="media/wall.png")
immov_obj.pellet_img = PhotoImage(file="media/pellet.png")
immov_obj.menu_img = PhotoImage(file="media/menu.png")
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
moving_obj.ghost_imgs = [PhotoImage(file="media/ghosts/helle.png"),
                             PhotoImage(file="media/ghosts/vilo.png"),
                             PhotoImage(file="media/ghosts/niitsoo.png"),
                             PhotoImage(file="media/ghosts/prank.png"),
                             PhotoImage(file="media/ghosts/vene.png"),
                             PhotoImage(file="media/ghosts/ghost_eyes.png")]
thisgame = game(tahvel)
thisgame.parent = menu
thisgame.create_mainmenu()





def up_press(event):
    if thisgame.state == "game":
        moving_obj.pac.new_dir = [0,-10]
        moving_obj.pac.new_dir_imgs = moving_obj.pac_imgs[1]
    elif thisgame.state == "menu":
        thisgame.nextselection(-1)

def down_press(event):
    if thisgame.state == "game":
        moving_obj.pac.new_dir = [0,10]
        moving_obj.pac.new_dir_imgs = moving_obj.pac_imgs[2]
    elif thisgame.state == "menu":
        thisgame.nextselection(1)

def left_press(event):
    if thisgame.state == "game":
        moving_obj.pac.new_dir = [-10,0]
        moving_obj.pac.new_dir_imgs = moving_obj.pac_imgs[3]

def right_press(event):
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
            frame.destroy()
    elif thisgame.state == "game":
        thisgame.state = "pause"
    elif thisgame.state == "pause":
        thisgame.state = "game"
    elif thisgame.state == "over":
        thisgame.state = "menu"
        thisgame.parent = menu
        thisgame.create_mainmenu()

def escape_press(event):
    if thisgame.state == "menu":
        frame.destroy()
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
frame.bind_all("<Up>", up_press)
frame.bind_all("<Down>",  down_press)
frame.bind_all("<Left>",  left_press)
frame.bind_all("<Right>", right_press)
frame.bind_all("<space>", spacebar_press)
frame.bind_all("<Escape>", escape_press)


def uuenda():
    if thisgame.state == "game":
        for elem in moving_obj.ghosts:
            elem.move()
        moving_obj.pac.move()
        thisgame.score.config(text="SCORE:"+str(moving_obj.pac.score))
        thisgame.lives.config(text="LIVES:"+str(moving_obj.pac.lives))
    # ootame 0,1 sekundit ja siis uuendame positsiooni
    frame.after(80, uuenda)

uuenda()
frame.mainloop()