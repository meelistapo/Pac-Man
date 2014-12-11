__author__ = 'Meelis Tapo'
__author__ = 'Eduard Šengals'

from tkinter import *
from game import *
from objects import *
from random import randint
#mängu akna parameetrid
frame = Tk()
frame.title("Pacversity")
frame.geometry("850x850")
canvas = Canvas(frame, width=850, height=850, bg="black")
menu = Canvas(frame, width=850, height=850, bg="black")
menu.grid()

#meedia sisselugemine
#esmalt piltide sisselugemine
immov_obj.wall_bak_img = PhotoImage(file="media/wall_bak.png")
immov_obj.wall_mag_img = PhotoImage(file="media/wall_mag.png")
immov_obj.wall_dok_img = PhotoImage(file="media/wall_dok.png")
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
#tekstide sisselugemine
textfile = open("media/texts.txt", encoding="utf-8")
ghostmsg = {}
for line in textfile:
    ghostmsg[line.split(": ")[0].lstrip("\ufeff")] = line.split(": ")[1].split("; ")
textfile.close()

#mängu loomine ja peamenüü avamine
thisgame = game(canvas)
thisgame.parent = menu
thisgame.create_mainmenu()

#----------------------------------------------------------------
#funktsioonid, mis määravad tegevused klahvivajutuste korral
#----------------------------------------------------------------
def up_press(event):
    if thisgame.state == "game":
        moving_obj.pac.new_dir = [0,-10] #pac liigub üles
        moving_obj.pac.new_dir_imgs = moving_obj.pac_imgs[1] #ülesliikumise piltide aktiveerimine
    elif thisgame.state == "menu":
        thisgame.nextselection(-1) #menüüs koha võrra üles liikumine

def down_press(event):
    if thisgame.state == "game":
        moving_obj.pac.new_dir = [0,10] #pac liigub alla
        moving_obj.pac.new_dir_imgs = moving_obj.pac_imgs[2] #allaliikumise piltide aktiveerimine
    elif thisgame.state == "menu":
        thisgame.nextselection(1) #menüüs koha võrra alla liikumine

def left_press(event):
    if thisgame.state == "game":
        moving_obj.pac.new_dir = [-10,0] #pac liigub vasakule
        moving_obj.pac.new_dir_imgs = moving_obj.pac_imgs[3] #vasakuleliikumise piltide aktiveerimine

def right_press(event):
    if thisgame.state == "game":
        moving_obj.pac.new_dir = [10,0] #pac liigub paremale
        moving_obj.pac.new_dir_imgs = moving_obj.pac_imgs[0] #paremaleliikumise piltide aktiveerimine

def spacebar_press(event):
    if thisgame.state == "menu":
        #kui valid menüüs baka taseme
        if thisgame.selection == 0:
            menu.grid_forget()
            thisgame.parent = canvas
            canvas.grid()
            thisgame.level = 'bak'
            thisgame.create_level() #luuakse baka level
            thisgame.create_gamemenu() #koos päises oleva infomenüüga
            thisgame.state = "game"
        #kui valid menüüs mag taseme
        elif thisgame.selection == 1:
            if thisgame.highestlevelcompleted != None: #kontollitakse, kas oled läbinud baka taseme
                menu.grid_forget()
                thisgame.parent = canvas
                canvas.grid()
                thisgame.level = 'mag'
                thisgame.create_level() #luuakse mag level
                thisgame.create_gamemenu()
                thisgame.state = "game"
            else:
                thisgame.create_attention_message() #antakse teada, et sul on eelmine level läbimata
        #kui valid menüüs dok taseme
        elif thisgame.selection == 2:
            if thisgame.highestlevelcompleted == "mag": #kontollitakse, kas oled läbinud mag taseme
                menu.grid_forget()
                thisgame.parent = canvas
                canvas.grid()
                thisgame.level = 'dok'
                thisgame.create_level() #luuakse dok level
                thisgame.create_gamemenu()
                thisgame.state = "game"
            else:
                thisgame.create_attention_message() #antakse teada, et sul on eelmine level läbimata
        #kui valid menüüs 'Abi', siis saad abi :)
        elif thisgame.selection == 3:
            thisgame.create_help_message()
        #kui valid menüüs 'Sulge, siis mäng suletakse
        elif thisgame.selection == 4:
            frame.destroy()
    #mängus vahepausi alustamine/lõpetamine
    elif thisgame.state == "game":
        thisgame.state = "pause"
    elif thisgame.state == "pause":
        thisgame.state = "game"

