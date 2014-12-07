__author__ = 'Meelis Tapo'
__author__ = 'Eduard'

#TODO game over graafika, pluss mängu uuesti laadimine pärast elude kaotust
#TODO tondid loogika (chaser, ambusher, fickle, stupid)
#TODO menüü taoline asjandus/hiscore/etc
#TODO helid (kaustas olemas die.ogg, intro.ogg)
#TODO powerupid

from tkinter import *
from objects import *
from menu import *
paused = True

# akna loomine
raam = Tk()
raam.title("Pacman")
raam.geometry("850x850")
tahvel = Canvas(raam, width=850, height=800, background="black")
tahvel.grid()

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

def create_level(file="levels/001"):
    global pacm
    global ghosts
    ghosts = []
    x,y = 0,0
    levelfile = open(file)
    for line in levelfile:
        line = line.strip("\n")
        for elem in line:
            if elem == "#":
                immov_obj([x*50+25,y*50+25], tahvel, immov_obj.wall_img)
            elif elem == "o":
                immov_obj([x*50+25,y*50+25], tahvel, immov_obj.pellet_img, is_pellet=True)
            elif elem == "P":
                pacm = moving_obj([x*50+25,y*50+25], tahvel, moving_obj.pac_imgs[0][0], att="player", coll_ghost=True, coll_pel=True)
            elif elem == "S":
                ghosts.append(moving_obj([x*50+25,y*50+25], tahvel, moving_obj.ghost_imgs[0]))
            elif elem == "C":
                ghosts.append(moving_obj([x*50+25,y*50+25], tahvel, moving_obj.ghost_imgs[1]))
            elif elem == "T":
                ghosts.append(moving_obj([x*50+25,y*50+25], tahvel, moving_obj.ghost_imgs[2]))
            x += 1
        y += 1
        x = 0
    levelfile.close()
    #----------------------------------------------------------

def nool_üles(event):
    if not paused:
        pacm.new_dir = [0,-10]
        pacm.new_dir_imgs = moving_obj.pac_imgs[1]

def nool_alla(event):
    if not paused:
        pacm.new_dir = [0,10]
        pacm.new_dir_imgs = moving_obj.pac_imgs[2]

def nool_vasakule(event):
    if not paused:
        pacm.new_dir = [-10,0]
        pacm.new_dir_imgs = moving_obj.pac_imgs[3]

def nool_paremale(event):
    if not paused:
        pacm.new_dir = [10,0]
        pacm.new_dir_imgs = moving_obj.pac_imgs[0]

def pause(event):
    global paused
    if paused:
        paused = False
    else:
        paused = True

# seon nooleklahvid vastavate funktsioonidega
raam.bind_all("<Up>", nool_üles)
raam.bind_all("<Down>",  nool_alla)
raam.bind_all("<Left>",  nool_vasakule)
raam.bind_all("<Right>", nool_paremale)
raam.bind_all("<space>", pause)

def uuenda():
    global paused
    if not paused:
        for elem in moving_obj.ghosts:
            elem.move()
        pacm.move()
        menu.score_var.config(text=pacm.score)
        menu.lives_var.config(text=pacm.lives)
    # ootame 0,1 sekundit ja siis uuendame positsiooni
    raam.after(80, uuenda)

create_level()
menu = menu(raam)
uuenda()

# ilmutame akna ekraanile
raam.mainloop()