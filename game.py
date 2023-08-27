import sys
import os


import random
import time

import pygame
from pygame.locals import *

player_counter = 0
goblo_counter  = 0

RESOLUTION_NHD =(640,360)
RESOLUTION_HD  =(1280,720)
RESOLUTION_FHD =(1920,1080)
RESOLUTION_QHD =(2560,1440)
RESOLUTION_4K  =(3840,2160)



COLOR_BLUE_LIGHT = (160, 190, 200)
COLOR_BLACK = (0, 0, 0)

def clear_screen():
    os.system('clear')
#fed

class player:
    kind = 'player'
    accuracy = 0.8
    atk_cost = 30
    energy_max = 100
    energy_regen = 10
    hp_max = 30

    def __init__(self, _hp,_atk, _player_counter, _energy_max, team):

        self.name = "player-" + str(_player_counter)
        self.team = team
        self.hp = _hp
        self.power = _atk
        self.energy = _energy_max
        _player_counter+= 1
    #new

    # how to model simultaneous attack? add it to a global queue
    def atk(self, _target):
        print(self.name + " preparing to attack "+ _target.name)

        if _target is None:
            print("[error] no target, something went wrong")
            return
        #fi
        if self.energy < self.atk_cost:
            print(self.name + ": not enough energy")
            return
        #fi
        self.energy-= self.atk_cost
        if random.random() < self.accuracy:
            print("{name} attacked {target} for {damage} dmg".format(name=self.name,target=_target.name, damage=self.power))
            _target.hp -= self.power
        else:
            print("oof... {name} missed {target}".format(name=self.name, target=_target.name))
        #fi
    #fed

    # attack first enemies you see
    def ai(self, world):
        for agent in world.agents:
            # don't hit yourself unless you're confused
            if agent.team != self.team:
                if agent is None:
                    print("[error] no target, something went wrong")
                #fi

                self.atk(agent)
            #fi
    #fed

    def check_died(self, world):
        if self.hp <= 0:
            print(self.name + "died")
            # remove from world
            world.agents.remove(self)
        #fi
    #fed

    # this should be run everyframe
    def update(self, world):
        self.check_died(world)
        self.energy += self.energy_regen
        if self.energy >= self.energy_max:
            self.energy = self.energy_max
        #fi
        self.ai(world)
    #fed
#class

class World:

    def __init__(self):
        self.agents = []
        self.agents.append(player(
            player.hp_max,3, player_counter, _energy_max=player.energy_max, team='1'))

        self.agents.append(player(
            player.hp_max,3, player_counter, _energy_max=player.energy_max, team='2'))

        self.agents.append(player(
            player.hp_max,3, player_counter, _energy_max=player.energy_max, team='3'))
    #fed

    def print(self):
        for agent in self.agents:
            print("{name} [hp:{hp}/{max_hp}] [e: {energy}/{energy_max}]".format(
                name=agent.name, hp=agent.hp, max_hp=agent.hp_max,
                energy=agent.energy,energy_max=agent.energy_max))
        #loop
    #fed

    # run all ai in the world
    def update(self):
        for agent in self.agents:
            agent.update(self)
        #loop
    #end

#end_class


def display_font(font_obj, surface, in_str):
    text = font_obj.render( in_str, True, (255,255,255), (159,182,205) )
    text_rect = text.get_rect()
    text_rect.centerx = surface.get_rect().centerx
    text_rect.centery = surface.get_rect().centery
    # blit - a logical operation in which a block of data is rapidly copied in memory
    #        most commonly used to animate two-dimensional graphics
    surface.blit(text, text_rect)
    pygame.display.update()
#fed

class displayresolution:
    def __init__(self, w, h):
        self.w = w
        self.h = h
    #end

    def set_resolution(self, w=800, h=450):
        # error checking
        if self.w is None:
            self.w = 800
        #fi
        if self.h is None:
            self.h = 450
        #fi
        screen = pygame.display.set_mode((self.w, self.h))
        return screen
    #end

    def print_resolution(self):
        print(f"resolution is w:{self.w} h:{self.h}")
    #end
#class

def set_resolution(w,h,multiplier):
    pass
#fin




def game():

    # set fps
    fps = 5
    sleep_time = 1/fps # lol turns out pygame already has clock.tick(fps)

    pygame.init()


    # start_ set resolution
    # screen = pygame.display.set_mode((resolution_w,resolution_h))
    res = displayresolution(640,360)
    screen = res.set_resolution()
    res.print_resolution()

    time.sleep(0.1)

    res.set_resolution(RESOLUTION_HD[0], RESOLUTION_HD[1])

    # end_ set resolution

    pygame.display.set_caption('python numbers')

    # https://www.pygame.org/docs/ref/surface.html#pygame.surface.fill

    screen.fill((159,182,205))

    time.sleep(1)

    screen.fill(COLOR_BLUE_LIGHT)
    font_obj = pygame.font.Font(None,17)

    # init world
    world = World()

    current_frame = 0
    done = False
    # game loop
    while not done:

        # slow down loop
        time.sleep(sleep_time)

        # display current frame
        display_font( font_obj, screen, str(current_frame) )
        if current_frame > 60:
            current_frame = 0
        #fi
        current_frame+= 1

        pygame.event.pump()

        # poll for key input
        keys = pygame.key.get_pressed()
        if keys[K_ESCAPE]:
            done = True
        #fi


        # update game logic
        world.update()
        # clear_screen()
        # print
        world.print()
    #loop
#end

if __name__ == "__main__":
    pass
    sys.exit(game())
#fi