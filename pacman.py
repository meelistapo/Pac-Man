__author__ = 'Meelis Tapo'
__author__ = 'Eduard'

#TODO game over graafika, pluss mängu uuesti laadimine pärast elude kaotust
#TODO tondid parkinsonist terveks ravida/loogika (chaser, ambusher, fickle, stupid)
#TODO tonte juurde
#TODO kaardisüsteem ümber(50*50px ruudud? i*50-25), kaardid suuremaks ja juurde
#TODO menüü taoline asjandus/hiscore/etc
#TODO nupu allavajutamisel astub 1 sammu, siis jõnksatab korraks seisma, siis liigub sujuvalt edasi, wot?
#TODO helid (kaustas olemas die.ogg, intro.ogg)
#TODO pelletid/powerupid
#TODO loogika eraldi faili?
#TODO ülikooli teema kujunduses
#TODO erinevad raskusastmed


from tkinter import *
from tkinter import ttk
from tkinter import font
import random

# akna loomine
raam = Tk()
raam.title("Pacman")
raam.geometry("550x600")
tahvel = Canvas(raam, width=550, height=550, background="blue")
tahvel.grid()



# meedia sisselugemine
pac1_east_img = PhotoImage(file="media/pac1_e.png")
pac1_west_img = PhotoImage(file="media/pac1_w.png")
pac1_north_img = PhotoImage(file="media/pac1_n.png")
pac1_south_img = PhotoImage(file="media/pac1_s.png")
pac2_east_img = PhotoImage(file="media/pac2_e.png")
pac2_west_img = PhotoImage(file="media/pac2_w.png")
pac2_north_img = PhotoImage(file="media/pac2_n.png")
pac2_south_img = PhotoImage(file="media/pac2_s.png")
wall_img = PhotoImage(file="media/wall.png")
ghost_img = PhotoImage(file="media/ghost.png")
pellet_img = PhotoImage(file="media/pellet.png")


# globaalsed muutujad
pac_step = 5
ghost_step = 50
pac_pos = [275,275]
ghost_pos = [175,275]
pac_pics =[pac1_east_img, pac1_east_img]
current_pic = pac_pics[0]
score = 0
lives = 3
trigger=True


# leveli kujunduse loomine
wall_pos = ([25,25], [25,75], [25,125], [25,175],[25,225], [25,275], [25,325], [25,375], [25,425], [25,475], [25,525],
            [525,25], [525,75], [525,125], [525,175],[525,225], [525,275], [525,325], [525,375], [525,425], [525,475], [525,525],
            [75,25],[125,25],[175,25],[225,25],[275,25],[325,25],[375,25],[425,25],[475,25],
            [75,525], [125,525],[175,525],[225,525],[275,525],[325,525],[375,525],[425,525],[475,525],
            [125,125], [175,125], [225,125], [275,125], [325,125], [375,125], [425,125],
            [125,425], [175,425], [225,425], [275,425], [325,425], [375,425], [425,425])

pellet_pos = [[175,475],[225,475],[275,475],[325,475],[375,475],
              [175,75],[225,75],[275,75],[325,75],[375,75]]

wall_id =[]
for i in range(len(wall_pos)):
    wall_id.append(tahvel.create_image(wall_pos[i][0], wall_pos[i][1], image=wall_img))

pellet_id = []
for i in range(len(pellet_pos)):
    pellet_id.append(tahvel.create_image(pellet_pos[i][0], pellet_pos[i][1], image=pellet_img))

# objektide loomine
pac_id = tahvel.create_image(pac_pos[0], pac_pos[1], image=current_pic)
ghost_id = tahvel.create_image(ghost_pos[0], ghost_pos[1], image=ghost_img)


minu_font = font.Font(family='Helvetica', size=12, weight='bold')
silt = ttk.Label(raam, text="Score:", font=minu_font)
silt.place(x=175, y=565)
silt1 = ttk.Label(raam, text="Lives:", font=minu_font)
silt1.place(x=275, y=565)




# liikumine
def samm(pos):
    üles = [pos[0], pos[1]-pac_step]
    alla = [pos[0], pos[1]+pac_step]
    vasakule = [pos[0]-pac_step, pos[1]]
    paremale = [pos[0]+pac_step, pos[1]]
    return üles, alla, vasakule, paremale


def nool_üles(event):
    global pac_pos, pac_pics
    if not wall2(samm(pac_pos)[0]):
        tahvel.move(pac_id, 0, -pac_step)
        pac_pos[1] -= pac_step
        pac_pics = [pac1_north_img, pac2_north_img]

def nool_alla(event):
    global pac_pos, pac_pics
    if not wall2(samm(pac_pos)[1]):
        tahvel.move(pac_id, 0, pac_step)
        pac_pos[1] += pac_step
        pac_pics = [pac1_south_img, pac2_south_img]

