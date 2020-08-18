import pygame
import sys
import math


def distance(point1, point2):
    point1_x = point1[0]
    point2_x = point2[0]
    point1_y = point1[1]
    point2_y = point2[1]
    return math.sqrt((point2_x - point1_x) ** 2 + (point2_y - point1_y) ** 2)


class Player:
    def __init__(self, screen, x, y):
        pass

    def draw(self):
        pass

    def putt(self):
        pass


class Disc:
    def __init__(self, screen, x, y, radius, power, height):
        self.screen = screen
        self.x = x
        self.y = y
        self.original_y = self.y
        self.radius = radius
        self.power = power
        self.height = height
        self.dy = 10
        self.dx = self.power

    def draw(self):
        pygame.draw.circle(self.screen, (0, 0, 255), (int(self.x), int(self.y)), self.radius)

    def move(self):
        if self.y < self.height:
            self.dy = 0
        if self.y > self.original_y:
            self.power = 0
            self.dy = 0
        else:
            self.dy = self.dy - .2
        self.x = self.x + self.power
        self.y = self.y - self.dy


class Basket:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.x = x
        self.y = y

    def draw(self):
        pygame.draw.line(self.screen, (255, 255, 255), (self.x, self.y), (self.x, self.y - 50), 5)
        pygame.draw.line(self.screen, (255, 255, 255), (self.x, self.y - 30), (self.x, self.y - 100), 100)

    def spit_out(self):
        pass

    def catch(self):
        font1 = pygame.font.Font(None, 50)
        message_text1 = "Good Putt!"
        message_image1 = font1.render(message_text1, True, (0, 255, 0))
        self.screen.blit(message_image1, (200, 800))


class Slider:
    def __init__(self, screen, x, y, length):
        self.screen = screen
        self.bar_x = x
        self.bar_y = y
        self.slider_x = x
        self.slider_y = y
        self.length = length

    def draw(self):
        pygame.draw.line(self.screen, (255, 255, 255), (self.bar_x, self.bar_y),
                         (self.bar_x + self.length, self.bar_y), 5)
        pygame.draw.line(self.screen, (128, 128, 128),
                         (self.slider_x, self.slider_y - 10),
                         (self.slider_x, self.slider_y + 10), 8)

    def set_power(self, disc, click_pos):
        if 25 <= click_pos[0] < 65 and 20 <= click_pos[1] <= 30:
            disc.power = 1
            self.slider_x = click_pos[0]
        if 65 <= click_pos[0] < 105 and 20 <= click_pos[1] <= 30:
            disc.power = 2
            self.slider_x = click_pos[0]
        if 105 <= click_pos[0] < 145 and 20 <= click_pos[1] <= 30:
            disc.power = 3
            self.slider_x = click_pos[0]
        if 145 <= click_pos[0] < 185 and 20 <= click_pos[1] <= 30:
            disc.power = 4
            self.slider_x = click_pos[0]
        if 185 <= click_pos[0] <= 225 and 20 <= click_pos[1] <= 30:
            disc.power = 5
            self.slider_x = click_pos[0]

    def set_height(self, disc, click_pos):
        if 25 <= click_pos[0] < 65 and 70 <= click_pos[1] <= 80:
            disc.height = 430
            self.slider_x = click_pos[0]
        if 65 <= click_pos[0] < 105 and 70 <= click_pos[1] <= 80:
            disc.height = 410
            self.slider_x = click_pos[0]
        if 105 <= click_pos[0] < 145 and 70 <= click_pos[1] <= 80:
            disc.height = 390
            self.slider_x = click_pos[0]
        if 145 <= click_pos[0] < 185 and 70 <= click_pos[1] <= 80:
            disc.height = 370
            self.slider_x = click_pos[0]
        if 185 <= click_pos[0] <= 225 and 70 <= click_pos[1] <= 80:
            disc.height = 350
            self.slider_x = click_pos[0]



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


def display_game_screen(clock, screen):
    disc = Disc(screen, 500, 450, 10, 4, 430)
    power_slider = Slider(screen, 25, 25, 200)
    height_slider = Slider(screen, 25, 75, 200)
    basket = Basket(screen, 800, 500)
    print("Game Screen")
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            pressed_keys = pygame.key.get_pressed()
            if event.type == pygame.KEYDOWN and pressed_keys[pygame.K_SPACE]:
                return
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_pos = event.pos
                button_position = distance(click_pos, (500, 50))
                if button_position <= 40:
                    return disc, power_slider, height_slider, basket
                power_slider.set_power(disc, click_pos)
                height_slider.set_height(disc, click_pos)

        screen.fill((0, 0, 0))
        pygame.draw.circle(screen, (255, 0, 0), (500, 50), 40, 40)
        font1 = pygame.font.Font(None, 30)
        message_text1 = "Throw"
        message_image1 = font1.render(message_text1, True, (255, 255, 255))
        screen.blit(message_image1, (470, 40))
        disc.draw()
        power_slider.draw()
        height_slider.draw()
        basket.draw()
        pygame.display.update()


def animation(clock, screen, disc, power_slider, height_slider, basket):
    print("animation")
    while True:
        screen.fill((0, 0, 0))
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        pygame.draw.circle(screen, (255, 0, 0), (500, 50), 40, 40)
        power_slider.draw()
        height_slider.draw()
        disc.move()
        disc.draw()
        basket.draw()
        # if 750 <= disc.x <= 800 and 470 <= disc.y <= 370:
        #     font1 = pygame.font.Font(None, 50)
        #     message_text1 = "Good Putt!"
        #     message_image1 = font1.render(message_text1, True, (0, 255, 0))
        #     screen.blit(message_image1, (200, 800))
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
    screen = pygame.display.set_mode((1000, 1000))
    pygame.display.update()

    while True:
        disc, power_slider, height_slider, basket = display_game_screen(clock, screen)
        animation(clock, screen, disc, power_slider, height_slider, basket)
        display_welcome(clock, screen)
        choose_player(clock, screen)
        display_leaderboard(clock, screen)


main()
