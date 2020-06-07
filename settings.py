import pygame as pg
pg.init()

# Define some colors (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
DARK_GRAY = (50, 50, 50)
LIGHT_GRAY = (150, 150, 150)

# Game window settings
infoObject = pg.display.Info()
WIDTH, HEIGHT= int(infoObject.current_w // 1.5), int(infoObject.current_h // 1.5)
FPS = 60
TITLE = 'Tile game'
BGCOLOR = DARK_GRAY

# Game settings
TILE_SIZE = WIDTH // 64
GRID_WIDTH = WIDTH / TILE_SIZE
GRID_HEIGHT = HEIGHT / TILE_SIZE
