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
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600


class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 300
        self.acc = 1

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

        # гравитация
        self.vy -= self.acc

        # сопротивление воздуха
        self.vy -= self.vy * 0.02
        self.vx -= self.vx * 0.02

        # перемещение
        self.x += self.vx
        self.y -= self.vy

        # останавливает шарик, если он на земле и у него маленькая скорость
        if self.vy ** 2 <= 1 and self.y >= HEIGHT - self.r and self.acc != 0:
            self.vy = 0
            self.acc = 0

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
        elif self.acc == 0:
            return False
        else:
            return False


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY

    def fire2_start(self, target):
        if target.live:
            self.f2_on = 1
        else:
            self.f2_on = 0


    def fire2_end(self, event, target):
        """
        Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        if target.live:
            bullet += 1
            new_ball = Ball(self.screen)
            new_ball.r += 5
            self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
            new_ball.vx = self.f2_power * math.cos(self.an)
            new_ball.vy = - self.f2_power * math.sin(self.an)
            balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((event.pos[1]-450) / (event.pos[0]-20))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        x0 = 40
        y0 = 450

        pos = pygame.mouse.get_pos()

        vect = [pos[0] - x0, pos[1] - y0]
        mod = math.sqrt(vect[0] ** 2 + vect[1] ** 2)
        vect = [vect[0]/mod, vect[1]/mod]
        norm = [-vect[1], vect[0]]

        length = 5 + self.f2_power / 10

        coordinates = [[x0 + norm[0] * 5, y0 + norm[1] * 5],
                       [x0 - norm[0] * 5, y0 - norm[1] * 5],
                       [x0 + (-norm[0] + vect[0] * length) * 5, y0 + (-norm[1] + vect[1] * length) * 5],
                       [x0 + (norm[0] + vect[0] * length) * 5, y0 + (norm[1] + vect[1] * length) * 5]]

        pygame.draw.polygon(screen, self.color, coordinates)

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
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
        """ Инициализация новой цели. """
        self.x = random.randint(600, 780)
        self.y = random.randint(300, 550)
        self.r = random.randint(2, 50)
        self.color = RED

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
            gun.fire2_start(target)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event, target)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    for b in balls:
        b.move()
        if b.hittest(target) and target.live:
            target.live = 0
            time = 0
            target.hit()
            target.new_target()

            bullet_mem = bullet

            bullet = 0



    for b in balls:
        if not b.life():
            balls.remove(b)


    gun.power_up()

pygame.quit()