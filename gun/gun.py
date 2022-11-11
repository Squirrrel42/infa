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

WIDTH = 1000
HEIGHT = 800


class Ball:
    def __init__(self, screen: pygame.Surface, x, y, live_long):
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

        self.vect = [0, 0]

        self.color = BLACK

        self.live = live_long

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

        # получим единичный вектор, направленный вдоль скорости
        self.vect = [self.vx, self.vy]
        mod = math.sqrt(self.vx ** 2 + self.vy ** 2)
        if(mod == 0):
            self.vect = [0, 0]
        else:
            self.vect = [self.vect[0] / mod, self.vect[1] / mod]

        coordinates = [[self.x + self.vect[1] * 10 - self.vect[0] * self.r, self.y - self.vect[0] * 10 - self.vect[1] * self.r],
                       [self.x - self.vect[1] * 10 - self.vect[0] * self.r, self.y + self.vect[0] * 10 - self.vect[1] * self.r],
                       [self.x + self.vect[0] * self.r, self.y + self.vect[1] * self.r]]

        pygame.draw.polygon(self.screen, ORANGE, coordinates)

    def move(self):
        for i in range(5):
            particles.append(Particle(b.x, b.y, b.vx, b.vy, b.vect))

        # столкновение со стенам
        if (self.x + self.r >= WIDTH):
            self.vx = -self.vx / 10
            self.x = WIDTH - self.r
        if (self.x - self.r <= 0):
            self.vx = -self.vx / 10
            self.x = self.r
        if (self.y + self.r >= HEIGHT):
            self.vy = -self.vy / 10
            self.y = HEIGHT - self.r
        if (self.y - self.r <= 0):
            self.vy = -self.vy / 10
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
        self.y = HEIGHT - self.r

        self.v = 5

        self.cannonball_amount = 5
        self.rocket_amount = 1

        self.reload_time = FPS * 5
        self.reload_time_current = self.reload_time
        self.is_reload = False

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

    def move(self, key_arr):
        '''
        чтобы пушка двигалась
        '''

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

    def reload(self, key_arr):
        if not self.is_reload:
            if key_arr[114]:
                self.is_reload = True
                self.color = RED
        else:
            if self.reload_time_current > 0:
                self.reload_time_current -= 1
            else:
                reload_sound = pygame.mixer.Sound("reload.wav")
                reload_sound.play()

                self.cannonball_amount = 5
                self.rocket_amount = 1

                self.reload_time_current = self.reload_time
                self.is_reload = False
                self.color = GREY

    def targetting(self, event):
        """
        Прицеливание. Зависит от положения мыши.
        """
        if event.pos[0] == self.x:
            a = self.x + 0.001
        else:
            a = event.pos[0]

        self.an = math.atan((event.pos[1]-self.y) / (a-self.x))

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 50:
                self.f2_power += 1
            if self.color != RED:
                self.color = YELLOW
        elif self.color != RED:
            self.color = GREY

    def fire2_start(self, condition, pressed):
        if condition and (pressed == 0 and self.cannonball_amount > 0 or pressed == 2 and self.rocket_amount > 0) and not self.is_reload:
            self.f2_on = 1
        else:
            self.f2_on = 0

    def fire2_end(self, event, condition, pressed):
        """
        Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        if condition and not self.is_reload:
            bullet += 1

            if pressed == 0 and self.cannonball_amount > 0:
                self.cannonball_amount -= 1
                new_ball = Ball(self.screen, self.x, self.y, 300)
                speed = 1

            elif pressed == 2 and self.rocket_amount > 0:
                self.rocket_amount -= 1
                new_ball = Rocket(self.screen, self.x, self.y, FPS * 9)
                speed = 0.1
                rocket_fly.play()
            else:
                return
            new_ball.r += 5
            self.an = math.atan2((event.pos[1] - new_ball.y), (event.pos[0] - new_ball.x))
            new_ball.vx = self.f2_power * math.cos(self.an) * speed
            new_ball.vy = - self.f2_power * math.sin(self.an) * speed
            balls.append(new_ball)

            shoot = pygame.mixer.Sound("shoot.wav")
            shoot.play()
        self.f2_on = 0
        self.f2_power = 10


class Target:
    def __init__(self):
        self.points = 0
        self.live = 1

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


class Second(Target):
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

        for b in balls:
            vect = [b.x, b.y]
            mod = math.sqrt((self.x - vect[0]) ** 2 + (self.y - vect[1]) ** 2)

            if (mod <= 100):
                a = [(vect[0] - self.x) / mod, (vect[1] - self.y) / mod]
            else:
                a = [self.vx / 20, self.vy / 20]

            self.vx -= a[0]
            self.vy -= a[1]

            self.x += self.vx
            self.y += self.vy


class Particle:
    def __init__(self, x, y, vx, vy, vect, life_long=20, colour=ORANGE):
        self.angle = random.randint(-10, 10) * math.pi / 10

        self.x = x
        self.y = y

        self.vx = (vx * math.cos(self.angle) - vy * math.sin(self.angle)) / 5
        self.vy = (vx * math.sin(self.angle) + vy * math.cos(self.angle)) / 5

        self.vect = vect

        self.acc = -0.2

        self.life_long = life_long

        self.colour = colour

    def move(self):
        # ускорение свободного падения
        self.vy += self.acc

        # сопротивление воздуха
        self.vy -= self.vy * 0.02
        self.vx -= self.vx * 0.02

        # перемещение
        self.x += self.vx
        self.y -= self.vy  # минус потому что ось y направлена вниз

    def draw(self):
        pygame.draw.circle(screen, self.colour, (self.x, self.y), 2)

    def life(self):
        if self.life_long > 0:
            self.life_long -= 1
            return True
        else:
            return False


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []
gun = Gun(screen)

def random_target():
    choice_target = random.randint(0, 1)
    if choice_target == 0:
        return Target()
    if choice_target == 1:
        return Second()
    return Target()

targets = [random_target(), random_target()]
particles = []

any_live = True

clock = pygame.time.Clock()
finished = False

time = 0
bullet_mem = bullet

time_rocket = FPS
rocket_fly = pygame.mixer.Sound("rocket3.wav")

font_size = 36
font = pygame.font.Font(None, font_size)

pressed = 0

while not finished:
    screen.fill(WHITE)

    ammo_str = "Ядра: " + str(gun.cannonball_amount) + "; Ракеты: " + str(gun.rocket_amount)
    text = font.render(ammo_str, 1, BLACK)
    screen.blit(text, (10, 50))

    text = font.render("ЛКМ — Ядро", 1, BLACK)
    screen.blit(text, (10, 50 + font_size))

    text = font.render("ПКМ — Ракета", 1, BLACK)
    screen.blit(text, (10, 50 + font_size * 2))

    text = font.render("[R] — Перезарядка", 1, BLACK)
    screen.blit(text, (10, 50 + font_size * 3))

    if gun.is_reload:
        reload_time_text = "Идёт перезарядка: " + str(math.floor(gun.reload_time_current / FPS))
        text = font.render(reload_time_text, 1, BLACK)
        screen.blit(text, (10, 50 + font_size * 4))

    for p in particles:
        p.draw()
        p.move()

    key_arr = pygame.key.get_pressed()

    gun.draw()
    gun.move(key_arr)
    gun.reload(key_arr)

    for t in targets:
        if t.live:
            t.draw()

    for b in balls:
        b.move()
        b.draw()

    # будет писать после каждого попадания сколько понадобилось шаров и запретит стрлять в течение нескольких секунд после
    if not any_live:
        if time <= FPS * 9:
            time += 1

            match bullet_mem % 100:
                case 11 | 12 | 13 | 14:
                    ending = "ов"
                case _:
                    match bullet_mem % 10:
                        case 1:
                            ending = ""
                        case 2 | 3 | 4:
                                ending = "а"
                        case _:
                            ending = "ов"

            message = "Вы уничтожили цель за " + str(bullet_mem) + " выстрел" + ending

            text1 = font.render(message, 1, BLACK)

            screen.blit(text1, (10, 50 - font_size))

        else:
            any_live = True

            for t in targets:
                t.live = 1

    pygame.display.update()
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_arr = pygame.mouse.get_pressed()
            for i in range(len(mouse_arr)):
                if mouse_arr[i]:
                    pressed = i
            condition = False
            for t in targets:
                if t.live:
                    condition = True
                    break
            gun.fire2_start(condition, pressed)
        elif event.type == pygame.MOUSEBUTTONUP:
            condition = False
            for t in targets:
                if t.live:
                    condition = True
                    break
            gun.fire2_end(event, condition, pressed)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    is_rocket = 0
    for b in balls: # попадание
        for t in targets:
            if b.hittest(t) and t.live:
                explosion = pygame.mixer.Sound("Explosion2.wav")
                explosion.play()

                for i in range(100):
                    particles.append(Particle(t.x, t.y, random.randint(-15, 15), random.randint(1, 15) - 20, [0, -1], 100, RED))

                t.live = 0
                time = 0
                t.hit()
                t = random_target()

    any_live = False
    for t in targets:
        if t.live:
            t.move()
            any_live = True
        else:
            bullet_mem = bullet

    for b in balls:
        if not b.life():
            balls.remove(b)

    for p in particles:
        if not p.life():
            particles.remove(p)

    gun.power_up()

pygame.quit()
