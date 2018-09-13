#!/usr/bin/env python
import pygame
pygame.init()


DISPLAY_WIDTH = 600
DISPLAY_HEIGHT = 400


class Game(object):
    def __init__(self):
        self.display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        self.display.fill((0, 0, 0))
        self.loop()

    def loop(self):
        while True:
            for event in pygame.event.get():
                self.handle_common_keys(event)

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
