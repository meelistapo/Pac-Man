__author__ = 'Meelis Tapo'
__author__ = 'Eduard Šengals'
import random
from game import *
class moving_obj:
    pac = None
    ghosts = []
    pac_imgs = []
    ghost_imgs = []
    moving = []
    def __init__(self, start_pos, parent, img, coll_pel = False, coll_ghost = False, att=None, name=None):
        self.coll_pel = coll_pel
        self.coll_ghost = coll_ghost
        self.parent = parent
        self.start_img = img
        self.img_index = 0
        self.dir_imgs = moving_obj.pac_imgs[0]
        self.new_dir_imgs = None
        self.id = self.parent.create_image(start_pos[0], start_pos[1], image=self.start_img)
        self.start_pos = start_pos
        self.pos = start_pos
        self.dir = None
        self.att = att
        self.new_dir = None
        self.possible_dir = []
        self.ainepunktid = 0.0
        self.hoiatused = 0
        self.name = name
        self.coll_name = None
        if self.att != "player":
            moving_obj.ghosts.append(self)
        else:
            moving_obj.pac = self
    def move(self, game):
        if (not self.pos[0]%25 and not self.pos[1]%25) and (self.pos[0]%50 or self.pos[1]%50):
            self.possible_dir.clear()
            if [self.pos[0]+50,self.pos[1]] not in immov_obj.walls.values():
                self.possible_dir.append([10,0])
            if [self.pos[0]-50,self.pos[1]] not in immov_obj.walls.values():
                self.possible_dir.append([-10,0])
            if [self.pos[0],self.pos[1]+50] not in immov_obj.walls.values():
                self.possible_dir.append([0,10])
            if [self.pos[0],self.pos[1]-50] not in immov_obj.walls.values():
                self.possible_dir.append([0,-10])
            if self.att != "player": #><
                if self.dir != None and [-self.dir[0],-self.dir[1]] in self.possible_dir and len(self.possible_dir) != 1:
                    self.possible_dir.remove([-self.dir[0],-self.dir[1]])
                if self.att == "ai":
                    self.check_lineofsight()
    #----------------------------------------------------------------
        if self.att == "player":
            if self.new_dir in self.possible_dir:
                self.dir = self.new_dir
                self.dir_imgs = self.new_dir_imgs
        elif self.att == "ai":
            if moving_obj.pac.pos[0] in range(self.lineofsight[0][0], self.lineofsight[0][1])and moving_obj.pac.pos[0] < self.pos[0] and [-10, 0] in self.possible_dir:
                self.dir = [-10, 0]
            elif moving_obj.pac.pos[0] in range(self.lineofsight[0][0], self.lineofsight[0][1])and moving_obj.pac.pos[0] > self.pos[0] and [10, 0] in self.possible_dir:
                self.dir = [10, 0]
            elif moving_obj.pac.pos[1] in range(self.lineofsight[1][0], self.lineofsight[0][1])and moving_obj.pac.pos[1] < self.pos[1] and [0, -10] in self.possible_dir:
                self.dir = [0, -10]
            elif moving_obj.pac.pos[1] in range(self.lineofsight[1][0], self.lineofsight[0][1])and moving_obj.pac.pos[1] > self.pos[1] and [0, 10] in self.possible_dir:
                self.dir = [0, 10]
            else:
                self.dir = self.possible_dir[random.randint(0,len(self.possible_dir)-1)]
        else:
            self.dir = self.possible_dir[random.randint(0,len(self.possible_dir)-1)]
    #----------------------------------------------------------------
        if self.dir in self.possible_dir:
            if self.att == "player":
                self.parent.move(self.id, self.dir[0], self.dir[1])
                self.pos = [self.pos[0]+self.dir[0],self.pos[1]+self.dir[1]]
                self.swapimage()
                self.possible_dir = [self.dir,[-self.dir[0],-self.dir[1]]]
            else:
                self.parent.move(self.id, self.dir[0], self.dir[1])
                self.pos = [self.pos[0]+self.dir[0],self.pos[1]+self.dir[1]]
                self.possible_dir = [self.dir]
    #----------------------------------------------------------------
        if self.coll_pel and (self.pos in immov_obj.pellets.values()):
            if game.level == "baka":
                self.ainepunktid += 180/130
            elif game.level == "mag":
                self.ainepunktid += 120/129
            elif game.level == "dok":
                self.ainepunktid += 240/129
            for k, v in immov_obj.pellets.items():
                if v == self.pos:
                    self.parent.delete(k)
                    break
            del immov_obj.pellets[k]
    #----------------------------------------------------------------
        if self.coll_ghost:
            for elem in moving_obj.ghosts:
                if abs(self.pos[0]-elem.pos[0])<30 and abs(self.pos[1]-elem.pos[1])<30:
                    self.coll_name = elem.name
                    self.parent.delete(self.id)
                    self.hoiatused += 1
                    self.id = self.parent.create_image(self.start_pos[0], self.start_pos[1], image=self.start_img)
                    self.pos = self.start_pos
                    self.dir, self.new_dir = None, None
                    for ghost in moving_obj.ghosts:
                        ghost.pos = ghost.start_pos
                        ghost.parent.delete(ghost.id)
                        ghost.id = ghost.parent.create_image(ghost.start_pos[0], ghost.start_pos[1], image=ghost.start_img)
                        ghost.dir, ghost.new_dir = None, None
                    break
    def swapimage(self):
        if self.att == "player":
            if self.img_index:
                self.img_index-=1
            else:
                self.img_index+=1
        self.parent.delete(self.id)
        self.id = self.parent.create_image(self.pos[0], self.pos[1], image=self.dir_imgs[self.img_index])
    def check_lineofsight(self):
        self.lineofsight = [[0,0],[0,0]] # [[xrange][yrange]
        i = 1
        while True:
            if [self.pos[0]-50*i, self.pos[1]] in immov_obj.walls.values():
                self.lineofsight[0][0] = self.pos[0]-50*i
                i = 1
                break
            i += 1
        while True:
            if [self.pos[0]+50*i, self.pos[1]] in immov_obj.walls.values():
                self.lineofsight[0][1] = self.pos[0]+50*i
                i = 1
                break
            i += 1
        while True:
            if [self.pos[0], self.pos[1]-50*i] in immov_obj.walls.values():
                self.lineofsight[1][0] = self.pos[1]-50*i
                i = 1
                break
            i += 1
        while True:
            if [self.pos[0], self.pos[1]+50*i] in immov_obj.walls.values():
                self.lineofsight[1][1] = self.pos[1]+50*i
                break
            i += 1

class immov_obj:
    walls = {}
    pellets = {}
    def __init__(self, pos, parent, img, is_pellet=False, is_wall=False):
        self.pos = pos
        self.parent = parent
        self.img = img
        self.id = self.parent.create_image(self.pos[0], self.pos[1], image=self.img)
        if is_pellet:
            immov_obj.pellets[self.id] = self.pos
        if is_wall:
            immov_obj.walls[self.id] = self.pos