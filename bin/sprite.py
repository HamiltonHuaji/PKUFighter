# -*- coding: utf-8 -*-
import os
import pygame
import itertools

ryu_base_coords = {
    "idle": (
        (0, 15, 50, 85),
        (49, 15, 50, 85),
        (99, 15, 50, 85),
        (148, 15, 50, 85)
    ),
    "walking": (
        (202, 15, 50, 85),
        (249, 15, 50, 85),
        (298, 15, 50, 85),
        (348, 15, 50, 85),
        (398, 15, 50, 85)
    ),
    "punch": (
        (0,130,50,85),
        (0,130,50,85),
        (49,130,65,85),
        (49,130,65,85),

        (215,130,56,85),
        (215,130,56,85),
        (271,130,80,85),
        (271,130,80,85),
        (215,130,56,85),

        (0,255,60,95),
        (0,255,60,95),
        (60,255,73,95),
        (60,255,73,95),
        (0,255,60,95),

        (622,531,48,85),
        (670,531,50,85),
        (720,531,57,85),
        (777,500,42,116),
        (819,500,38,116),
        (857,500,37,116),
        (894,500,49,116)
    )
    ,
    "defend": (
        (1210,15,50,85),
        (1210,15,50,85)
    ),
    "hit": (
        (0,755,50,85),
        (49,755,50,85),
        (100,755,60,85),
        (160,755,50,85)
    ),
    "jump": (
        (450,15,50,85),
        (500,5,40,95),
        (540,15,37,85),
        (577,15,38,85),
        (615,15,38,85),
        (653,5,42,95),
        (695,15,45,85)
    ),
    "shoot": (
        (0,632,57,85),
        (57,632,71,85),
        (128,632,71,85),
        (199,632,96,85),
        (295,632,76,85)
    ),
    "wave": (
        (415,640,43,55),
        (415,640,43,55),
        (375,640,40,55),
        (375,640,40,55)
    ),
    "climax": (
        (948,516,46,100),
        (994,486,45,130),

        (1044,486,68,130),
        (1112,492,47,124),
        (1159,492,73,124),
        (1232,492,45,124),

        (1044,486,68,130),
        (1112,492,47,124),
        (1159,492,73,124),
        (1232,492,45,124),

        (1044,486,68,130),
        (1112,492,47,124),
        (1159,492,73,124),
        (1232,492,45,124),

        (1044,486,68,130),
        (1112,492,47,124),
        (1159,492,73,124),
        (1232,492,45,124),

        (1044,486,68,130),
        (1112,492,47,124),
        (1159,492,73,124),
        (1232,492,45,124),

        (1044,486,68,130),
        (1112,492,47,124),
        (1159,492,73,124),
        (1232,492,45,124),

        (1044,486,68,130),
        (1112,492,47,124),
        (1159,492,73,124),
        (1232,492,45,124),

        (1283,500,50,116),
        (1333,531,37,85)
    ),
    "pa": (
        (817,643,26,45),
        (817,643,26,45)
    ),
    "ko": (
        (1161,775,55,66),
        (1216,775,76,66),
        (1292,775,80,66),
        (1372,775,76,66),
        (1448,775,77,66)
    ),
    "ko_loop":(
        (1448,775,77,66),
        (1448,775,77,66),
    ),
    "win": (
        (54,870,50,95),
        (54,870,50,95),
        (54,870,50,95),
        (54,870,50,95),
        (54,870,50,95),
        (54,870,50,95),
        (104,848,50,117),
        (104,848,50,117),
        (104,848,50,117),
        (104,848,50,117),
        (104,848,50,117),
        (104,848,50,117),
    ),
    "win_loop":(
        (160,870,45,95),
        (160,870,45,95),
        (160,870,45,95),
        (205,870,48,95),
        (205,870,48,95),
        (205,870,48,95),
        (253,870,48,95),
        (253,870,48,95),
        (253,870,48,95),
        (301,870,48,95),
        (301,870,48,95),
        (301,870,48,95),
        (349,870,48,95),
        (349,870,48,95),
        (349,870,48,95),
        (397,870,48,95),
        (397,870,48,95),
        (397,870,48,95),
        (445,870,48,95),
        (445,870,48,95),
        (445,870,48,95)
    )
}

