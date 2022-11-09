import math
import random
from random import choice

import pygame


FPS = 60

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
DARK_GREEN = 0x317828
ORANGE = 0xFFBF00
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600


class Ball:
    def __init__(self, screen: pygame.Surface, x, y):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen

        self.x = x
        self.y = y

        self.r = 5

        self.vx = 0
        self.vy = 0

        self.color = BLACK

        self.live = 300

        self.acc = -1

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """

        # столкновение со стенам
        if(self.x + self.r >= WIDTH):
            self.vx = -self.vx
            self.x = WIDTH - self.r
        if(self.x - self.r <= 0):
            self.vx = -self.vx
            self.x = self.r
        if(self.y + self.r >= HEIGHT):
            self.vy = -self.vy
            self.y = HEIGHT - self.r
        if(self.y - self.r <= 0):
            self.vy = -self.vy
            self.y = self.r

        # ускорение свободного падения
        self.vy += self.acc

        # сопротивление воздуха
        self.vy -= self.vy * 0.02
        self.vx -= self.vx * 0.02

        # перемещение
        self.x += self.vx
        self.y -= self.vy # минус потому что ось y направлена вниз


    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if (math.sqrt((obj.x - self.x) ** 2 + (obj.y - self.y) ** 2) <= (obj.r + self.r)):
            return True
        else:
            return False

    def life(self):
        self.live -= 1
        if(self.live > 0):
            return True
        else:
            return False

class Rocket(Ball):
    def draw(self):
        pygame.draw.circle(self.screen, ORANGE, (self.x, self.y), self.r)

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
        pos = pygame.mouse.get_pos()
        mod = math.sqrt((self.x - pos[0]) ** 2 + (self.y - pos[1]) ** 2)
        a = [(self.x - pos[0]) / mod, (self.y - pos[1]) / mod]

        koef = 0.4

        self.vx -= a[0] * koef
        self.vy -= a[1] * koef

        self.x += self.vx
        self.y += self.vy

class Gun:
    def __init__(self, screen):
        self.screen = screen

        self.f2_power = 10

        self.f2_on = 0

        self.an = 1

        self.color = GREY

        self.r = 20

        self.x = 40
        self.y = 450

        self.v = 5

    def move(self):
        '''
        чтобы пушка двигалась
        '''

        key_arr = pygame.key.get_pressed()

        if(key_arr[100] == True):
            self.x += self.v
        elif(key_arr[97] == True):
            self.x -= self.v

        # столкновение со стенам
        if (self.x + self.r >= WIDTH):
            self.x = WIDTH - self.r
        if (self.x - self.r <= 0):
            self.x = self.r
        if (self.y + self.r >= HEIGHT):
            self.y = HEIGHT - self.r
        if (self.y - self.r <= 0):
            self.y = self.r

    def fire2_start(self, target, pressed):
        if target.live and (pressed == 0 or pressed == 2):
            self.f2_on = 1
        else:
            self.f2_on = 0


    def fire2_end(self, event, target, pressed):
        """
        Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        if target.live:
            bullet += 1
            if(pressed == 0):
                new_ball = Ball(self.screen, self.x, self.y)
                speed = 1
            elif(pressed == 2):
                new_ball = Rocket(self.screen, self.x, self.y)
                speed = 0.1
            else:
                return
            new_ball.r += 5
            self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
            new_ball.vx = self.f2_power * math.cos(self.an) * speed
            new_ball.vy = - self.f2_power * math.sin(self.an) * speed
            balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """
        Прицеливание. Зависит от положения мыши.
        """
        if event.pos[0] == self.x:
            a = self.x + 0.001
        else:
            a = event.pos[0]

        if event:
            self.an = math.atan((event.pos[1]-self.y) / (a-self.x))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        '''
        рисуем пушку
        '''

        # позиция мыши
        pos = pygame.mouse.get_pos()

        # единичный вектор, направленный от пушки к мыши, и нормальный ему
        vect = [pos[0] - self.x, pos[1] - self.y]
        mod = math.sqrt(vect[0] ** 2 + vect[1] ** 2)
        vect = [vect[0] / mod, vect[1] / mod]
        norm = [-vect[1], vect[0]]

        # рисуем корпус
        d = self.r
        D = self.r * 3 / 2
        pygame.draw.rect(self.screen, DARK_GREEN, (self.x - D / 2, self.y, D, d))

        # рисуем дуло
        length = 5 + self.f2_power / 10

        coordinates = [[self.x + norm[0] * 5, self.y + norm[1] * 5],
                       [self.x - norm[0] * 5, self.y - norm[1] * 5],
                       [self.x + (-norm[0] + vect[0] * length) * 5, self.y + (-norm[1] + vect[1] * length) * 5],
                       [self.x + (norm[0] + vect[0] * length) * 5, self.y + (norm[1] + vect[1] * length) * 5]]

        pygame.draw.polygon(self.screen, self.color, coordinates)
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), 5)


    def power_up(self):
        if self.f2_on:
            if self.f2_power < 50:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY

class Target:
    def __init__(self):
        self.points = 0
        self.live = 1
        self.new_target()

    def new_target(self):
        """
        Инициализация новой цели.
        """
        self.r = random.randint(5, 25)

        while True:
            self.x = random.randint(self.r, WIDTH - self.r)
            self.y = random.randint(self.r, HEIGHT - self.r)
            if(math.sqrt((self.x - gun.x) ** 2 + (self.y - gun.y) ** 2) >= 200):
                break

        self.vx = random.randint(2, 10)
        self.vy = random.randint(2, 10)

        self.color = RED

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
        self.y += self.vy

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
        pygame.draw.circle(screen, self.color, [self.x, self.y], self.r)




pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []

clock = pygame.time.Clock()
gun = Gun(screen)
target = Target()
finished = False

time = 0
bullet_mem = bullet

while not finished:
    screen.fill(WHITE)



    gun.draw()
    if target.live:
        target.draw()
    for b in balls:
        b.draw()



    # будет писать после каждого попадания сколько понадобилось шаров и запретит стрлять в течение нескольких секунд после
    if not target.live:
        if time <= 300:
            time += 1

            match bullet_mem % 10:
                case 1:
                    ending = ""
                case 2 | 3 | 4:
                    ending = "а"
                case _:
                    ending = "ов"

            message = "Вы уничтожили цель за " + str(bullet_mem) + " выстрел" + ending

            font = pygame.font.Font(None, 36)
            text1 = font.render(message, 1, BLACK)

            screen.blit(text1, (10, 50))

        else:
            target.live = 1

    pygame.display.update()
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_arr = pygame.mouse.get_pressed()
            for i in range(len(mouse_arr)):
                if (mouse_arr[i] == True):
                    pressed = i
            gun.fire2_start(target, pressed)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event, target, pressed)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    gun.move()

    for b in balls:
        b.move()
        if b.hittest(target) and target.live:
            target.live = 0
            time = 0
            target.hit()
            target.new_target()

            bullet_mem = bullet

            bullet = 0

    if target.live:
        target.move()

    for b in balls:
        if not b.life():
            balls.remove(b)





    gun.power_up()

pygame.quit()