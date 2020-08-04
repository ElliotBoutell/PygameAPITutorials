import pygame
import sys
import math


class Player:
    def __init__(self, screen, x, y):
        pass

    def draw(self):
        pass

    def normal_putt(self):
        pass

    def jump_putt(self):
        pass

    def power(self):
        pass

    def height(self):
        pass


class Disc:
    def __init__(self, screen, x, y):
        pass

    def draw(self):
        pass

    def move(self):
        pass


class Basket:
    def __init__(self, screen, x, y):
        pass

    def draw(self):
        pass

    def spit_out(self):
        pass


class Weather:
    def __init__(self, screen, x, y):
        pass

    def draw(self):
        pass

    def wind(self):
        pass

    def rain(self):
        pass


class Tree:
    def __init__(self):
        pass

    def draw(self):
        pass


class Menu:
    def __init__(self, screen, x, y):
        pass

    def draw(self):
        pass


class End:
    def __init__(self, screen, x, y):
        pass

    def draw(self):
        pass


def display_welcome(clock, screen):
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            pressed_keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN and pressed_keys[pygame.K_SPACE]:
                return
        screen.fill((0, 0, 0))
        background = pygame.image.load("menu_screen.png")
        screen.blit(background, (0, 0))
        font1 = pygame.font.Font(None, 50)
        message_text1 = "Press Space to Continue"
        message_image1 = font1.render(message_text1, True, (255, 255, 0))
        screen.blit(message_image1, (170, 600))
        font2 = pygame.font.Font(None, 50)
        message_text2 = "Welcome to Local Legends Disc Golf"
        message_image2 = font2.render(message_text2, True, (255, 255, 0))
        screen.blit(message_image2, (50, 100))
        pygame.display.update()


def choose_player(clock, screen):
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            pressed_keys = pygame.key.get_pressed()
            if event.type == pygame.KEYDOWN and pressed_keys[pygame.K_SPACE]:
                return
        screen.fill((0, 0, 0))
        background = pygame.image.load("name_screen.png")
        screen.blit(background, (0, 0))
        font1 = pygame.font.Font(None, 50)
        message_text1 = "Type Name:"
        message_image1 = font1.render(message_text1, True, (255, 255, 0))
        screen.blit(message_image1, (25, 25))
        font2 = pygame.font.Font(None, 50)
        message_text2 = "Press Space to Continue"
        message_image2 = font2.render(message_text2, True, (255, 255, 0))
        screen.blit(message_image2, (170, 600))
        pygame.display.update()


def display_leaderboard(clock, screen):
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            pressed_keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN and pressed_keys[pygame.K_SPACE]:
                return
        screen.fill((0, 0, 0))
        background = pygame.image.load("end_screen.png")
        screen.blit(background, (0, 0))
        font1 = pygame.font.Font(None, 30)
        message_text1 = "Leaderboard"
        message_image1 = font1.render(message_text1, True, (255, 255, 0))
        screen.blit(message_image1, (25, 25))
        font2 = pygame.font.Font(None, 50)
        message_text2 = "Press Space to Restart"
        message_image2 = font2.render(message_text2, True, (255, 255, 0))
        screen.blit(message_image2, (170, 600))
        pygame.display.update()


def main():
    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.set_caption("Disc Golf Putting Game")
    screen = pygame.display.set_mode((700, 700))
    pygame.display.update()
    while True:
        display_welcome(clock, screen)
        choose_player(clock, screen)
        display_leaderboard(clock, screen)


main()
