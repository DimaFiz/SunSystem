import sys
from typing import Self, Literal
from abc import abstractmethod
import random
import math
import pygame
from dataclass import SpaceData

"""Parameters"""
G = SpaceData.G  # gravitational constant
FPS = SpaceData.FPS
dt = SpaceData.dt
DARK_BLUE = SpaceData.DARK_BLUE
YELLOW = SpaceData.YELLOW
screen_width = SpaceData.screen_width
screen_height = SpaceData.screen_height
CENTER = SpaceData.CENTER

"""Planets"""
PLANETS = SpaceData.PLANETS

"""Sputniks"""
SATELLITES = SpaceData.SATELLITES

PLANET_TO_SUN_RADIUS_RATIO = SpaceData.PLANET_TO_SUN_RADIUS_RATIO


class Vector:
    """Vector."""

    @classmethod
    def creator(cls, *args):
        """Create vector."""
        return cls(args)

    def __init__(self, x: int, y: int) -> Self:
        """X and Y."""
        self.x = x
        self.y = y

    def __add__(self, other: Self) -> Self:
        """Vector1 + Vector2."""
        return self.v_on_startvector(self.x + other.x, self.y + other.y)

    def __sub__(self, other) -> Self:
        """Vector1 - Vector2."""
        return self.v_on_startvector(self.x - other.x, self.y - other.y)

    def __mul__(self, other) -> Self:
        """Vector * Const."""
        return self.v_on_startvector(self.x * other, self.y * other)

    def __rmul__(self, other) -> Self:
        """Const * Vector1."""
        return self.v_on_startvector(self.x * other, self.y * other)

    def __eq__(self, other) -> bool:
        """Vector1 == Vector2."""
        return self.x == other.x and self.y == other.y

    def __ne__(self, other) -> bool:
        """Vector1 != Vector2."""
        return self.x != other.x or self.y != other.y

    def reverse(self) -> Self:
        """-Vector."""
        return self.v_on_startvector(-self.x, -self.y)

    def e_v(self) -> Self:  # unit vector
        """Turn to unit vector."""
        c = self.x ** 2 + self.y ** 2
        return self.creator(self.x / c, self.y / c)

    def abs(self) -> Self:
        """Abs(vector)."""
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def __str__(self) -> str:
        """Print vector."""
        return f"({self.x}, {self.y})"

    @classmethod
    def v_on_startvector(cls, x, y) -> Self:
        """Make class constructor."""
        return cls(x, y)


class Acceleration(Vector):
    """Planet's acceleration."""

    ...


class Speed(Vector):
    """Planet's speed."""

    ...


FAKE_RADIUS = 1
FAKE_CORDS = 1


class Sun:
    """System's center (Sun)."""

    mass = 1.98892e30
    _details = 500
    sigma = 0.9

    def __init__(self, r=6_963_400, x=0, y=0,
                 color: tuple = YELLOW, name=None) -> Self:
        """Parameteres."""
        self.x = x
        self.y = y
        self.r = r
        self.color = color
        self.name = name
        self.sputniks = []
        self.v = Speed(0, 0)
        self.a = Acceleration(0, 0)

    def __eq__(self, other) -> bool:
        """Comparison."""
        return self.name == other.name

    def __iadd__(self, other) -> None:
        """Vector change."""
        if isinstance(other, Speed):
            self.x += other.x
            self.y += other.y
        if isinstance(other, Acceleration):
            self.v += other
        return self

    def append(self, sputnik) -> None:
        """Add sputnik."""
        self.sputniks.append(sputnik)

    def get_sputniks(self) -> None:
        """Return sputniks."""
        return self.sputniks

    def d(self, planet) -> None:
        """Distance between planets."""
        return math.sqrt((self.x - planet.x) ** 2
                         + (self.y - planet.y) ** 2)

    def change(self, mass: int, r: int,
               name: str, distance: int, color: tuple) -> None:
        """Change parameters."""
        self.mass = mass
        self.r = r
        self.name = name
        self.distance = distance
        self.color = color

    def it_is_dark_hole(self) -> None:
        self.mass = 10e100
        self.color = (0, 0, 0)

    def get_section(self):
        return (self.sgn(self.x), self.sgn(self.y))

    def light_speed(self):
        self.v = Speed(3e8, 0)

    @staticmethod
    def sgn(x):
        return -1 if x < 0 else 1

    @abstractmethod
    def move(self) -> None:
        """Object move."""
        ...

    @abstractmethod
    def f(self, *args):
        """Space object's interaction."""
        ...

    @abstractmethod
    def v_on_start(self, helio):
        """Speed start vector."""
        ...


