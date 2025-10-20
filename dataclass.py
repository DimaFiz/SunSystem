from dataclasses import dataclass


@dataclass
class SpaceData:
    """Planets' and satellites' parameters"""

    G = 6.67e-11
    FPS = 100
    dt = 365 * 24
    DARK_BLUE = (0, 0, 50)
    YELLOW = (220, 200, 0)
    screen_width = 1200
    screen_height = 900
    CENTER = (screen_width // 2, screen_height // 2)

    """Planets"""
    PLANETS = {
        "MERCURY": {
            "mass": 3.302e23,
            "name": "MERCURY",
            "r": 2_439_700,  # radius
            "distance": 57.9e9,
            "color": (169, 169, 169),  # grey
        },
        "VENUS": {
            "mass": 4.868e24,
            "name": "VENUS",
            "r": 6_051_800,  # radius
            "distance": 108.2e9,
            "color": (238, 203, 173),  # beige-yellow
        },
        "EARTH": {
            "mass": 5.974e24,
            "name": "EARTH",
            "r": 6_371_000,  # radius
            "distance": 149.6e9,
            "color": (0, 0, 255),  # blue
        },
        "MARS": {
            "mass": 6.419e23,
            "name": "MARS",
            "r": 3_389_500,  # radius
            "distance": 227.9e9,
            "color": (255, 0, 0),  # red
        },
        "JUPITER": {
            "mass": 1.898e27,
            "name": "JUPITER",
            "r": 69_911_000,  # radius
            "distance": 778.5e9,
            "color": (255, 165, 0),  # orange
        },
        "SATURN": {
            "mass": 5.684e26,
            "name": "SATURN",
            "r": 58_232_000,  # radius
            "distance": 1.434e12,
            "color": (210, 180, 140),  # goldish
        },
        "URANUS": {
            "mass": 8.681e25,
            "name": "URANUS",
            "r": 25_362_000,  # radius
            "distance": 2.871e12,
            "color": (173, 216, 230),  # light blue
        },
        "NEPTUNE": {
            "mass": 1.024e26,
            "name": "NEPTUNE",
            "r": 24_622_000,  # radius
            "distance": 4.495e12,
            "color": (0, 0, 139),  # dark blue
        },
    }

    """Sputniks"""
    SATELLITES = {
        "EARTH": {
            "MOON": {
                "mass": 7.347e22,
                "name": "MOON",
                "r": 1_737_400,
                "distance": 149.6e9 + 384_400_000,
                "color": (192, 192, 192),  # silver grey
            }
        },
        "MARS": {
            "PHOBOS": {
                "mass": 1.065e16,
                "name": "PHOBOS",
                "r": 11_266,
                "distance": 227.9e9 + 9_377_000,
                "color": (139, 69, 19),  # dark brown
            },
            "DEIMOS": {
                "mass": 1.476e15,
                "name": "DEIMOS",
                "r": 6_200,
                "distance": 227.9e9 + 23_460_000,
                "color": (160, 82, 45),  # brown
            },
        },
        "JUPITER": {
            "IO": {
                "mass": 8.931e22,
                "name": "IO",
                "r": 1_821_600,
                "distance": 778.5e9 + 421_700_000,
                "color": (255, 165, 0),  # orange
            },
            "EUROPA": {
                "mass": 4.799e22,
                "name": "EUROPA",
                "r": 1_560_800,
                "distance": 778.5e9 + 671_034_000,
                "color": (210, 180, 140),  # beige
            },
            "GANYMEDE": {
                "mass": 1.481e23,
                "name": "GANYMEDE",
                "r": 2_631_200,
                "distance": 778.5e9 + 1_070_412_000,
                "color": (128, 128, 128),  # grey
            },
            "CALLISTO": {
                "mass": 1.075e23,
                "name": "CALLISTO",
                "r": 2_410_300,
                "distance": 778.5e9 + 1_882_709_000,
                "color": (105, 105, 105),  # dark grey
            },
        },
        "SATURN": {
            "TITAN": {
                "mass": 1.345e23,
                "name": "TITAN",
                "r": 2_574_700,
                "distance": 1.434e12 + 1_221_870_000,
                "color": (210, 180, 140),  # goldish
            },
            "RHEA": {
                "mass": 2.306e21,
                "name": "RHEA",
                "r": 763_800,
                "distance": 1.434e12 + 527_108_000,
                "color": (169, 169, 169),  # grey
            },
            "IAPETUS": {
                "mass": 1.805e21,
                "name": "IAPETUS",
                "r": 734_500,
                "distance": 1.434e12 + 3_560_820_000,
                "color": (220, 220, 220),  # light grey
            },
        },
        "URANUS": {
            "TITANIA": {
                "mass": 3.400e21,
                "name": "TITANIA",
                "r": 788_400,
                "distance": 2.871e12 + 435_910_000,
                "color": (176, 196, 222),  # light steel
            },
            "OBERON": {
                "mass": 2.883e21,
                "name": "OBERON",
                "r": 761_400,
                "distance": 2.871e12 + 583_520_000,
                "color": (119, 136, 153),  # blue-grey
            },
        },
        "NEPTUNE": {
            "TRITON": {
                "mass": 2.138e22,
                "name": "TRITON",
                "r": 1_353_400,
                "distance": 4.495e12 + 354_759_000,
                "color": (173, 216, 230),  # light blue
            }
        },
    }

    # отношение радиуса планеты к радиусу солнца
    PLANET_TO_SUN_RADIUS_RATIO = {
        None: 1,
        "MERCURY": 2_439.7 / 696_340,
        "VENUS": 6_051.8 / 696_340,
        "EARTH": 6_371.0 / 696_340,
        "MARS": 3_389.5 / 696_340,
        "JUPITER": 69_911.0 / 696_340,
        "SATURN": 58_232.0 / 696_340,
        "URANUS": 25_362.0 / 696_340,
        "NEPTUNE": 24_622.0 / 696_340,
    }
    TRAPPIST_1 = {
        "mass": 1.77021e29,
        "name": "TRAPPIST-1",
        "r": 82864460,
        "distance": 0,
        "color": (255, 100, 0),
    }

    TRAPPIST_1_PLANETS = {
        "TRAPPIST-1B": {
            "mass": 6.075558e24,
            "name": "TRAPPIST-1B",
            "r": 6918906,
            "distance": 1662056000,
            "color": (200, 100, 50),
        },
        "TRAPPIST-1C": {
            "mass": 6.905944e24,
            "name": "TRAPPIST-1C",
            "r": 6727776,
            "distance": 2275416000,
            "color": (180, 80, 60),
        },
        "TRAPPIST-1D": {
            "mass": 1.773278e24,
            "name": "TRAPPIST-1D",
            "r": 4918412,
            "distance": 3207424000,
            "color": (160, 120, 80),
        },
        "TRAPPIST-1E": {
            "mass": 4.611928e24,
            "name": "TRAPPIST-1E",
            "r": 5848578,
            "distance": 4214232000,
            "color": (100, 150, 200),
        },
        "TRAPPIST-1F": {
            "mass": 5.577716e24,
            "name": "TRAPPIST-1F",
            "r": 6657695,
            "distance": 5550160000,
            "color": (80, 130, 180),
        },
        "TRAPPIST-1G": {
            "mass": 6.858152e24,
            "name": "TRAPPIST-1G",
            "r": 7180117,
            "distance": 6746960000,
            "color": (70, 110, 160),
        },
        "TRAPPIST-1H": {
            "mass": 1.977394e24,
            "name": "TRAPPIST-1H",
            "r": 4810105,
            "distance": 9260240000,
            "color": (200, 150, 100),
        },
    }

    TRAPPIST_1_TO_STAR_RADIUS_RATIO = {
        "TRAPPIST-1": 1.0,
        "TRAPPIST-1B": 0.0835,
        "TRAPPIST-1C": 0.0812,
        "TRAPPIST-1D": 0.0593,
        "TRAPPIST-1E": 0.0706,
        "TRAPPIST-1F": 0.0803,
        "TRAPPIST-1G": 0.0866,
        "TRAPPIST-1H": 0.0580,
    }

    TRAPPIST_1_SATELLITES = {
        "TRAPPIST-1E": {
            "LUNA_PRIMA": {
                "mass": 7.347e21,  # ~0.1 массы Луны
                "name": "LUNA_PRIMA",
                "r": 500_000,  # ~0.29 радиуса Луны
                "distance": 4214232000 + 10000000,  # 10,000 км от планеты
                "color": (150, 150, 180),  # серо-голубой
            }
        },
        "TRAPPIST-1F": {
            "AQUA_MOON": {
                "mass": 1.474e22,  # ~0.2 массы Луны
                "name": "AQUA_MOON",
                "r": 800_000,  # ~0.46 радиуса Луны
                "distance": 5550160000 + 15000000,  # 15,000 км от планеты
                "color": (100, 150, 220),  # голубой (возможные океаны)
            }
        },
        "TRAPPIST-1G": {
            "TERRA_SATELLITE": {
                "mass": 3.673e22,  # ~0.5 массы Луны
                "name": "TERRA_SATELLITE",
                "r": 1_000_000,  # ~0.58 радиуса Луны
                "distance": 6746960000 + 20000000,  # 20,000 км от планеты
                "color": (120, 100, 80),  # коричневатый
            },
            "MINOR_MOON": {
                "mass": 1.837e21,  # ~0.025 массы Луны
                "name": "MINOR_MOON",
                "r": 300_000,  # ~0.17 радиуса Луны
                "distance": 6746960000 + 50000000,  # 50,000 км от планеты
                "color": (180, 170, 160),  # светло-серый
            },
        },
        "TRAPPIST-1H": {
            "CRYSTAL_ORB": {
                "mass": 5.144e21,  # ~0.07 массы Луны
                "name": "CRYSTAL_ORB",
                "r": 450_000,  # ~0.26 радиуса Луны
                "distance": 9260240000 + 12000000,  # 12,000 км от планеты
                "color": (200, 220, 240),  # ледяной голубой
            }
        },
    }
