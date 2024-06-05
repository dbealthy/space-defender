from dataclasses import dataclass


def load_settings():
    return Settings()


@dataclass
class Settings:
    # screen configurations
    WIDTH = 1280
    HEIGHT = 720
    CENTER = (WIDTH // 2, HEIGHT // 2)
    CTOP = (WIDTH // 2, 0)

    SCREEN_SIZE = WIDTH, HEIGHT

    PLAYER_SIZE = (80, 75)
    STAR_RATE = 500
    METEOR_SIZE_RANGE = (25, 100)
    STAR_QUT = 20

    FPS = 60
