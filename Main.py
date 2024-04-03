import pygame
import os
import time

(width, height) = (800, 600)
screen = pygame.display.set_mode((width, height))
pygame.display.flip()

my_image = pygame.image.load('moln.jpg')
DISC_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bear1.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bear2.png")))]
BASKET_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "goal.png")))

class Disc:
    IMGS = DISC_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height  = self.y
        self.img_count = 0
        self.img = self.IMGS[0]
        
class Basket:
    VEL = 5

    def __init__(self, x): 
        



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
        screen.blit(my_image, (0, 0))
        pygame.display.update()
            


    