def nool_vasakule(event):
    global pac_pos, pac_pics
    if not wall2(samm(pac_pos)[2]):
        tahvel.move(pac_id, -pac_step, 0)
        pac_pos[0] -= pac_step
        pac_pics = [pac1_west_img, pac2_west_img]

def nool_paremale(event):
    global pac_pos, pac_pics
    if not wall2(samm(pac_pos)[3]):
        tahvel.move(pac_id, pac_step, 0)
        pac_pos[0] += pac_step
        pac_pics = [pac1_east_img, pac2_east_img]

def release_key(event):
    global pac_pics
    pac_pics[1] = pac_pics[0]


liigu = ['üles','alla','vasakule','paremale']

def liikumine(indeks):
    if liigu[indeks] == 'üles':
        return [0,-ghost_step]
    elif liigu[indeks] == 'alla':
        return [0,+ghost_step]
    elif liigu[indeks] == 'vasakule':
        return [-ghost_step,0]
    elif liigu[indeks] == 'paremale':
        return [+ghost_step,0]

# def wall(pos): # ei kasuta seda enam
#     for i in range(len(wall_pos)):
#         if wall_pos[i][0] == pos[0] and wall_pos[i][1] == pos[1]:
#             return True
#     return False

def wall2(pos):
    for wall_elem in wall_pos:
        if collision(pos, wall_elem):
            return True
    return False


#ruut 50px x 50 px, kus koordinaadid on ruudu keskpunktiks.
#tipud on vastava ümbrisruudu tipud (nt pos 25x25 puhul 0x0, 0x50, 50x0, 50x50)
def tipud(pos):
    tipud = []
    tipud.append([pos[0]-25, pos[1]-25]) # Ül Vas
    tipud.append([pos[0]-25, pos[1]+25]) # Al Vas
    tipud.append([pos[0]+25, pos[1]-25]) # Ül Par
    tipud.append([pos[0]+25, pos[1]+25]) # Al Par
    #külgede keskpunktid
    tipud.append([pos[0], pos[1]-25])
    tipud.append([pos[0], pos[1]+25])
    tipud.append([pos[0]-25, pos[1]])
    tipud.append([pos[0]+25, pos[1]])
    return tipud
#kontrollib 2 objekti kokkupõrget
#kontrollib kas ühe objekti mingi piirnurk asub teise objekti piirides
def collision(pos_obj1, pos_obj2):
    tipud_obj1 = tipud(pos_obj1)
    for elem in tipud_obj1:
        if elem[0] > pos_obj2[0]-25 and elem[0] < pos_obj2[0]+25:
            if elem[1] > pos_obj2[1]-25 and elem[1] < pos_obj2[1]+25:
                return True
    #eraldi kontroll -OK, lisaks elemendi ümbrisnelinurga tippudele kontrollib ka külgede keskpunkte

def remove_pellets(pellet_pos, pac_pos):
    global score
    for i in range(len(pellet_pos)):
        if abs(pellet_pos[i][0] - pac_pos[0]) < 40 and abs(pellet_pos[i][1] - pac_pos[1]) <40:
            tahvel.delete(pellet_id[i])
            pellet_pos[i] = [1000,1000]
            score += 50
            break

def ghost_collision(ghost_pos, obj1_pos):
    global lives, pac_pos
    if abs(ghost_pos[0] - obj1_pos[0]) < 40 and abs(ghost_pos[1] -obj1_pos[1]) <40:
            lives -= 1
            pac_pos = [275,275]




# seon nooleklahvid vastavate funktsioonidega
raam.bind_all("<Up>",    nool_üles)
raam.bind_all("<Down>",  nool_alla)
raam.bind_all("<Left>",  nool_vasakule)
raam.bind_all("<Right>", nool_paremale)
raam.bind_all("<KeyRelease>", release_key)



def uuenda():
    global pac_id, ghost_pos, current_pic, trigger
    indeks = random.randint(0,3)
    kuhu = liikumine(indeks)
    if wall2(samm(ghost_pos)[indeks]) != True:
        ghost_pos[0] += kuhu[0]
        ghost_pos[1] += kuhu[1]
        tahvel.move(ghost_id,kuhu[0],kuhu[1])
    tahvel.delete(pac_id)
    if trigger:
        current_pic = pac_pics[0]
        trigger = False
    else:
        current_pic = pac_pics[1]
        trigger = True
    pac_id = tahvel.create_image(pac_pos[0], pac_pos[1], image=current_pic)

    remove_pellets(pellet_pos, pac_pos)
    ghost_collision(ghost_pos, pac_pos)

    silt2 = ttk.Label(raam, text=score, font=minu_font)
    silt2.place(x=230, y=565)
    silt3 = ttk.Label(raam, text=lives, font=minu_font)
    silt3.place(x=330, y=565)

    # ootame 0,1 sekundit ja siis uuendame positsiooni
    raam.after(100, uuenda)

uuenda()

# ilmutame akna ekraanile
raam.mainloop()