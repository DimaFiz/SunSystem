import sys
from typing import Self, Literal
from abc import abstractmethod
import random, math, pygame
from dataclass import SpaceData

# какие-то параматры
G = SpaceData.G
FPS = SpaceData.FPS
dt = SpaceData.dt
DARK_BLUE = SpaceData.DARK_BLUE
YELLOW = SpaceData.YELLOW
screen_width = SpaceData.screen_width
screen_height = SpaceData.screen_height
CENTER = SpaceData.CENTER
# планеты
PLANETS = SpaceData.PLANETS
# спутники
SATELLITES = SpaceData.SATELLITES


class Vector:
    """Vector"""

    @classmethod
    def creator(cls, *args):
        return cls(args)

    def __init__(self, x: int, y: int) -> Self:
        self.x = x
        self.y = y

    def __add__(self, other: Self) -> Self:
        return self.v_on_startector(self.x + other.x, self.y + other.y)

    def __sub__(self, other) -> Self:
        return self.v_on_startector(self.x - other.x, self.y - other.y)

    def __mul__(self, other) -> Self:
        return self.v_on_startector(self.x * other, self.y * other)

    def __rmul__(self, other) -> Self:
        return self.v_on_startector(self.x * other, self.y * other)

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y

    def __ne__(self, other) -> bool:
        return self.x != other.x or self.y != other.y

    def reverse(self) -> Self:
        return self.v_on_startector(-self.x, -self.y)

    def e_v(self):  # единичный вектор
        c = self.x ** 2 + self.y ** 2
        return self.creator(self.x / c, self.y / c)

    def abs(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    @classmethod
    def v_on_startector(cls, x, y) -> Self:
        return cls(x, y)


class Acceleration(Vector): ...


class Speed(Vector): ...


FAKE_RADIUS = 1
FAKE_CORDS = 1


class Sun:
    global FAKE_RADIUS, FAKE_CORCS
    """Центр системы(Солнце)"""

    mass = 1.98892e30  # надо будет найти массу солнца
    _details = 500
    sigma = 0.9

    # для отрисовки
    dx = SpaceData.screen_width / 2
    dy = SpaceData.screen_height / 2

    def __init__(
            self, r=6_963_400, x=0, y=0, color: tuple = YELLOW, name=None
    ) -> Self:
        self.x = x
        self.y = y
        self.r = r
        self.color = color
        self.name = name
        self.sputniks = []
        self.v = Speed(0, 0)
        self.a = Acceleration(0, 0)

    def __eq__(self, other) -> bool:
        return self.name == other.name

    def draw(self, screen) -> None:
        x_ = self.x / FAKE_CORDS + self.dx
        y_ = self.y / FAKE_CORDS + self.dy
        r_ = self.r / FAKE_RADIUS
        dots = []
        for i in range(1, self._details + 1):
            alfa = (2 * math.pi / self._details) * i
            gauss = random.gauss(0, self.sigma)
            x = x_ + (r_ + gauss) * math.cos(alfa)
            y = y_ + (r_ + gauss) * math.sin(alfa)
            dots.append((x, y))
        pygame.draw.polygon(screen, self.color, dots)

    def __iadd__(self, other) -> None:
        if isinstance(other, Speed):
            self.x += other.x
            self.y += other.y
        if isinstance(other, Acceleration):
            self.v += other
        return self

    def append(self, sputnik) -> None:
        self.sputniks.append(sputnik)

    def get_sputniks(self) -> None:
        return self.sputniks

    def d(self, planet) -> None:
        return math.sqrt((self.x - planet.x) ** 2 + (self.y - planet.y) ** 2)

    @abstractmethod
    def move(self) -> None:
        ...

    @abstractmethod
    def f(self, *args):
        ...

    @abstractmethod
    def v_on_start(self, helio):
        ...


class SpaceObject(Sun):
    _details = 100
    sigma = 0.3

    # def __init__(self, gelio, mass, sigma, sputniks=None, *args) -> None:
    def __init__(self, center, /, *, mass, name, r, distance, color):
        self.center = center
        self.mass = mass
        self.name = name
        self.r = r
        self.x = 0
        self.y = distance - center.x
        self.color = color
        self.v = Speed(0, 0)
        self.a = Acceleration(0, 0)

    def __str__(self) -> str:
        return f"{self.name} ({self.x}, {self.y})"

    def cos(self, planet) -> None:
        return (planet.x - self.x) / self.d(planet)

    def sin(self, planet) -> None:
        return -(self.y - planet.y) / self.d(planet)

    def v_on_start(self, helio):
        a = math.sqrt(SpaceData.G * helio.mass / self.d(helio))
        self.v += Speed(a, 0)

    def move(self) -> None:
        self += self.v * dt
        self.v += self.a * dt
        self.a = Acceleration(0, 0)

    def f(self, planet) -> None:
        if self is planet:
            return None
        try:
            a = SpaceData.G * planet.mass / self.d(planet) ** 2
            self.a += Acceleration(a * self.cos(planet), a * self.sin(planet))
        except ZeroDivisionError:
            return None


def draw(screen, center, planet):
    global FAKE_RADIUS, FAKE_CORDS
    x_ = planet.x / FAKE_CORDS - center.x / FAKE_CORDS + planet.dx
    y_ = planet.y / FAKE_CORDS - center.y / FAKE_CORDS + planet.dy
    r_ = planet.r / FAKE_RADIUS
    dots = []
    for i in range(1, planet._details + 1):
        alfa = (2 * math.pi / planet._details) * i
        gauss = random.gauss(0, planet.sigma)
        x = x_ + (r_ + gauss) * math.cos(alfa)
        y = y_ + (r_ + gauss) * math.sin(alfa)
        dots.append((x, y))
    pygame.draw.polygon(screen, planet.color, dots)


def sun(fake_radius, fake_cords):
    global FAKE_RADIUS, FAKE_CORDS
    FAKE_RADIUS = fake_radius
    FAKE_CORDS = fake_cords
    SPACE_OBJECTS = []
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Солнечная система")
    clock = pygame.time.Clock()
    sun_ = Sun()
    SPACE_OBJECTS.append(sun_)
    for planet in PLANETS:
        SPACE_OBJECTS.append(SpaceObject(sun_, **PLANETS[planet]))
        SPACE_OBJECTS[-1].v_on_start(sun_)

    for planet in SPACE_OBJECTS:
        if planet.name in SATELLITES:
            for st in SATELLITES[planet.name]:
                SPACE_OBJECTS.append(SpaceObject(sun_, **SATELLITES[planet.name][st]))
                SPACE_OBJECTS[-1].v_on_start(sun_)
                SPACE_OBJECTS[-1].v_on_start(planet)

    print(SPACE_OBJECTS)
    while True:
        clock.tick(60)
        screen.fill(DARK_BLUE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        for obj1 in SPACE_OBJECTS:
            for obj2 in SPACE_OBJECTS:
                obj1.f(obj2)

        for obj in SPACE_OBJECTS:
            obj.move()
            draw(screen, sun_, obj)
            # if obj.name == "MERCURY":
            #     print(obj)

        pygame.display.flip()


def earth(fake_radius, fake_cords):
    global FAKE_RADIUS, FAKE_CORDS
    FAKE_RADIUS = fake_radius
    FAKE_CORDS = fake_cords
    SPACE_OBJECTS = []
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Солнечная система")
    clock = pygame.time.Clock()
    sun_ = Sun()
    earth_ = None
    SPACE_OBJECTS.append(sun_)
    for planet in PLANETS:
        SPACE_OBJECTS.append(SpaceObject(sun_, **PLANETS[planet]))
        if planet == "EARTH":
            earth_ = SPACE_OBJECTS[-1]
        SPACE_OBJECTS[-1].v_on_start(sun_)
    for planet in SPACE_OBJECTS:
        if planet.name in SATELLITES:
            for st in SATELLITES[planet.name]:
                SPACE_OBJECTS.append(SpaceObject(sun_, **SATELLITES[planet.name][st]))
                SPACE_OBJECTS[-1].v_on_start(sun_)
                SPACE_OBJECTS[-1].v_on_start(planet)

    while True:
        clock.tick(60)
        screen.fill(DARK_BLUE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        for obj1 in SPACE_OBJECTS:
            for obj2 in SPACE_OBJECTS:
                obj1.f(obj2)

        for obj in SPACE_OBJECTS:
            obj.move()
            draw(screen, earth_, obj)
            draw(screen, earth_, obj)
            # if obj.name == "MERCURY":
            #     print(obj)

        pygame.display.flip()


def my_center(name: Literal['EARTH', 'MARS', 'JUPITER', 'SATURN', 'URANUS', 'NEPTUNE'], fake_radius,
              fake_cords):
    global FAKE_RADIUS, FAKE_CORDS
    FAKE_RADIUS = fake_radius
    FAKE_CORDS = fake_cords
    SPACE_OBJECTS = []
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Солнечная система")
    clock = pygame.time.Clock()
    sun_ = Sun()
    center_ = None
    SPACE_OBJECTS.append(sun_)
    for planet in PLANETS:
        SPACE_OBJECTS.append(SpaceObject(sun_, **PLANETS[planet]))
        if planet == name:
            center_ = SPACE_OBJECTS[-1]
        SPACE_OBJECTS[-1].v_on_start(sun_)
    for planet in SPACE_OBJECTS:
        if planet.name in SATELLITES:
            for st in SATELLITES[planet.name]:
                SPACE_OBJECTS.append(SpaceObject(sun_, **SATELLITES[planet.name][st]))
                SPACE_OBJECTS[-1].v_on_start(sun_)
                SPACE_OBJECTS[-1].v_on_start(planet)

    while True:
        clock.tick(60)
        screen.fill(DARK_BLUE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        for obj1 in SPACE_OBJECTS:
            for obj2 in SPACE_OBJECTS:
                obj1.f(obj2)

        for obj in SPACE_OBJECTS:
            obj.move()
            draw(screen, center_, obj)
            draw(screen, center_, obj)

        pygame.display.flip()
