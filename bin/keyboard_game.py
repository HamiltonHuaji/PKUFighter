#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import pygame
import copy
from pygame.locals import *
from sprite import Player

# consts

screen_width, screen_height = (1242, 480)
frame_rate = 60
move_distance = 40
cnt=0
jump_height=[250,140,50,10,50,140,250]


def move(x,y,d):
    if y<x:
        x+=d
    else:
        x-=d


def separate(x1,l1,x2,l2):
    if x1<x2:
        m=(x1+x2+l2)//2
        x1=m-l1
        x2=m

def intersect(x1,l1,x2,l2):
    return not (x1+l1<x2 or x2+l2<x1)

def intersectd2(x1,y1,l1,d1,x2,y2,l2,d2):
    return not (x1+l1<x2 or x2+l2<x1 or y1+d1<y2 or y2+d2<y1)


class Game(object):
    size = (screen_width, screen_height)

    def __init__(self):

        # some initialization

        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])
        path = os.path.dirname(os.path.realpath(__file__))
        image = pygame.image.load(
            path + '/../assets/background-1.jpg'
        ).convert()
        self.background = pygame.transform.scale2x(image)
        self.background_copy = pygame.transform.scale2x(image)

        left = (self.background.get_width() - self.size[0]) / 2
        # print(self.background.get_width())
        self.background_position = [-left, 0]
        for i in range(99):
            pygame.draw.rect(self.background,(255,i*2.5,0),(20+i*5,20,10,40))
        for i in range(99):
            pygame.draw.rect(self.background,(255,i*2.5,0),(1222-(i+2)*5,20,10,40))
        # print(left)

        # prepare players
        # should build animation in Player()

        self.players = [Player(0, (0, screen_width-100)), Player(1, (0, screen_width-100))]

        self.players[0].base_point[0] = 0.0
        self.players[1].base_point[0] = screen_width - 100

        self.players[0].direction = "right"
        self.players[1].direction = "left"

        self.process()

    def process(self):
        p=self.players

        if p[0].base_point[0]<p[1].base_point[0]:
            p[0].direction="right"
            p[1].direction="left"
        else:
            p[0].direction="left"
            p[1].direction="right"



        for i in range(2):
            if p[i].flying:
                if p[i^1].defend==0 and intersectd2(p[i].wave_point[0]-5,p[i].wave_point[1],p[i].fsprite.get_width()+15,p[i].fsprite.get_height(),p[i^1].base_point[0],p[i^1].base_point[1],p[i^1].sprite.get_width(),p[i^1].sprite.get_height())!=0:
                    p[i^1].hitremain=4
                    p[i^1].hp=max(p[i^1].hp-5,0)
                    p[i].power=min(p[i].power+1,15)
                    p[i^1].power=min(p[i^1].power+2,15)
                    p[i^1].sprite_set[p[i^1].direction]['hit'].nxt(p=0)
                    p[i].flying=0
                else:
                    p[i].wave_point[0]+=p[i].flydis
                    p[i].fsprite=p[i].sprite_set[p[i].direction]['wave'].nxt()


        for i in range(2):
            if p[i].defend or p[i].shoot:
                p[i].idle=1
            if p[i].idle==0:
                p[i].base_point[0] += move_distance*p[i].walk

        for i in range(2):
            if p[i].climax or p[i].climaxremain:
                p[i].defend=1

        for i in range(2):


            flag=p[i].hitremain or p[i].punchremain or p[i].defend or p[i].jumpremain or p[i].shootremain or p[i].jump or p[i].punch or p[i].shoot or p[i].climaxremain or p[i].climax

            if p[i].hitremain:
                p[i].sprite=p[i].sprite_set[p[i].direction]['hit'].nxt()
                p[i].hitremain-=1
                if p[i].hitremain==2:
                    move(p[i].base_point[0],p[i^1].base_point[0],3)


            elif p[i].jumpremain:
                p[i].sprite=p[i].sprite_set[p[i].direction]['jump'].nxt()
                p[i].jumpremain-=1
                p[i].base_point[1]=jump_height[p[i].jumpremain]


            elif p[i].punchremain>0:
                p[i].sprite=p[i].sprite_set[p[i].direction]['punch'].nxt()
                p[i].punchremain-=1
                if p[i].punchremain<p[i].punch_frame_cnt[p[i].punchlevel]:
                    clevel=p[i].punchlevel
                    cframe=p[i].punchremain
                else:
                    clevel=p[i].punchlevel-1
                    cframe=p[i].punchremain-p[i].punch_frame_cnt[p[i].punchlevel]
                cframe=p[i].punch_frame_cnt[clevel]-cframe-1
                p[i].base_point[1]=p[i].punch_height[clevel][cframe]
                if p[i].punch and p[i].punchremain<p[i].punch_frame_cnt[p[i].punchlevel] and p[i].punchlevel<3:
                    p[i].punchlevel+=1
                    p[i].punchremain+=p[i].punch_frame_cnt[p[i].punchlevel]
                if p[i].punch_judge[clevel][cframe]>0 and p[i^1].defend==0 and intersect(p[i].base_point[0]-15,p[i].sprite.get_width()+30,p[i^1].base_point[0],p[i^1].sprite.get_width())!=0:
                    p[i^1].hitremain=4
                    p[i^1].hp=max(p[i^1].hp-p[i].punch_judge[clevel][cframe],0)
                    p[i].power=min(p[i].power+1,15)
                    p[i^1].power=min(p[i^1].power+2,15)
                    p[i^1].sprite_set[p[i^1].direction]['hit'].nxt(p=0)
                # print(p[i].base_point[0]-5,p[i].sprite.get_width()+5,p[i^1].base_point[0],p[i^1].sprite.get_width(),p[i].punch_judge[clevel][cframe],p[i].punchremain)


            elif p[i].climaxremain:
                p[i].sprite=p[i].sprite_set[p[i].direction]['climax'].nxt()
                p[i].climaxremain-=1
                cframe=32-p[i].climaxremain-1
                if p[i].climax_judge[cframe]>0 and p[i^1].defend==0 and intersect(p[i].base_point[0]-15,p[i].sprite.get_width()+30,p[i^1].base_point[0],p[i^1].sprite.get_width())!=0:
                    p[i^1].hitremain=4
                    p[i^1].hp=max(p[i^1].hp-p[i].climax_judge[cframe],0)
                    p[i^1].power=min(p[i^1].power+2,15)
                    p[i^1].sprite_set[p[i^1].direction]['hit'].nxt(p=0)
                # print(p[i].base_point[0]-5,p[i].sprite.get_width()+5,p[i^1].base_point[0],p[i^1].sprite.get_width(),p[i].climax_judge[cframe],p[i].climaxremain)


            elif p[i].shootremain:
                p[i].sprite=p[i].sprite_set[p[i].direction]['shoot'].nxt()
                p[i].shootremain-=1
                p[i].idle=1
                if p[i].shootremain==1:
                    p[i].flying=1
                    p[i].fsprite=p[i].sprite_set[p[i].direction]['wave'].nxt(p=0)
                    if p[i].direction=="right":
                        p[i].wave_point[0]=p[i].base_point[0]+p[i].sprite.get_width()
                        p[i].flydis=80
                    else:
                        p[i].wave_point[0]=p[i].base_point[0]
                        p[i].flydis=-80


            elif p[i].climax:
                p[i].climax=0
                if p[i].power==15:
                    p[i].sprite=p[i].sprite_set[p[i].direction]['climax'].nxt(p=0)
                    p[i].climaxremain=31
                    p[i].power=0
                    # print(p[i].base_point[0]-5,p[i].sprite.get_width()+5,p[i^1].base_point[0],p[i^1].sprite.get_width())


            elif p[i].jump:
                if p[i].jumpremain==0:
                    p[i].jumpremain=7
                    p[i].sprite=p[i].sprite_set[p[i].direction]['jump'].nxt(p=0)
                p[i].jump=0


            elif p[i].defend:
                p[i].sprite=p[i].sprite_set[p[i].direction]['defend'].nxt()


            elif p[i].punch:
                p[i].punch=0
                p[i].punched=0
                p[i].sprite=p[i].sprite_set[p[i].direction]['punch'].nxt(p=0)
                # pygame.draw.line(p[i].sprite,(255,0,0),(10,20),(50,50),3)
                # print("punch mark poped")
                p[i].punchremain=3
                p[i].punchlevel=0


            elif p[i].shoot:
                p[i].shoot=0
                if p[i].flying==0:
                    p[i].sprite=p[i].sprite_set[p[i].direction]['shoot'].nxt(p=0)
                    p[i].shootremain=5
                    p[i].idle=1


            #!!!
            if p[i].idle:
                if flag==0:
                    p[i].sprite=p[i].sprite_set[p[i].direction]['idle'].nxt()


            else:
                if flag==0:
                    p[i].sprite=p[i].sprite_set[p[i].direction]['walking'].nxt()

        for i in range(2):

            p[i].base_point[0]=max(p[i].base_point[0],p[i].screen_left)
            p[i].base_point[0]=min(p[i].base_point[0],p[i].screen_right)

            if intersectd2(p[0].base_point[0],p[0].base_point[1],
                         p[0].sprite.get_width(),p[0].sprite.get_height(),
                         p[1].base_point[0],p[1].base_point[1],
                         p[1].sprite.get_width(),p[1].sprite.get_height()):
                if p[i].base_point[0]<p[i^1].base_point[0]:
                    p[i].base_point[0]=min(p[i].base_point[0],p[i^1].base_point[0]-p[i].sprite.get_width())
                else:
                    p[i].base_point[0]=max(p[i].base_point[0],p[i^1].base_point[0]+p[i^1].sprite.get_width())


    def run(self):
        global cnt
        running = True
        while running:
            pygame.time.Clock().tick(frame_rate)
            # print(pygame.time.Clock().get_fps())
            running = self.handleEvents()
            # blit the background


            # pygame.draw.rect(self.background,(255,i*2.5,0),(20+i*5,20,10,40))
            self.screen.blit(self.background, self.background_position)
            tmp=self.background_copy.subsurface((20+self.players[0].hp*5,20,(100-self.players[0].hp)*5,40))
            self.screen.blit(tmp, [20+self.players[0].hp*5,20])


            # pygame.draw.rect(self.background,(255,i*2.5,0),(1222-(i+2)*5,20,10,40)
            tmp=self.background_copy.subsurface((722,20,(100-self.players[1].hp)*5,40))
            self.screen.blit(tmp, [722,20])


            tmp=pygame.Surface((self.players[0].power*20,10))
            if self.players[0].power<15:
                tmp.fill((0,255*self.players[0].power//15,255))
            else:
                tmp.fill((255,255,255))
            self.screen.blit(tmp,[20,100])


            tmp=pygame.Surface((self.players[1].power*20,10))
            if self.players[1].power<15:
                tmp.fill((0,255*self.players[1].power//15,255))
            else:
                tmp.fill((255,255,255))
            self.screen.blit(tmp,[1222-self.players[1].power*20,100])
            # blit the sprite
            # self.screen.blit(next(self.sprite), (self.p1left, 250))

            self.process()

            for i in range(2):
                self.screen.blit(self.players[i].sprite,
                                 (self.players[i].base_point[0],
                                  self.players[i].base_point[1]-(self.players[i].sprite.get_height()-170)))
                # print(self.players[i].sprite.get_height())
            for i in range(2):
                if self.players[i].flying:
                    self.screen.blit(self.players[i].fsprite,self.players[i].wave_point)
                if self.players[i].hitremain>=3:
                    if self.players[i].direction=='left':
                        self.screen.blit(self.players[i^1].sprite_set[self.players[i].direction]["pa"].nxt(p=0),
                                         (self.players[i].base_point[0]+10,self.players[i].base_point[1]))
                    else:
                        self.screen.blit(self.players[i^1].sprite_set[self.players[i].direction]["pa"].nxt(p=0),
                                         (self.players[i].base_point[0]+self.players[i].sprite.get_width()-30,self.players[i].base_point[1]))


            # update screen
            rect = pygame.Rect(
                0,
                0,
                self.size[0],
                self.size[1]
            )
            pygame.display.update(rect)
            cnt+=1
            print(cnt)

    def handleEvents(self):

        self.players[0].idle = True
        self.players[1].idle = True
        for i in range(2):
            self.players[i].defend=0
            self.players[i].punch=0
            self.players[i].jump=0
            self.players[i].hit=0
            self.players[i].shoot=0
            self.players[i].climax=0
            self.players[i].pa=0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                # if the user presses escape or 'q', quit the event loop.
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    return False
                if event.key == pygame.K_a:
                    print("a pressed")
                if event.key == pygame.K_j:
                    self.players[0].punch=1
                    print("j pressed")
                if event.key == pygame.K_k:
                    self.players[0].jump=1
                    print("k pressed")
                if event.key == pygame.K_u:
                    self.players[0].shoot=1
                    print("u pressed")
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    print("a unpressed")
                if event.key == pygame.K_j:
                    print("j unpressed")

        pressed = pygame.key.get_pressed()
        # movement control controlling background for now

        if pressed[pygame.K_a]:
            self.players[0].walk = -1
            self.players[0].idle = False
            print("pressed a")
        if pressed[pygame.K_d]:
            self.players[0].walk = 1
            self.players[0].idle = False
        if pressed[pygame.K_LEFT]:
            self.players[1].walk = -1
            self.players[1].idle = False
        if pressed[pygame.K_RIGHT]:
            self.players[1].walk = 1
            self.players[1].idle = False
        if pressed[pygame.K_l]:
            self.players[0].defend=1
            self.players[0].idle=1
        if pressed[pygame.K_u] and pressed[pygame.K_j]:
            self.players[0].climax=1
        return True
