import pygame
from pygame.draw import *
import random
import math

FPS = 60

WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE = (0, 0, 200)
YELLOW = (200, 200, 0)
GREEN = (0, 200, 0)
MAGENTA = (200, 0, 200)
CYAN = (0, 200, 200)
BLACK = (0, 0, 0)
COLORS = [BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 1200
HEIGHT = 900

class Ball:
    def __init__(self):
        self.r = random.randint(50, 100)

        self.x = random.randint(self.r, WIDTH - self.r)
        self.y = random.randint(self.r, HEIGHT - self.r)

        self.vx = random.randint(5, 15)
        self.vy = random.randint(5, 15)

        self.color = random.choice(COLORS)

        self.time = 0

    def draw(self):
        circle(screen, self.color, [self.x, self.y], self.r)

    def hit(self, event, points, screen):
        if(math.sqrt((event.pos[0] - self.x) ** 2 + (event.pos[1] - self.y) ** 2) <= self.r):
            points.add()
            screen.fill(WHITE)
            return True

    def move(self):
        # столкновение со стенам
        if (self.x + self.r >= WIDTH):
            self.vx = -self.vx
            self.x = WIDTH - self.r
        if (self.x - self.r <= 0):
            self.vx = -self.vx
            self.x = self.r
        if (self.y + self.r >= HEIGHT):
            self.vy = -self.vy
            self.y = HEIGHT - self.r
        if (self.y - self.r <= 0):
            self.vy = -self.vy
            self.y = self.r

        # перемещение
        self.x += self.vx
        self.y -= self.vy

    def life(self):
        self.time += 1
        return self.time

class Points:
    def __init__(self):
        self.points = 0

    def add(self, sum=1):
        self.points += sum

    def get(self):
        return self.points

    def print(self):
        str_points = "Количество очков: " + str(self.points)

        font = pygame.font.Font(None, 36)
        text1 = font.render(str_points, 1, BLACK)

        screen.blit(text1, (10, 50))

class Skull:
    def __init__(self):
        self.r = 50

        self.x = random.randint(self.r, WIDTH - self.r)
        self.y = random.randint(self.r, HEIGHT - self.r)

        self.speed = 10

        self.image = pygame.image.load("skull.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.r * 2, self.r * 2))

        self.time = 0


    def move(self):
        pos = pygame.mouse.get_pos()
        mod = math.sqrt((self.x - pos[0]) ** 2 + (self.y - pos[1]) ** 2)
        a = [(self.x - pos[0]) / mod, (self.y - pos[1]) / mod]

        self.x -= a[0] * self.speed
        self.y -= a[1] * self.speed

    def draw(self):
        screen.blit(self.image, (self.x - self.r, self.y - self.r))

    def life(self):
        self.time += 1
        return self.time

    def check(self):
        pos = pygame.mouse.get_pos()
        if(math.sqrt((self.x - pos[0]) ** 2 + (self.y - pos[1]) ** 2) <= self.r):
            return True

    def hit(self, event, points, screen):
        return 0


class Rat:
    def __init__(self):
        self.r = 50

        self.x = random.randint(self.r, WIDTH - self.r)
        self.y = random.randint(self.r, HEIGHT - self.r)

        self.vx = 0
        self.vy = 0

        self.image = pygame.image.load("rat.png")#.convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.r * 2, self.r * 2))

        self.time = 0


    def move(self):
        pos = pygame.mouse.get_pos()
        mod = math.sqrt((self.x - pos[0]) ** 2 + (self.y - pos[1]) ** 2)

        if(mod <= 100):
            a = [(pos[0] - self.x) / mod, (pos[1] - self.y) / mod]
        else:
            a = [self.vx / 20, self.vy / 20]

        self.vx -= a[0]
        self.vy -= a[1]



        self.x += self.vx
        self.y += self.vy


        if (self.x + self.r >= WIDTH):
            self.x = self.r
        elif (self.x - self.r <= 0):
            self.x = WIDTH - self.r
        elif (self.y + self.r >= HEIGHT):
            self.y = self.r
        elif (self.y - self.r <= 0):
            self.y = HEIGHT - self.r



    def draw(self):
        screen.blit(self.image, (self.x - self.r, self.y - self.r))

    def life(self):
        self.time += 0.1
        return self.time

    def hit(self, event, points, screen):
        if (math.sqrt((event.pos[0] - self.x) ** 2 + (event.pos[1] - self.y) ** 2) <= self.r):
            points.add(10)
            screen.fill(WHITE)
            return True

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()
finished = False

balls = []
points = Points()

chance = [0, 0, 0, 0, 0, 0, 0, 1, 1, 2]

time_ = 0

death = False

def new():
    choice = random.choice(chance)
    if (choice == 0):
        return Ball()
    elif(chance == 1):
        return Skull()
    else:
        return Rat()

while not finished:
    screen.fill(WHITE)

    while(len(balls) < 3):
        balls.append(new())

    time_ += 1

    if(time_ >= 150):
        time_ = 0
        balls.append(new())

    for b in balls:
        b.draw()

    points.print()

    pygame.display.update()
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for b in balls:
                if b.hit(event, points, screen):
                    balls.remove(b)

    for b in balls:
        if(b.life() >= 200):
            balls.remove(b)
            if(type(b) == Ball):
                balls.append(Ball())

    for b in balls:
        b.move()

    for b in balls:
        if type(b) == Skull:
            if b.check() == True:
                finished = True
                death = True

if(death == True):
    screen.fill(BLACK)

    font = pygame.font.Font(None, int(WIDTH/4))
    text = font.render("YOU DIED", 1, RED)

    screen.blit(text, (50, int(HEIGHT/3)))

    font = pygame.font.Font(None, 72)
    text = font.render("Избегайте черепов!", 1, WHITE)

    screen.blit(text, (50, int(HEIGHT/3 + WIDTH/4)))

    str_score = "Набранное количество очков:" + str(points.get())
    text = font.render(str_score, 1, WHITE)

    screen.blit(text, (50, int(HEIGHT/3 + WIDTH/4 + 72)))

    pygame.display.update()

    pygame.mixer.music.load("death.mp3")
    pygame.mixer.music.play()

    pygame.time.delay(7000)


pygame.quit()