chun_li_base_coords = {
    "idle":(
        (0,28,50,85),
        (53,28,50,85),
        (105,28,50,85),
        (158,28,50,85),
    ),
    "walking":(
        (216,28,50,85),
        (272,28,50,85),
        (333,28,50,85),
        (390,28,50,85),
        (448,28,50,85),
        (505,28,50,85),
        (562,28,50,85),
        (618,28,50,85),
    ),
    "punch": (
        (0,141,69,85),
        (69,134,57,92),
        (69,134,57,92),
        (0,141,69,85),

        (198,145,70,80),
        (268,145,90,80),
        (268,145,90,80),
        (198,145,70,80),
        (400,258,59,85),

        (459,248,81,95),
        (540,258,71,85),
        (611,258,50,85),
        (1147,585,49,105),
        (1196,600,53,90),

        (530,590,80,100),
        (610,590,60,100),
        (697,590,85,100),
        (782,590,70,100),
        (881,590,88,100),
        (969,590,60,100),
        (1064,590,76,100)
    ),
    "defend": (
        (1008,140,55,85),
        (1008,140,55,85)
    ),
    "hit": (
        (0,850,60,85),
        (0,850,60,85),
        (60,850,68,85),
        (60,850,68,85)
    ),
    "jump": (
        (680,28,50,85),
        (730,13,40,100),
        (730,13,40,100),
        (770,13,40,70),
        (770,13,40,70),
        (810,13,40,100),
        (810,13,40,100)
    ),
    "shoot": (
        (0,585,54,105),
        (54,585,65,105),
        (54,585,65,105),
        (119,580,51,110),
        (170,585,69,105),
    ),
    "wave": (
        (244,595,39,55),
        (244,595,39,55),
        (323,595,39,55),
        (323,595,39,55)
    ),
    "climax": (

        (0,774,50,60),
        (50,729,53,105),
        (103,729,56,105),
        (159,709,76,125),
        (235,709,46,125),
        (281,709,49,125),
        (330,709,44,125),

        (377,709,46,125),
        (423,709,91,125),
        (514,709,50,125),
        (564,709,89,125),

        (377,709,46,125),
        (423,709,91,125),
        (514,709,50,125),
        (564,709,89,125),

        (377,709,46,125),
        (423,709,91,125),
        (514,709,50,125),
        (564,709,89,125),

        (377,709,46,125),
        (423,709,91,125),
        (514,709,50,125),
        (564,709,89,125),

        (377,709,46,125),
        (423,709,91,125),
        (514,709,50,125),
        (564,709,89,125),

        (656,709,45,125),
        (701,709,46,125),
        (747,709,75,125),
        (822,709,57,125),
        (879,729,50,105)
    ),
    "pa": (
        (373,648,23,40),
        (373,648,23,40)
    ),
    "ko": (
        (808,865,75,70),
        (883,865,63,70),
        (949,865,72,70),
        (1021,865,84,70),
        (1021,865,84,70)
    ),
    "ko_loop":(
        (1021,865,84,70),
        (1021,865,84,70)
    ),
    "win": (
        (162,1000,49,100),
        (211,1000,49,100),
        (260,965,55,135),
        (315,955,52,145),
        (367,965,53,135),

        (211,1000,49,100),
        (260,965,55,135),
        (315,955,52,145),
        (367,965,53,135),
    ),
    "win_loop":(
        (649,1000,49,100),
        (649,1000,49,100),
        (698,1000,49,100),
        (698,1000,49,100),
        (747,1000,49,100),
        (747,1000,49,100),
        (796,1000,49,100),
        (796,1000,49,100),
        (649,1000,49,100),
        (649,1000,49,100),
        (698,1000,49,100),
        (698,1000,49,100),
        (747,1000,49,100),
        (747,1000,49,100),
        (796,1000,49,100),
        (796,1000,49,100),
        (1050,985,50,115),
        (1050,985,50,115),
        (1050,985,50,115),
        (1050,985,50,115)
    )

}

class Itercycle(object):
    def __init__(self, lst):
        self.cur=0
        self.length=len(lst)
        self.cycle=lst
        # print(self.length)

    def now(self):
        return self.cycle[self.cur]

    def nxt(self,p=-1):
        if p==-1:
            self.cur=(self.cur+1)%self.length
        else:
            # print("p=%d" % p)
            self.cur=p
        return self.cycle[self.cur]

    def pre(self):
        self.cur=(self.cur-1)%self.length
        return self.cycle[self.cur]

    def size(self):
        return self.length

