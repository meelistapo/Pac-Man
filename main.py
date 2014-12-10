__author__ = 'Meelis Tapo'
__author__ = 'Eduard Šengals'

from tkinter import *
from game import *
from objects import *
from random import randint

# akna loomine
frame = Tk()
frame.title("Pacversity")
frame.geometry("850x850")
tahvel = Canvas(frame, width=850, height=850, bg="black")
menu = Canvas(frame, width=850, height=850, bg="black")
menu.grid()

# meedia sisselugemine
immov_obj.wall_img = PhotoImage(file="media/wall.png")
immov_obj.pellet_img = PhotoImage(file="media/pellet.png")
immov_obj.menu_img = PhotoImage(file="media/menu.png")
moving_obj.pac_imgs.append([PhotoImage(file="media/pacs/pac_e_1.png"),
                            PhotoImage(file="media/pacs/pac_e_2.png")])
moving_obj.pac_imgs.append([PhotoImage(file="media/pacs/pac_n_1.png"),
                            PhotoImage(file="media/pacs/pac_n_2.png")])
moving_obj.pac_imgs.append([PhotoImage(file="media/pacs/pac_s_1.png"),
                            PhotoImage(file="media/pacs/pac_s_2.png")])
moving_obj.pac_imgs.append([PhotoImage(file="media/pacs/pac_w_1.png"),
                            PhotoImage(file="media/pacs/pac_w_2.png")])
moving_obj.ghost_imgs =[PhotoImage(file="media/ghosts/vilo.png"),
                            PhotoImage(file="media/ghosts/vene.png"),
                            PhotoImage(file="media/ghosts/prank.png"),
                            PhotoImage(file="media/ghosts/niitsoo.png"),
                            PhotoImage(file="media/ghosts/hein.png"),
                            PhotoImage(file="media/ghosts/plank.png"),
                            PhotoImage(file="media/ghosts/tamm.png"),
                            PhotoImage(file="media/ghosts/nolv.png"),
                            PhotoImage(file="media/ghosts/pungas.png"),
                            PhotoImage(file="media/ghosts/paales.png"),
                            PhotoImage(file="media/ghosts/annamaa.png"),
                            PhotoImage(file="media/ghosts/palm.png")]
textfile = open("media/texts.txt", encoding="utf-8")
ghostmsg = {}
for line in textfile:
    ghostmsg[line.split(": ")[0].lstrip("\ufeff")] = line.split(": ")[1].split("; ")
textfile.close()

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
            thisgame.level = 'baka'
            thisgame.create_level()
            thisgame.create_gamemenu()
            thisgame.state = "game"
        elif thisgame.selection == 1:
            if thisgame.highestlevelcompleted != None:
                menu.grid_forget()
                thisgame.parent = tahvel
                tahvel.grid()
                thisgame.level = 'mag'
                thisgame.create_level()
                thisgame.create_gamemenu()
                thisgame.state = "game"
            else:
                thisgame.create_attention_message()
        elif thisgame.selection == 2:
            if thisgame.highestlevelcompleted == "mag":
                menu.grid_forget()
                thisgame.parent = tahvel
                tahvel.grid()
                thisgame.level = 'dok'
                thisgame.create_level()
                thisgame.create_gamemenu()
                thisgame.state = "game"
            else:
                thisgame.create_attention_message()
        elif thisgame.selection == 3:
            thisgame.create_help_message()
        elif thisgame.selection == 4:
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
frame.bind_all("<Return>", spacebar_press)


def uuenda():
    if thisgame.state == "game":
        for elem in moving_obj.ghosts:
            elem.move(thisgame)
        moving_obj.pac.move(thisgame)
        thisgame.ainepunktid.config(text="EAP: "+str(int(moving_obj.pac.ainepunktid)))
        thisgame.hoiatused.config(text="HOIATUSI: "+str(moving_obj.pac.hoiatused))
        if moving_obj.pac.coll_name != None:
            hoiatus = ghostmsg[moving_obj.pac.coll_name][randint(0,1)]
            if '|' in hoiatus:
                warning = hoiatus.split('|')
                hoiatus = warning[0]+'\n'+warning[1].strip()
            thisgame.viimanehoiatus.config(text=hoiatus, justify='left')
            thisgame.turns_to_show_warning = 120
            moving_obj.pac.coll_name = None
        if thisgame.turns_to_show_warning:
            thisgame.turns_to_show_warning -= 1
        else:
            thisgame.viimanehoiatus.config(text="")
        if moving_obj.pac.hoiatused == 3:
            thisgame.state = "pause"
            thisgame.create_gameover_message()
            escape_press("<Escape>")
        if thisgame.state == "game" and len(immov_obj.pellets) == 0:
            thisgame.state = "pause"
            thisgame.create_victory_message()
            escape_press("<Escape>")
            if thisgame.level == 'baka':
                thisgame.highestlevelcompleted = 'baka'
                thisgame.selection_pointer.place(x=35, y=100+1*40)
                thisgame.selection = 1
            elif thisgame.level == 'mag':
                thisgame.highestlevelcompleted = 'mag'
                thisgame.selection_pointer.place(x=35, y=100+2*40)
                thisgame.selection = 2
            else:
                thisgame.selection_pointer.place(x=35, y=100+4*40)
                thisgame.selection = 4

    # ootame 0,06 sekundit ja siis uuendame positsiooni
    if thisgame.level == "dok":
        frame.after(60, uuenda)
    else:
        frame.after(80, uuenda)

uuenda()
frame.mainloop()