import pygame
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))
screen.fill((255, 255, 255))

circle(screen, (255, 255, 0), (200, 200), 100)
circle(screen, (0, 0, 0), (200, 200), 100, 1)

circle(screen, (255, 0, 0), (160, 180), 20)
circle(screen, (0, 0, 0), (160, 180), 20, 1)
circle(screen, (0, 0, 0), (160, 180), 10)

circle(screen, (255, 0, 0), (240, 170), 17)
circle(screen, (0, 0, 0), (240, 170), 17, 1)
circle(screen, (0, 0, 0), (240, 170), 6)

line(screen, (0, 0, 0), (140, 150), (180, 160), 10)
line(screen, (0, 0, 0), (250, 143), (220, 163), 10)

rect(screen, (0, 0, 0), (160, 250, 80, 20))

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()