class SpaceObject(Sun):
    """Planets."""

    _details = 100
    sigma = 0.3

    def __init__(self, center, /, *, mass, name, r, distance, color) -> Self:
        """Planet's parameteres."""
        self.center = center
        self.mass = mass
        self.name = name
        self.r = r  # radius
        self.x = 0
        self.y = distance - center.x
        self.color = color
        self.v = Speed(0, 0)
        self.a = Acceleration(0, 0)

    def __str__(self) -> str:
        """Print planet's vector."""
        return f"{self.name} ({self.x}, {self.y})"

    def cos(self, planet) -> None:
        """Planet's cosinus."""
        return (planet.x - self.x) / self.d(planet)

    def sin(self, planet) -> None:
        """Planet's sinus."""
        return -(self.y - planet.y) / self.d(planet)

    def v_on_start(self, helio):
        """Speed start vector."""
        a = math.sqrt(SpaceData.G * helio.mass / self.d(helio))
        self.v += Speed(a, 0)

    def move(self) -> None:
        """Object move."""
        self += self.v * dt
        self.v += self.a * dt
        self.a = Acceleration(0, 0)

    def f(self, planet) -> None:
        """Space object's interaction."""
        if self is planet:
            return None
        try:
            a = SpaceData.G * planet.mass / self.d(planet) ** 2
            self.a += Acceleration(a * self.cos(planet), a * self.sin(planet))
        except ZeroDivisionError:
            return None


dx = screen_width / 2
dy = screen_height / 2


def draw(screen, center, planet):
    """Display."""
    x_ = planet.x / FAKE_CORDS - center.x / FAKE_CORDS + dx
    y_ = planet.y / FAKE_CORDS - center.y / FAKE_CORDS + dy
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
    """Sun display."""
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
                SPACE_OBJECTS.append(SpaceObject(
                    sun_, **SATELLITES[planet.name][st]))
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
            draw(screen, sun_, obj)

        pygame.display.flip()


def earth(fake_radius, fake_cords):
    """Earth display."""
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
                SPACE_OBJECTS.append(SpaceObject(
                    sun_, **SATELLITES[planet.name][st]))
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

        pygame.display.flip()


def my_center(
        name: Literal["EARTH", "MARS", "JUPITER", "SATURN", "URANUS", "NEPTUNE"],
        fake_radius,
        fake_cords,
):
    """Define system's center."""
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
                SPACE_OBJECTS.append(SpaceObject(
                    sun_, **SATELLITES[planet.name][st]))
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


