from abc import abstractmethod

import pygame, math, random

# rкакие-то параматры
FPS = 600
disc = 1 / 100
DARK_BLUE = (0, 0, 50)
YELLOW = (130, 130, 0)
screen_width = 1200
screen_hieght = 800
CENTER = (screen_width // 2, screen_hieght // 2)
# планеты
PLANETS = {
    "EARTH": (5000, 0.3, 20, 600, 150, (0, 10, 255))
}
# спутники
SPUTNIKS = {
    "EARTH": [[10], [0.1], [10], [600], [100],  [(255, 10, 255)]]
}
Planets_list = []


def sign(x): return 1 if x > 0 else -1


class Sun:
    """Центр системы(Солнце)"""
    mass = 1000  # надо будет найти массу солнца
    _details = 500

    def __init__(self, r=60, x=600, y=400, color: tuple = YELLOW, sigma=0.9):
        self.x = x
        self.y = y
        self.r = r
        self.color = color
        self.sigma = sigma

    def draw(self, screen) -> None:
        dots = []
        for i in range(1, self._details + 1):
            alfa = (2 * math.pi / self._details) * i
            gauss = random.gauss(0, self.sigma)
            x = self.x + (self.r + gauss) * math.cos(alfa)
            y = self.y + (self.r + gauss) * math.sin(alfa)
            dots.append((x, y))
        pygame.draw.polygon(screen, self.color, dots)

    @abstractmethod
    def move(self) -> None: ...

    @abstractmethod
    def f(self): ...


class Planet(Sun):
    _details = 100
    def __init__(self, mass, sigma, sputniks, *args):
        super().__init__(*args)
        self.mass = mass
        self.sigma = sigma
        self.a_x = 0
        self.a_y = 0
        self.sputniks = sputniks
        self.make_v_s()
        self.make_v(gelio)
        # self.make_v_s(gelio)

    def cos(self, planet):
        return (planet.x - self.x) / self.distance(planet)

    def sin(self, planet):
        return -(self.y - planet.y) / self.distance(planet)

    def make_v(self, helio):
        self.v_x = math.sqrt(helio.mass / self.distance(helio)) * 0.95
        self.v_y = math.sqrt(helio.mass / self.distance(helio)) * 0

    def move(self):
        # двигаем планету
        self.x += self.v_x * disc
        self.y += self.v_y * disc
        # двигаем спутник
        for sputnik in self.sputniks:
            sputnik.x += self.v_x * disc
            sputnik.y += self.v_y * disc
        # меняем скорость планеты
        self.v_x += self.a_x * disc
        self.v_y += self.a_y * disc
        # # меням скорость спутника относительно Солнца но не земли
        # self.sputnik.v_x += self.a_x * disc
        # self.sputnik.v_y += self.a_y * disc
        # обнуляем ускорение
        self.a_x = 0
        self.a_y = 0
        # делаем круговое вращение спутника по орбите планеты
        self.move_s()

    def f(self, planet):
        forse = planet.mass / self.distance(planet) ** 2
        self.a_x += self.cos(planet) * forse
        self.a_y += self.sin(planet) * forse
        self.f_s()

    def draw_planet(self, screen):
        dots = []
        for i in range(1, self._details + 1):
            alfa = (2 * math.pi / self._details) * i
            gauss = random.gauss(0, self.sigma)
            x = self.x + (self.r + gauss) * math.cos(alfa)
            y = self.y + (self.r + gauss) * math.sin(alfa)
            dots.append((x, y))
        pygame.draw.polygon(screen, self.color, dots)

    def draw(self, screen) -> None:
        self.draw_planet(screen)
        for sputnik in self.sputniks:
            sputnik.draw(screen)

    def speed(self):
        return (self.v_x ** 2 + self.v_y ** 2) ** 0.5

    def distance(self, planet):
        return math.sqrt((self.x - planet.x) ** 2 + (self.y - planet.y) ** 2)

    ### методы для спуников

    def move_s(self):
        for sputnik in self.sputniks:
            sputnik.move()

    def make_v_s(self):
        for sputnik in self.sputniks:
            sputnik.make_v(self)

    def f_s(self):
        for sputnik in self.sputniks:
            sputnik.f(self)


class Sputnik(Sun):
    _details = 50
    def __init__(self, mass, sigma, *args):
        super().__init__(*args)
        self.mass = mass
        self.sigma = sigma
        self.a_x = 0
        self.a_y = 0
        self.v_x = 0
        self.v_y = 0

    def cos(self, planet):
        return (planet.x - self.x) / self.distance(planet)

    def sin(self, planet):
        return -(self.y - planet.y) / self.distance(planet)

    def make_v(self, helio):
        self.v_x = math.sqrt(helio.mass / self.distance(helio))
        self.v_y = math.sqrt(helio.mass / self.distance(helio)) * 0

    def move(self):
        # двигаем спутник относительно планеты
        self.x += self.v_x * disc
        self.y += self.v_y * disc
        # # меняем скорость спутника относительно планеты
        self.v_x += self.a_x * disc
        self.v_y += self.a_y * disc
        # обнуляем ускорение
        self.a_x = 0
        self.a_y = 0

    def f(self, planet):
        forse = planet.mass / self.distance(planet) ** 2
        self.a_x += self.cos(planet) * forse
        self.a_y += self.sin(planet) * forse

    def speed(self):
        return (self.v_x ** 2 + self.v_y ** 2) ** 0.5

    def distance(self, planet):
        return math.sqrt((self.x - planet.x) ** 2 + (self.y - planet.y) ** 2)


def make_planet(mass, sigma, r, x, y, color, sputniks):
    return Planet(mass, sigma, sputniks, r, x, y, color)


def make_sputniks(masses, sigmas, r, x, y, colors):
    s_list = []
    for i in zip(masses, sigmas, r, x, y, colors):
        s_list.append(Sputnik(*i))
    return s_list



pygame.init()
screen = pygame.display.set_mode((screen_width, screen_hieght))
pygame.display.set_caption("Солнечная система")
clock = pygame.time.Clock()

# создадим солнце
gelio = Sun()
# создадим планеты
for planet, param in PLANETS.items():
    sputniks = make_sputniks(*SPUTNIKS[planet])
    Planets_list.append(make_planet(param[0], param[1], param[2], param[3], param[4], param[5], sputniks))

moon = Sputnik(10, 0.1, 10, 600, 200, (255, 10, 255))
planet1 = Planet(500, 0.3, [moon], 20, 600, 250, (0, 10, 255))

while True:

    clock.tick(FPS*10)
    screen.fill(DARK_BLUE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    gelio.draw(screen)
    for planet in Planets_list:
        planet.draw(screen)
        planet.move()
        planet.f(gelio)

    pygame.display.flip()