def escape_press(event):
    #mängu sulgemine
    if thisgame.state == "menu":
        frame.destroy()
    #mängust peamenüüsse ja mänguobjektide algseisundi taastamine
    elif thisgame.state != "menu":
        thisgame.state = "menu"
        for elem in immov_obj.walls:
            canvas.delete(elem)
        for elem in immov_obj.pellets:
            canvas.delete(elem)
        for elem in moving_obj.ghosts:
            canvas.delete(elem.id)
        for elem in thisgame.textobjects:
            elem.config(text="")
        canvas.delete(moving_obj.pac.id)
        immov_obj.walls = {}
        immov_obj.pellets = {}
        moving_obj.pac = None
        moving_obj.ghosts = []
        moving_obj.moving = []
        thisgame.parent = menu
        canvas.grid_forget()
        menu.grid()

# seon klahvid vastavate funktsioonidega
frame.bind_all("<Up>", up_press)
frame.bind_all("<Down>",  down_press)
frame.bind_all("<Left>",  left_press)
frame.bind_all("<Right>", right_press)
frame.bind_all("<space>", spacebar_press)
frame.bind_all("<Escape>", escape_press)
frame.bind_all("<Return>", spacebar_press)

#----------------------------------------------------------------
#funktsioon, mis määrab objektide käitumise ajaühiku möödumisel
#----------------------------------------------------------------
def reload():
    if thisgame.state == "game":
        for elem in moving_obj.ghosts:  #tontide liigutamine
            elem.move(thisgame)
        moving_obj.pac.move(thisgame)   #pac'i liigutamine
        thisgame.eap.config(text="EAP: "+str(int(moving_obj.pac.eap))) #EAP-de loenduri uuendamine
        thisgame.warnings.config(text="HOIATUSI: "+str(moving_obj.pac.warnings)) #hoiatuste loenduri uuendamine
        #kui pac põrkab tondiga kokku, siis kuvatakse selle tondi spetsiifiline hoiatus
        if moving_obj.pac.coll_name is not None:
            warning_msg = ghostmsg[moving_obj.pac.coll_name][randint(0,1)]
            if '|' in warning_msg:
                warning_txt = warning_msg.split('|')
                warning_msg = warning_txt[0]+'\n'+warning_txt[1].strip()
            thisgame.last_warning.config(text=warning_msg, justify='left')
            thisgame.turns_to_show_warning = 120
            moving_obj.pac.coll_name = None
        if thisgame.turns_to_show_warning:
            thisgame.turns_to_show_warning -= 1 #hoiatuse teksti kuvamise timeri vähendamine
        else:
            thisgame.last_warning.config(text="") #hoiatuse teksti ekraanilt kustutamine
        #kui hoiatusi on kokku kolm, siis kuvatakse kaotussõnum ja viiakse sind peamenüüsse
        if moving_obj.pac.warnings == 3:
            thisgame.state = "pause"
            thisgame.create_game_over_message()
            escape_press("<Escape>")
        #kui kõik pelletid on kokkukorjatud, siis kuvatakse võidussõnum ja viiakse sind peamenüüsse
        if thisgame.state == "game" and len(immov_obj.pellets) == 0:
            thisgame.state = "pause"
            thisgame.create_victory_message()
            escape_press("<Escape>")
             #leveli läbimine jäetakse meelde ning menüüs viidatakse järgmisele tasemele või dok leveli läbimisel mängust väljumisele
            if thisgame.level == 'bak':
                thisgame.highestlevelcompleted = 'bak'
                thisgame.selection_pointer.place(x=35, y=100+1*40)
                thisgame.selection = 1
            elif thisgame.level == 'mag':
                thisgame.highestlevelcompleted = 'mag'
                thisgame.selection_pointer.place(x=35, y=100+2*40)
                thisgame.selection = 2
            else:
                thisgame.selection_pointer.place(x=35, y=100+4*40)
                thisgame.selection = 4

    # timer
    if thisgame.level == "dok":
        frame.after(60, reload) #dok levelil uueneb kuva iga 0,06 sekundi taga
    else:
        frame.after(80, reload) #teistel levelitel uueneb kuva iga 0,08 sekundi taga

reload()
frame.mainloop()