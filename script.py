#!/usr/bin/env python
import pygame
pygame.init()


# SETTINGS
# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 255)
BRIGHT_RED = (255, 0, 0)
BRIGHT_GREEN = (0, 255, 0)
MAROON = (128,  0,   0)
# Screen
DISPLAY_WIDTH = 600
DISPLAY_HEIGHT = 400
RATE_BLOCK_SIZE = 0.05


class Ground(object):
    def __init__(self, game):
        self.heights = [5, 5, 5, 5, 5, 4, 5, 5, 5, 7, 5, 5, 3]
        self.size = len(self.heights)

        self.ys = []
        for height in self.heights:
            self.ys.append(DISPLAY_HEIGHT - height * game.block_size)
        self.thickness = 2

    def update(self, game):
        self.ys = []
        for height in self.heights:
            self.ys.append(DISPLAY_HEIGHT - height * game.block_size)
        for i, y in enumerate(self.ys):
            x0 = i * game.block_size
            y0 = y
            x1 = (i + 1) * game.block_size
            y1 = y
            pygame.draw.line(game.display, WHITE, (x0, y0), (x1, y1),
                             self.thickness)
            if i + 1 < self.size and y != self.ys[i + 1]:
                y2 = self.ys[i + 1]
                pygame.draw.line(game.display, WHITE, (x1, y1), (x1, y2),
                                 self.thickness)


class Hero(object):
    def __init__(self, game):
        self.pos = 0
        self.x = self.pos * game.block_size
        self.y = game.ground.ys[self.pos]
        self.height = 1 * game.block_size
        self.width = 1 * game.block_size
        self.carrying_the_box = True
        self.turned = "right"

    def handle_events(self, game, event):
        old_pos = self.pos
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_RIGHT]:
                self.pos += 1
                self.turned = "right"
            if event.key in [pygame.K_LEFT]:
                self.pos -= 1
                self.turned = "left"
            if event.key in [pygame.K_UP]:
                if not self.carrying_the_box:
                    if self.turned == "right":
                        if game.ground.heights[self.pos + 1] -\
                                game.ground.heights[self.pos] == 1:
                            self.carrying_the_box = True
                            game.ground.heights[self.pos + 1] -= 1
                    if self.turned == "left":
                        if game.ground.heights[self.pos - 1] -\
                                game.ground.heights[self.pos] == 1:
                            self.carrying_the_box = True
                            game.ground.heights[self.pos - 1] -= 1

            if event.key in [pygame.K_DOWN]:
                if self.carrying_the_box:
                    if self.turned == "right":
                        game.ground.heights[self.pos + 1] += 1
                    else:
                        game.ground.heights[self.pos - 1] += 1
                    self.carrying_the_box = False
        print abs(game.ground.ys[self.pos] - game.ground.ys[old_pos]
                  ), game.ground.ys[self.pos], game.ground.ys[old_pos]
        if game.ground.heights[self.pos] - game.ground.heights[old_pos] > 1:
            self.pos = old_pos
        self.pos = max(self.pos, 0)
        print self.pos

    def update(self, game):
        self.x = self.pos * game.block_size
        self.y = game.ground.ys[self.pos]
        pygame.draw.rect(game.display, BLUE, (self.x, self.y - self.height,
                                              self.width, self.height))
        if self.carrying_the_box:
            pygame.draw.rect(game.display, WHITE,
                             (self.x, self.y - 2 * self.height,
                              self.width, self.height))


class Game(object):
    def __init__(self):
        self.cmd_key_down = False
        self.display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        self.block_size = DISPLAY_WIDTH * RATE_BLOCK_SIZE
        self.ground = Ground(self)
        self.hero = Hero(self)
        self.loop()

    def loop(self):
        while True:
            self.display.fill((0, 0, 0))
            for event in pygame.event.get():
                self.handle_common_keys(event)
                self.hero.handle_events(self, event)
            self.hero.update(self)
            self.ground.update(self)
            pygame.display.update()

    def handle_common_keys(self, event):
        if event.type == pygame.QUIT:
            self.quit()

        if event.type == pygame.KEYDOWN:
            if event.key == 310:
                self.cmd_key_down = True
            if self.cmd_key_down and event.key == pygame.K_q:
                self.quit()

        if event.type == pygame.KEYUP:
            if event.key == 310:
                self.cmd_key_down = False

    def quit(self):
        pygame.quit()
        quit()


Game()