class Player(object):
    def __init__(self, player_id, walkable_area):
        path = os.path.dirname(os.path.realpath(__file__))
        self.pid=player_id
        if player_id==1:
            self.sprite_image = pygame.image.load(path + "/../assets/ryu.gif").convert()
            self.sprite_base_coords = ryu_base_coords
            self.punch_height=[[250,250,250,250],[250,250,250,250,250],[250,250,250,250,250],
              [250,250,250,200,140,200,250]]
            self.punch_judge=[[0,0,5,0],[0,0,5,0,0],[0,0,5,0,0],[0,0,5,5,5,5,0]]
            self.punch_frame_cnt=[4,5,5,7]
            self.climax_judge=[0,0,
                               5,0,0,0,
                               5,0,0,0,
                               5,0,0,0,
                               5,0,0,0,
                               5,0,0,0,
                               5,0,0,0,
                               5,0,0,0,
                               0,0]


        else:
            self.sprite_image = pygame.image.load(path + "/../assets/chun-li.gif").convert()
            self.sprite_base_coords = chun_li_base_coords
            self.punch_height=[[250,250,250,250],[250,250,250,250,250],[250,250,250,250,250],
              [250,250,250,250,250,250,250]]
            self.punch_judge=[[0,0,5,0],[0,5,0,0,0],[5,0,0,0,0],[5,0,5,0,5,0,5]]
            self.punch_frame_cnt=[4,5,5,7]
            self.climax_judge=[0,0,0,0,0,0,0,
                               0,3,0,4,
                               0,3,0,4,
                               0,3,0,4,
                               0,3,0,4,
                               0,3,0,4,
                               0,0,0,0,0]

        self.sprite_set = {
            "left":self.build_left_sprite_set(),
            "right":self.build_right_sprite_set()
        }
        self.base_point = [0,250] # left, up point's position
        self.wave_point = [0,280]
        self.screen_left = walkable_area[0]
        self.screen_right = walkable_area[1]

        self.idle = "idle"
        self.direction = "right"
        self.walk=-1
        self.punch=0
        self.punchremain=0
        self.punched=0
        self.punchlevel=0
        self.jump=0
        self.jumpremain=0
        self.defend=0
        self.hit=0
        self.hitremain=0
        self.shoot=0
        self.shootremain=0
        self.flying=0
        self.flydis=0
        self.hp=200
        self.power=0
        self.climax=0
        self.climaxremain=0
        self.paremain=0
        self.winnow=0
        self.konow=0

    def build_right_sprite_set(self):
        """
        Cut and build sprite set
        """
        # get spriteset
        transparent_pixel = (0, 0)
        self.sprite_image.set_colorkey(self.sprite_image.get_at(transparent_pixel))
        sprites = dict()
        for name, coords in self.sprite_base_coords.items():
            temp = list()
            # cnt=0
            for coord in coords[0:]:
                rect = pygame.Rect(coord[0], coord[1], coord[2], coord[3])
                sprite = self.sprite_image.subsurface(rect).convert()
                # pygame.draw.line(sprite,(0,0,0),(0,0),(coord[2]-1,0),1)
                # pygame.draw.line(sprite,(0,0,0),(coord[2]-1,0),(coord[2]-1,coord[3]-1),1)
                # pygame.draw.line(sprite,(0,0,0),(0,0),(0,coord[3]-1),1)
                # pygame.draw.line(sprite,(0,0,0),(0,coord[3]-1),(coord[2]-1,coord[3]-1),1)
                sprite = pygame.transform.scale2x(sprite)
                temp.append(sprite)
                # cnt+=1
            # print("cnt=%d" % cnt)
            sprites[name] = Itercycle(temp)
        return sprites

    def build_left_sprite_set(self):
        """
        Cut and build sprite set
        """
        # get spriteset
        transparent_pixel = (0, 0)
        self.sprite_image.set_colorkey(self.sprite_image.get_at(transparent_pixel))
        sprites = dict()
        for name, coords in self.sprite_base_coords.items():
            temp = list()
            # cnt=0
            for coord in coords[0:]:
                rect = pygame.Rect(coord[0], coord[1], coord[2], coord[3])
                sprite = self.sprite_image.subsurface(rect).convert()
                # pygame.draw.line(sprite,(0,0,0),(0,0),(coord[2]-1,0),1)
                # pygame.draw.line(sprite,(0,0,0),(coord[2]-1,0),(coord[2]-1,coord[3]-1),1)
                # pygame.draw.line(sprite,(0,0,0),(0,0),(0,coord[3]-1),1)
                # pygame.draw.line(sprite,(0,0,0),(0,coord[3]-1),(coord[2]-1,coord[3]-1),1)
                sprite = pygame.transform.flip(pygame.transform.scale2x(sprite),True,False)
                temp.append(sprite)
            #     cnt+=1
            # print("%d %s cnt=%d" % (self.pid,name,cnt))
            sprites[name] = Itercycle(temp)
        return sprites

    # def choosesprite(self):
    #     if self.punch==1 and self.defend==0:
    #         self.punchremain=3
    #         self.punch=0
    #     if self.punchremain:
    #         self.sprite = self.sprite_set[self.direction]['punch']
    #         self.punchremain-=1
    #     elif self.defend:
    #         self.sprite=self.sprite_set[self.direction]['defend']
    #         return
    #     if self.idle :
    #         if self.punchremain==0:
    #             self.sprite = (self.sprite_set[self.direction]['idle'])
    #         return
    #     else:
    #         if self.punchremain==0:
    #             self.sprite = (self.sprite_set[self.direction]['walking'])
    # def proc(self):
    #     self.base_point[0] += distance if self.direction == "right" else (-distance)
    #     self.base_point[0] = self.base_point[0] if self.base_point[0] >= self.screen_left else self.screen_left
    #     self.base_point[0] = self.base_point[0] if self.base_point[0] <= self.screen_right else self.screen_right
