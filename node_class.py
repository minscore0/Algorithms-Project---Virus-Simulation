import pygame
import random
import math
import time


class Node:
    def __init__(self, screen, name, coords, color=(0, 0, 0), radius=30, mask=False, immune=False, infected=False, visited=False):
        self.screen = screen
        self.name = name
        self.coords = coords
        self.mask = mask
        if mask:
            self.color = (66, 161, 245)
        elif immune:
            self.color = (109, 237, 102)
        else:
            self.color = color
        self.radius = radius
        self.mask = mask
        self.immune = immune
        self.infected = infected
        self.visited = visited

        finding = True
        while finding: #generate unique coordinates
            finding = False
            self.x = random.randint(50, 1250) # based off of dimensions from screen.
            self.y = random.randint(50, 850)
            for x, y in coords:
                if math.dist((self.x, self.y), (x, y)) < 100:
                    finding = True

        self.coord = (self.x, self.y)
        self.interactions = 0

        #pygame.draw.circle(screen, color, self.coord, radius)

    def draw_node(self):
        pygame.draw.circle(self.screen, self.color, self.coord, self.radius)

    def give_mask(self):
        self.immune = False
        self.mask = True
        self.color = (66, 161, 245)
        self.draw_node()

    def make_immune(self):
        self.mask = False
        self.immune = True
        self.color = (109, 237, 102)
        self.draw_node()

    def make_normal(self):
        self.mask = False
        self.immune = False
        self.color = (0, 0, 0)
        self.draw_node()
    
    def disappear(self):
        self.color = (158, 158, 158)
        self.draw_node()

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name