def run():
    """Programme run."""
    global FAKE_RADIUS, FAKE_CORDS, dx, dy
    fake_radius = 400_000
    fake_cords = 1_000_000_000
    FAKE_RADIUS = fake_radius * 100
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
        SPACE_OBJECTS[-1].v_on_start(sun_)
    for planet in SPACE_OBJECTS:
        if planet.name in SATELLITES:
            for st in SATELLITES[planet.name]:
                SPACE_OBJECTS.append(SpaceObject(
                    sun_, **SATELLITES[planet.name][st]))
                SPACE_OBJECTS[-1].v_on_start(sun_)
                SPACE_OBJECTS[-1].v_on_start(planet)
    center_ = sun_

    # Переменные для управления удержанием клавиш
    last_zoom_time = 0
    zoom_interval = 50  # интервал в мсек между изменениями при удержании
    last_move_time = 0
    move_interval = 16  # примерно 60 FPS

    while True:
        current_time = pygame.time.get_ticks()
        clock.tick(60)
        screen.fill(DARK_BLUE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == 61:  # +
                    FAKE_RADIUS /= 1.1
                    FAKE_CORDS /= 1.1
                elif event.key == 45:  # -
                    FAKE_RADIUS *= 1.1
                    FAKE_CORDS *= 1.1
                elif 47 < event.key < 57:
                    center_ = SPACE_OBJECTS[event.key - 48]
                    FAKE_RADIUS = fake_radius * (
                            PLANET_TO_SUN_RADIUS_RATIO[
                                SPACE_OBJECTS[event.key - 48].name]
                            * 100
                    )
                    FAKE_CORDS = (
                            fake_cords
                            * PLANET_TO_SUN_RADIUS_RATIO[
                                SPACE_OBJECTS[event.key - 48].name]
                    )
                    dx = screen_width / 2
                    dy = screen_height / 2

        # Обработка удержания клавиш масштабирования
        keys = pygame.key.get_pressed()
        if current_time - last_zoom_time > zoom_interval:
            if keys[pygame.K_EQUALS] or keys[pygame.K_PLUS]:  # + или =
                FAKE_RADIUS /= 1.1
                FAKE_CORDS /= 1.1
                last_zoom_time = current_time
            elif keys[pygame.K_MINUS]:  # -
                FAKE_RADIUS *= 1.1
                FAKE_CORDS *= 1.1
                last_zoom_time = current_time

        # Обработка удержания клавиш перемещения
        if current_time - last_move_time > move_interval:
            move_speed = 10  # скорость перемещения

            # Стрелка влево (1073741904)
            if keys[pygame.K_LEFT]:
                dx -= move_speed
                last_move_time = current_time
            # Стрелка вверх (1073741906)
            elif keys[pygame.K_UP]:
                dy -= move_speed
                last_move_time = current_time
            # Стрелка вниз (1073741905)
            elif keys[pygame.K_DOWN]:
                dy += move_speed
                last_move_time = current_time
            # Стрелка вправо (1073741903)
            elif keys[pygame.K_RIGHT]:
                dx += move_speed
                last_move_time = current_time

        # Физика и отрисовка
        for obj1 in SPACE_OBJECTS:
            for obj2 in SPACE_OBJECTS:
                obj1.f(obj2)

        for obj in SPACE_OBJECTS:
            obj.move()
            draw(screen, center_, obj)

        pygame.display.flip()


def trappist_1(fake_radius, fake_cords):
    """Создание обычных переменных из класса SpaceData"""
    TRAPPIST_1 = SpaceData.TRAPPIST_1
    TRAPPIST_1_PLANETS = SpaceData.TRAPPIST_1_PLANETS
    TRAPPIST_1_SATELLITES = SpaceData.TRAPPIST_1_SATELLITES
    TRAPPIST_1_TO_STAR_RADIUS_RATIO = SpaceData.TRAPPIST_1_TO_STAR_RADIUS_RATIO
    global FAKE_RADIUS, FAKE_CORDS, dx, dy
    FAKE_RADIUS = fake_radius
    FAKE_CORDS = fake_cords
    SPACE_OBJECTS = []
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Солнечная система")
    clock = pygame.time.Clock()
    sun_ = Sun()
    center_ = sun_
    sun_.change(**TRAPPIST_1)
    SPACE_OBJECTS.append(sun_)
    for planet in TRAPPIST_1_PLANETS:
        SPACE_OBJECTS.append(SpaceObject(sun_, **TRAPPIST_1_PLANETS[planet]))
        SPACE_OBJECTS[-1].v_on_start(sun_)

    for planet in SPACE_OBJECTS:
        if planet.name in TRAPPIST_1_SATELLITES:
            for st in TRAPPIST_1_SATELLITES[planet.name]:
                SPACE_OBJECTS.append(
                    SpaceObject(sun_, **TRAPPIST_1_SATELLITES[planet.name][st])
                )
                SPACE_OBJECTS[-1].v_on_start(sun_)
                SPACE_OBJECTS[-1].v_on_start(planet)
    last_zoom_time = 0
    zoom_interval = 50  # интервал в мсек между изменениями при удержании
    last_move_time = 0
    move_interval = 16

    while True:

        current_time = pygame.time.get_ticks()
        clock.tick(FPS)
        screen.fill(DARK_BLUE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == 61:  # +
                    FAKE_RADIUS /= 1.1
                    FAKE_CORDS /= 1.1
                elif event.key == 45:  # -
                    FAKE_RADIUS *= 1.1
                    FAKE_CORDS *= 1.1
                elif 47 < event.key < 56:
                    center_ = SPACE_OBJECTS[event.key - 48]
                    FAKE_RADIUS = fake_radius * (
                        TRAPPIST_1_TO_STAR_RADIUS_RATIO[
                            SPACE_OBJECTS[event.key - 48].name
                        ]
                    )
                    FAKE_CORDS = (
                            fake_cords
                            * TRAPPIST_1_TO_STAR_RADIUS_RATIO[
                                SPACE_OBJECTS[event.key - 48].name
                            ]
                    )
                    dx = screen_width / 2
                    dy = screen_height / 2

        # Обработка удержания клавиш масштабирования
        keys = pygame.key.get_pressed()
        if current_time - last_zoom_time > zoom_interval:
            if keys[pygame.K_EQUALS] or keys[pygame.K_PLUS]:  # + или =
                FAKE_RADIUS /= 1.1
                FAKE_CORDS /= 1.1
                last_zoom_time = current_time
            elif keys[pygame.K_MINUS]:  # -
                FAKE_RADIUS *= 1.1
                FAKE_CORDS *= 1.1
                last_zoom_time = current_time

        # Обработка удержания клавиш перемещения
        if current_time - last_move_time > move_interval:
            move_speed = 10  # скорость перемещения

            # Стрелка влево (1073741904)
            if keys[pygame.K_LEFT]:
                dx -= move_speed
                last_move_time = current_time
            # Стрелка вверх (1073741906)
            elif keys[pygame.K_UP]:
                dy -= move_speed
                last_move_time = current_time
            # Стрелка вниз (1073741905)
            elif keys[pygame.K_DOWN]:
                dy += move_speed
                last_move_time = current_time
            # Стрелка вправо (1073741903)
            elif keys[pygame.K_RIGHT]:
                dx += move_speed
                last_move_time = current_time

        for obj1 in SPACE_OBJECTS:
            for obj2 in SPACE_OBJECTS:
                obj1.f(obj2)

        for obj in SPACE_OBJECTS:
            obj.move()
            draw(screen, center_, obj)
        pygame.display.flip()


def dark_hole(
        fake_radius: int = 10_000_000,
        fake_cords=10_000_000_000,
        PLANETS: dict = PLANETS,
        SATELLITES: dict = SATELLITES,
) -> None:
    """Dark Hole Display"""

    global FAKE_RADIUS, FAKE_CORDS, dt, dx, dy
    dt = 10e-30
    FAKE_RADIUS = fake_radius
    FAKE_CORDS = fake_cords
    SPACE_OBJECTS = []
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Солнечная система")
    clock = pygame.time.Clock()
    center_ = Sun()
    center_.it_is_dark_hole()
    SPACE_OBJECTS.append(center_)
    for planet in PLANETS:
        SPACE_OBJECTS.append(SpaceObject(center_, **PLANETS[planet]))
        SPACE_OBJECTS[-1].light_speed()
    for planet in SPACE_OBJECTS:
        if planet.name in SATELLITES:
            for st in SATELLITES[planet.name]:
                SPACE_OBJECTS.append(
                    SpaceObject(center_, **SATELLITES[planet.name][st])
                )
                SPACE_OBJECTS[-1].light_speed()
    # Переменные для управления удержанием клавиш
    last_zoom_time = 0
    zoom_interval = 50  # интервал в мсек между изменениями при удержании
    last_move_time = 0
    move_interval = 16  # примерно 60 FPS

    while True:
        current_time = pygame.time.get_ticks()
        clock.tick(60)
        screen.fill(DARK_BLUE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == 61:  # +
                    FAKE_RADIUS /= 1.1
                    FAKE_CORDS /= 1.1
                elif event.key == 45:  # -
                    FAKE_RADIUS *= 1.1
                    FAKE_CORDS *= 1.1

        # Обработка удержания клавиш масштабирования
        keys = pygame.key.get_pressed()
        if current_time - last_zoom_time > zoom_interval:
            if keys[pygame.K_EQUALS] or keys[pygame.K_PLUS]:  # + или =
                FAKE_RADIUS /= 1.1
                FAKE_CORDS /= 1.1
                last_zoom_time = current_time
            elif keys[pygame.K_MINUS]:  # -
                FAKE_RADIUS *= 1.1
                FAKE_CORDS *= 1.1
                last_zoom_time = current_time

        # Обработка удержания клавиш перемещения
        if current_time - last_move_time > move_interval:
            move_speed = 10  # скорость перемещения

            # Стрелка влево (1073741904)
            if keys[pygame.K_LEFT]:
                dx -= move_speed
                last_move_time = current_time
            # Стрелка вверх (1073741906)
            elif keys[pygame.K_UP]:
                dy -= move_speed
                last_move_time = current_time
            # Стрелка вниз (1073741905)
            elif keys[pygame.K_DOWN]:
                dy += move_speed
                last_move_time = current_time
            # Стрелка вправо (1073741903)
            elif keys[pygame.K_RIGHT]:
                dx += move_speed
                last_move_time = current_time

        # Физика и отрисовка
        for obj1 in SPACE_OBJECTS:
            for obj2 in SPACE_OBJECTS:
                obj1.f(obj2)

        for obj in SPACE_OBJECTS:
            x, y = obj.get_section()
            obj.move()
            if obj.get_section() == (-x, y):
                SPACE_OBJECTS.remove(obj)
                center_.r *= 1.05
                continue
            draw(screen, center_, obj)

        pygame.display.flip()

