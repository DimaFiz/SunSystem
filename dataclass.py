from dataclasses import dataclass


@dataclass
class SpaceData:
    G = 6.67e-11
    FPS = 100
    dt = 365 * 24
    DARK_BLUE = (0, 0, 50)
    YELLOW = (220, 200, 0)
    screen_width = 1200
    screen_height = 900
    CENTER = (screen_width // 2, screen_height // 2)
    # планеты
    PLANETS = {
        "MERCURY": {
            "mass": 3.302e23,
            "name": "MERCURY",
            "r": 2_439_700,
            "distance": 57.9e9,
            "color": (169, 169, 169)  # серый
        },
        "VENUS": {
            "mass": 4.868e24,
            "name": "VENUS",
            "r": 6_051_800,
            "distance": 108.2e9,
            "color": (238, 203, 173)  # бежево-желтый
        },
        "EARTH": {
            "mass": 5.974e24,
            "name": "EARTH",
            "r": 6_371_000,
            "distance": 149.6e9,
            "color": (0, 0, 255)  # синий
        },
        "MARS": {
            "mass": 6.419e23,
            "name": "MARS",
            "r": 3_389_500,
            "distance": 227.9e9,
            "color": (255, 0, 0)  # красный
        },
        "JUPITER": {
            "mass": 1.898e27,
            "name": "JUPITER",
            "r": 69_911_000,
            "distance": 778.5e9,
            "color": (255, 165, 0)  # оранжевый
        },
        "SATURN": {
            "mass": 5.684e26,
            "name": "SATURN",
            "r": 58_232_000,
            "distance": 1.434e12,
            "color": (210, 180, 140)  # золотистый
        },
        "URANUS": {
            "mass": 8.681e25,
            "name": "URANUS",
            "r": 25_362_000,
            "distance": 2.871e12,
            "color": (173, 216, 230)  # голубой
        },
        "NEPTUNE": {
            "mass": 1.024e26,
            "name": "NEPTUNE",
            "r": 24_622_000,
            "distance": 4.495e12,
            "color": (0, 0, 139)  # темно-синий
        }
    }
    # спутники
    SATELLITES = {
        "EARTH": {
            "MOON": {
                "mass": 7.347e22,
                "name": "MOON",
                "r": 1_737_400,
                "distance": 149.6e9 + 384_400_000,
                "color": (192, 192, 192)  # серебристо-серый
            }
        },
        "MARS": {
            "PHOBOS": {
                "mass": 1.065e16,
                "name": "PHOBOS",
                "r": 11_266,
                "distance": 227.9e9 + 9_377_000,
                "color": (139, 69, 19)  # темно-коричневый
            },
            "DEIMOS": {
                "mass": 1.476e15,
                "name": "DEIMOS",
                "r": 6_200,
                "distance": 227.9e9 + 23_460_000,
                "color": (160, 82, 45)  # коричневый
            }
        },
        "JUPITER": {
            "IO": {
                "mass": 8.931e22,
                "name": "IO",
                "r": 1_821_600,
                "distance": 778.5e9 + 421_700_000,
                "color": (255, 165, 0)  # оранжевый
            },
            "EUROPA": {
                "mass": 4.799e22,
                "name": "EUROPA",
                "r": 1_560_800,
                "distance": 778.5e9 + 671_034_000,
                "color": (210, 180, 140)  # бежевый
            },
            "GANYMEDE": {
                "mass": 1.481e23,
                "name": "GANYMEDE",
                "r": 2_631_200,
                "distance": 778.5e9 + 1_070_412_000,
                "color": (128, 128, 128)  # серый
            },
            "CALLISTO": {
                "mass": 1.075e23,
                "name": "CALLISTO",
                "r": 2_410_300,
                "distance": 778.5e9 + 1_882_709_000,
                "color": (105, 105, 105)  # темно-серый
            }
        },
        "SATURN": {
            "TITAN": {
                "mass": 1.345e23,
                "name": "TITAN",
                "r": 2_574_700,
                "distance": 1.434e12 + 1_221_870_000,
                "color": (210, 180, 140)  # золотистый
            },
            "RHEA": {
                "mass": 2.306e21,
                "name": "RHEA",
                "r": 763_800,
                "distance": 1.434e12 + 527_108_000,
                "color": (169, 169, 169)  # серый
            },
            "IAPETUS": {
                "mass": 1.805e21,
                "name": "IAPETUS",
                "r": 734_500,
                "distance": 1.434e12 + 3_560_820_000,
                "color": (220, 220, 220)  # светло-серый
            }
        },
        "URANUS": {
            "TITANIA": {
                "mass": 3.400e21,
                "name": "TITANIA",
                "r": 788_400,
                "distance": 2.871e12 + 435_910_000,
                "color": (176, 196, 222)  # светло-стальной
            },
            "OBERON": {
                "mass": 2.883e21,
                "name": "OBERON",
                "r": 761_400,
                "distance": 2.871e12 + 583_520_000,
                "color": (119, 136, 153)  # серо-голубой
            }
        },
        "NEPTUNE": {
            "TRITON": {
                "mass": 2.138e22,
                "name": "TRITON",
                "r": 1_353_400,
                "distance": 4.495e12 + 354_759_000,
                "color": (173, 216, 230)  # голубой
            }
        }
    }
