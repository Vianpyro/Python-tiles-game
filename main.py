import pygame as pg
import sys
from os import environ, path
from time import time
from settings import *
from sprites import *
from tilemap import *
import vianpyro_random_map_generation_v1 as vmap1


class Game:
    def __init__(self):
        pg.init()
        environ["SDL_VIDEO_CENTERED"] = '1'
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        NEW_MAP = vmap1.Map(int(GRID_WIDTH * 1.5), int(GRID_HEIGHT * 1.5), 1, 0, 4)
        NEW_MAP.save_to_file(NEW_MAP.generate_2d_noise(), True, True, 1)
        self.map = Map(path.join(game_folder, 'save.wia'))
        
    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        for row, tiles in enumerate(self.map.data):
            for column, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, column, row)
                elif tile == 'P':
                    self.player = Player(self, column, row)
        try: self.player.move(0, 0)
        except: self.player = Player(self, GRID_WIDTH // 2 - 1, GRID_HEIGHT // 2 - 1)
        self.camera = Camera(self.map.width, self.map.height)


    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            fps_time = time()  # FPS COUNT
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
            pg.display.set_caption(f'{TITLE} (FPS: {round(1.0 / (time() - fps_time))})')  # Display FPS


    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)

    def draw_grid(self):
        for x in range(0, WIDTH, TILE_SIZE):
            pg.draw.line(self.screen, LIGHT_GRAY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILE_SIZE):
            pg.draw.line(self.screen, LIGHT_GRAY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass


# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
