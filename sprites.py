import pygame as pg
from settings import *


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.velocity_x = self.velocity_y = 0

    def get_keys(self):
        self.velocity_x = self.velocity_y = 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]: self.velocity_x = -PLAYER_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]: self.velocity_x = PLAYER_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]: self.velocity_y = -PLAYER_SPEED
        if keys[pg.K_DOWN] or keys[pg.K_s]: self.velocity_y = PLAYER_SPEED

        # Slow the diagonal movement
        if self.velocity_x != 0 and self.velocity_y != 0:
            self.velocity_x *= 0.7071 # 1/sqrt(2)
            self.velocity_y *= 0.7071 # ~

    def collide_with_walls(self, direction):
        if direction == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.velocity_x > 0: # Moving to the right
                    self.x = hits[0].rect.left - self.rect.width
                if self.velocity_x < 0: # Moving to the left
                    self.x = hits[0].rect.right
                self.velocity_x = 0
                self.rect.x = self.x
        if direction == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.velocity_y > 0: # Moving down
                    self.y = hits[0].rect.top - self.rect.height
                if self.velocity_y < 0: # Moving up
                    self.y = hits[0].rect.bottom
                self.velocity_y = 0
                self.rect.y = self.y


    def update(self):
        self.get_keys()
        self.x += self.velocity_x * self.game.dt # Make sure the player's moving at the same speed regardless of his FPS
        self.y += self.velocity_y * self.game.dt # ~
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE
