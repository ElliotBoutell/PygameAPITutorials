import pygame
import sys
import math
import random


def distance(point1, point2):
    point1_x = point1[0]
    point2_x = point2[0]
    point1_y = point1[1]
    point2_y = point2[1]
    return math.sqrt((point2_x - point1_x) ** 2 + (point2_y - point1_y) ** 2)


class Message:

    def __init__(self, screen, x, y, size, color, message_text):
        self.screen = screen
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.message_text = message_text

    def draw(self):
        font = pygame.font.Font(None, self.size)
        message_image1 = font.render(self.message_text, True, self.color)
        self.screen.blit(message_image1, (self.x, self.y))


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
        self.is_caught_by_basket = False
        self.is_caught_by_tree = False

    def draw(self):
        pygame.draw.circle(self.screen, (0, 0, 255), (int(self.x), int(self.y)), self.radius)

    def move(self):
        if self.is_caught_by_basket:
            return
        if self.is_caught_by_tree:
            return
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
        pygame.draw.rect(self.screen, (255, 255, 255), (self.x - 50, self.y - 150, 100, 100))

    def catch(self, disc, scoreboard):
        hit_box = pygame.Rect(self.x - 50, self.y - 150, 100, 100)
        if hit_box.collidepoint(int(disc.x), int(disc.y)):
            disc.x = self.x
            disc.y = self.y - 70
            disc.dy = 0
            disc.dx = 0
            disc.is_caught_by_basket = True



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
            disc.power = 2
            self.slider_x = click_pos[0]
        if 65 <= click_pos[0] < 105 and 20 <= click_pos[1] <= 30:
            disc.power = 4
            self.slider_x = click_pos[0]
        if 105 <= click_pos[0] < 145 and 20 <= click_pos[1] <= 30:
            disc.power = 6
            self.slider_x = click_pos[0]
        if 145 <= click_pos[0] < 185 and 20 <= click_pos[1] <= 30:
            disc.power = 8
            self.slider_x = click_pos[0]
        if 185 <= click_pos[0] <= 225 and 20 <= click_pos[1] <= 30:
            disc.power = 10
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


class Wind:
    def __init__(self, screen):
        self.screen = screen
        self.speed = random.randrange(-5, 6)

    def draw(self):
        font1 = pygame.font.Font(None, 30)
        message_text1 = "Wind Speed: " + str(self.speed)
        message_image1 = font1.render(message_text1, True, (255, 255, 255))
        self.screen.blit(message_image1, (800, 100))

    def blow(self, disc):
        disc.power = disc.power + self.speed
        disc.height = disc.height - self.speed


class Tree:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.x = x
        self.y = y
        self.height = 500 - self.y

    def draw(self):
        pygame.draw.line(self.screen, (210, 105, 30), (self.x, self.y), (self.x, self.y + self.height), 10)

    def catch(self, disc):
        # pygame.draw.rect(self.screen, (255, 255, 255), (self.x, self.y, 50, 200))
        hit_box = pygame.Rect(self.x, self.y, 10, self.height)
        if hit_box.collidepoint(int(disc.x), int(disc.y)):
            disc.x = self.x - 10
            disc.y = 490
            disc.dy = 0
            disc.dx = 0
            disc.is_caught_by_tree = True


class Scoreboard:

    def __init__(self, screen):
        self.screen = screen
        self.score = 0
        self.font = pygame.font.Font(None, 30)
        self.ready_to_update = True


    def draw(self):
        score_string = "Score:" + str(self.score)
        score_image = self.font.render(score_string, True, (255, 255, 255))
        self.screen.blit(score_image, (5, 100))

    def update(self, amount_to_change):
        if self.ready_to_update:
            self.score = self.score + amount_to_change
            self.ready_to_update = False

    def make_ready(self):
        self.ready_to_update = True


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
        space_continue = Message(screen, 170, 400, 50, (255, 255, 0), "Press Space to Continue")
        space_continue.draw()
        welcome = Message(screen, 50, 100, 50, (255, 255, 0), "Welcome to Local Legends Disc Golf")
        welcome.draw()
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
        screen.blit(message_image2, (170, 400))
        pygame.display.update()


def display_game_screen(clock, screen, scoreboard):
    disc = Disc(screen, 500, 450, 10, 4, 430)
    power_slider = Slider(screen, 25, 25, 200)
    height_slider = Slider(screen, 25, 75, 200)
    basket = Basket(screen, 800, 500)
    wind = Wind(screen)
    tree_y = random.randrange(350, 450)
    tree = Tree(screen, 650, tree_y)

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
                    return disc, power_slider, height_slider, basket, wind, tree
                power_slider.set_power(disc, click_pos)
                height_slider.set_height(disc, click_pos)
                wind.blow(disc)

        screen.fill((0, 0, 0))
        pygame.draw.circle(screen, (255, 0, 0), (500, 50), 40, 40)
        throw = Message(screen, 470, 40, 30, (255, 255, 255), "Throw")
        throw.draw()
        power = Message(screen, 250, 25, 20, (255, 255, 255), "Power")
        power.draw()
        height = Message(screen, 250, 75, 20, (255, 255, 255), "Height")
        height.draw()
        disc.draw()
        power_slider.draw()
        height_slider.draw()
        basket.draw()
        wind.draw()
        tree.draw()
        scoreboard.draw()
        pygame.display.update()


def animation(clock, screen, disc, power_slider, height_slider, basket, wind, tree, scoreboard):
    scoreboard.make_ready()
    while True:
        screen.fill((0, 0, 0))
        clock.tick(60)
        for event in pygame.event.get():
            pressed_keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN and pressed_keys[pygame.K_SPACE]:
                return
        pygame.draw.circle(screen, (255, 0, 0), (500, 50), 40, 40)
        throw = Message(screen, 470, 40, 30, (255, 255, 255), "Throw")
        throw.draw()
        power_slider.draw()
        height_slider.draw()
        power = Message(screen, 250, 25, 20, (255, 255, 255), "Power")
        power.draw()
        height = Message(screen, 250, 75, 20, (255, 255, 255), "Height")
        height.draw()
        basket.draw()
        scoreboard.draw()
        wind.draw()
        disc.move()
        disc.draw()
        tree.draw()
        tree.catch(disc)
        basket.catch(disc, scoreboard)
        if disc.is_caught_by_basket:
            good_putt = Message(screen, 800, 200, 50, (0, 255, 0 ), "Good Putt!")
            good_putt.draw()
            space_continue = Message(screen, 170, 400, 50, (255, 255, 0), "Press Space to Continue")
            space_continue.draw()
            scoreboard.update(100)
        if disc.is_caught_by_tree:
            too_bad = Message(screen, 800, 200, 50, (255, 0, 0), "Too Bad!")
            too_bad.draw()
            space_continue = Message(screen, 170, 400, 50, (255, 255, 0), "Press Space to Continue")
            space_continue.draw()
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
        screen.blit(message_image2, (170, 400))
        pygame.display.update()


def instruction_screen(clock, screen):
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            pressed_keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN and pressed_keys[pygame.K_SPACE]:
                return
        screen.fill((0, 0, 0))
        welcome = Message(screen, 180, 30, 50, (255, 255, 0), "Welcome to Local Legends Disc Golf")
        welcome.draw()
        font = pygame.font.Font(None, 30)
        text = "The objective of this game is to land the disc inside the basket on each putt." \
               " Each Putt is worth 100 points." \
               " To throw the disc, set the power and height bars and hit the red button." \
               " The wind will effect your power and height depending on which way it is blowing:" \
               " Headwinds (negative numbers) will lift the disc and take away power." \
               " Tailwinds (positive numbers) will drop your disc and add power." \
               " Watch out for trees as well as they will block your disc" \
               " But most importantly, Have Fun!"
        drawText(screen, text, (255, 255, 255), (100, 75, 800, 500), font)
        space_continue = Message(screen, 170, 400, 50, (255, 255, 0), "Press Space to Continue")
        space_continue.draw()
        pygame.display.update()


def drawText(surface, text, color, rect, font, aa=False, bkg=None):
    # I got from: https://www.pygame.org/wiki/TextWrap#:~:text=Simple%20Text%20Wrapping%20for%20pygame.&text=Simple%20function%20that%20will%20draw,make%20the%20line%20closer%20together.
    # draw some text into an area of a surface
    # automatically wraps words
    # returns any text that didn't get blitted
    rect = pygame.Rect(rect)
    y = rect.top
    lineSpacing = -2

    # get the height of the font
    fontHeight = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word
        if i < len(text):
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]

    return text


def main():
    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.set_caption("Disc Golf Putting Game")
    screen = pygame.display.set_mode((1000, 500))
    scoreboard = Scoreboard(screen)
    pygame.display.update()

    while True:
        display_welcome(clock, screen)
        instruction_screen(clock, screen)
        choose_player(clock, screen)
        for k in range(3):
            disc, power_slider, height_slider, basket, wind, tree = display_game_screen(clock, screen, scoreboard)
            animation(clock, screen, disc, power_slider, height_slider, basket, wind, tree, scoreboard)
        display_leaderboard(clock, screen)


main()
