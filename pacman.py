__author__ = 'Meelis Tapo'

from tkinter import *
import time
import random

sammu_pikkus = 50
alg_pos = [275,275]
wall_pos = ([25,25], [25,75], [25,125], [25,175],[25,225], [25,275], [25,325], [25,375], [25,425], [25,475], [25,525],
            [525,25], [525,75], [525,125], [525,175],[525,225], [525,275], [525,325], [525,375], [525,425], [525,475], [525,525],
            [75,25],[125,25],[175,25],[225,25],[275,25],[325,25],[375,25],[425,25],[475,25],
            [75,525], [125,525],[175,525],[225,525],[275,525],[325,525],[375,525],[425,525],[475,525],
            [125,125], [175,125], [225,125], [275,125], [325,125], [375,125], [425,125],
            [125,425], [175,425], [225,425], [275,425], [325,425], [375,425], [425,425])

pac_pos = [alg_pos[0], alg_pos[1]]
ghost_pos = [175,275]

# loome akna
raam = Tk()
raam.title("Pacman")
raam.geometry("700x700")
tahvel = Canvas(raam, width=550, height=550, background="blue")
tahvel.grid(column=3, row=5, columnspan=5, rowspan=5, sticky=(N, S, W, E))



def samm(pos,):
    üles = [pos[0], pos[1]-sammu_pikkus]
    alla = [pos[0], pos[1]+sammu_pikkus]
    vasakule = [pos[0]-sammu_pikkus, pos[1]]
    paremale = [pos[0]+sammu_pikkus, pos[1]]
    return üles, alla, vasakule, paremale


def nool_üles(event):
    global pac_pos
    if wall(samm(pac_pos)[0]) != True:
        tahvel.move(pac_id, 0, -sammu_pikkus)
        pac_pos[1] -= sammu_pikkus
        print(pac_pos)

def nool_alla(event):
    global pac_pos
    if wall(samm(pac_pos)[1]) != True:
        tahvel.move(pac_id, 0, sammu_pikkus)
        pac_pos[1] += sammu_pikkus
        print(pac_pos)

def nool_vasakule(event):
    global pac_pos
    if wall(samm(pac_pos)[2]) != True:
        tahvel.move(pac_id, -sammu_pikkus, 0)
        pac_pos[0] -= sammu_pikkus
        print(pac_pos)

def nool_paremale(event):
    global pac_pos
    if wall(samm(pac_pos)[3]) != True:
        tahvel.move(pac_id, sammu_pikkus, 0)
        pac_pos[0] += sammu_pikkus
        print(pac_pos)

def wall(pos):
    for i in range(len(wall_pos)):
        if wall_pos[i][0] == pos[0] and wall_pos[i][1] == pos[1]:
            return True
    return False


# tavaline pildi sisselugemine
pac_img = PhotoImage(file="pac1.png")
wall_img = PhotoImage(file="wall.png")
ghost_img = PhotoImage(file="ghost.png")

# pildi loomisel jätan meelde pildi id
pac_id = tahvel.create_image(alg_pos[0], alg_pos[1], image=pac_img)
ghost_id = tahvel.create_image(ghost_pos[0], ghost_pos[1], image=ghost_img)

wall_id =[]
for i in range(len(wall_pos)):
    wall_id.append(tahvel.create_image(wall_pos[i][0], wall_pos[i][1], image=wall_img))


# seon nooleklahvid vastavate funktsioonidega
raam.bind_all("<Up>",    nool_üles)
raam.bind_all("<Down>",  nool_alla)
raam.bind_all("<Left>",  nool_vasakule)
raam.bind_all("<Right>", nool_paremale)

liigu = ['üles','alla','vasakule','paremale']

def liikumine(indeks):
    if liigu[indeks] == 'üles':
        return [0,-sammu_pikkus]
    elif liigu[indeks] == 'alla':
        return [0,+sammu_pikkus]
    elif liigu[indeks] == 'vasakule':
        return [-sammu_pikkus,0]
    elif liigu[indeks] == 'paremale':
        return [+sammu_pikkus,0]




def uuenda():
    global ghost_pos
    print(ghost_pos)
    indeks = random.randint(0,3)
    kuhu = liikumine(indeks)
    if wall(samm(ghost_pos)[indeks]) != True:
        ghost_pos[0] += kuhu[0]
        ghost_pos[1] += kuhu[1]
        tahvel.move(ghost_id,kuhu[0],kuhu[1])

    # ootame 0,1 sekundit ja siis uuendame positsiooni
    raam.after(10, uuenda)

uuenda()




# ilmutame akna ekraanile
raam.mainloop()