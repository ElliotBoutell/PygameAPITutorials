import pygame
import sys
import math
import random
text_color = (0, 0, 128)


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
        self.screen = screen
        self.x = x
        self.y = y
        self.starting_arm_position = (self.x, self.y)
        self.end_arm_position = (self.x + 5, self. y - 30)

    def draw(self):
        pygame.draw.line(self.screen, (255, 255, 255), self.starting_arm_position, (self.x - 30, self.y - 30), 3)
        pygame.draw.line(self.screen, (255, 255, 255), (self.x - 60, self.y), (self.x - 30, self.y - 30), 3)
        pygame.draw.line(self.screen, (255, 255, 255), (self.x - 30, self.y - 30), (self.x - 30, self.y + 30), 3)
        pygame.draw.line(self.screen, (255, 255, 255), (self.x, self.y + 90), (self.x - 30, self.y + 30), 3)
        pygame.draw.line(self.screen, (255, 255, 255), (self.x - 60, self.y + 90), (self.x - 30, self.y + 30), 3)
        pygame.draw.circle(self.screen, (255, 255, 255), (self.x - 30, self.y - 45), 15, 15)

    def move(self):
        self.starting_arm_position = self.end_arm_position


class Disc:
    def __init__(self, screen, x, y, radius, power, height, color):
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
        self.hits_ground = False
        self.color = color

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (int(self.x), int(self.y)), self.radius)

    def move(self):
        if self.is_caught_by_basket:
            return
        if self.is_caught_by_tree:
            return
        if self.hits_ground:
            return
        if self.y < self.height:
            self.dy = 0
        if self.y > 490:
            self.power = 0
            self.dy = 0
        if self.x > 1010:
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
        self.image = pygame.image.load("basket2.png")

    def draw(self):
        self.screen.blit(self.image, (self.x - 50, self.y - 140))

    def catch(self, disc):
        hit_box = pygame.Rect(self.x - 50, self.y - 150, 20, 100)
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
        if 25 <= click_pos[0] <= 225 and 20 <= click_pos[1] <= 30:
            x = (click_pos[0] - 5) // 20
            disc.power = 2 * x
            self.slider_x = click_pos[0]

    def set_height(self, disc, click_pos):
        if 25 <= click_pos[0] <= 225 and 70 <= click_pos[1] <= 80:
            y = (click_pos[0] - 5) // 20
            disc.height = 430 - (y * 20)
            self.slider_x = click_pos[0]


class Wind:
    def __init__(self, screen):
        self.screen = screen
        self.speed = random.randrange(-5, 6)

    def draw(self):
        wind_speed = Message(self.screen, 800, 25, 30, text_color, "Wind Speed: " + str(self.speed))
        wind_speed.draw()

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
        pygame.draw.circle(self.screen, (34, 139, 34), (self.x, self.y + 20), 25, 25)

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
        score_string = "Score: " + str(self.score)
        score_image = self.font.render(score_string, True, (0, 0, 128))
        self.screen.blit(score_image, (800, 100))

    def update(self, amount_to_change, chain_sound, applause_sound):
        if self.ready_to_update:
            self.score = self.score + amount_to_change
            chain_sound.play()
            applause_sound.play()
            self.ready_to_update = False

    def make_ready(self):
        self.ready_to_update = True


def choose_player(clock, screen):
    background = pygame.image.load("menu_screen.png")
    pygame.key.start_text_input()
    name = ""
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            pressed_keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN and pressed_keys[pygame.K_RETURN]:
                return name
            if event.type == pygame.KEYDOWN and pressed_keys[pygame.K_BACKSPACE]:
                name = name[:-1]
            if event.type == pygame.KEYDOWN:
                name = name + event.unicode
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        type_name = Message(screen, 25, 25, 50, (255, 255, 0), "Type Name:")
        type_name.draw()
        space_continue = Message(screen, 250, 400, 50, (255, 255, 0), "Press Enter to Continue")
        space_continue.draw()
        name_message = Message(screen, 320, 25, 50, (255, 255, 255), name)
        name_message.draw()

        pygame.display.update()


def display_game_screen(clock, screen, scoreboard, turn):
    background = pygame.image.load("game_background.png")
    color_list = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
    disc_color = random.randrange(0, 6)
    disc_position = random.randrange(150, 501)
    disc = Disc(screen, disc_position, 430, 10, 1, 410, color_list[disc_color])
    power_slider = Slider(screen, 25, 25, 200)
    height_slider = Slider(screen, 25, 75, 200)
    basket = Basket(screen, 800, 500)
    wind = Wind(screen)
    tree_y = random.randrange(350, 450)
    tree = Tree(screen, 650, tree_y)
    player = Player(screen, disc.x, disc.y)
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_pos = event.pos
                button_position = distance(click_pos, (500, 50))
                if button_position <= 40:
                    return disc, power_slider, height_slider, basket, wind, tree, player
                power_slider.set_power(disc, click_pos)
                height_slider.set_height(disc, click_pos)
                wind.blow(disc)

        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        pygame.draw.circle(screen, (255, 0, 0), (500, 50), 40, 40)
        throw = Message(screen, 470, 40, 30, (255, 255, 255), "Throw")
        throw.draw()
        power = Message(screen, 250, 25, 20, text_color, "Power")
        power.draw()
        height = Message(screen, 250, 75, 20, text_color, "Height")
        turn_counter = Message(screen, 800, 65, 30, text_color, "Turn: " + str(turn))
        turn_counter.draw()
        height.draw()
        disc.draw()
        power_slider.draw()
        height_slider.draw()
        basket.draw()
        wind.draw()
        tree.draw()
        scoreboard.draw()
        player.draw()
        pygame.display.update()


def animation(clock, screen, disc, power_slider, height_slider, basket, wind, tree, scoreboard, player, turn):
    scoreboard.make_ready()
    chain_sound = pygame.mixer.Sound("chains2.wav")
    applause_sound = pygame.mixer.Sound("applause.wav")
    chain_sound.set_volume(1)
    applause_sound.set_volume(.1)
    background = pygame.image.load("game_background.png")
    while True:
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
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
        power = Message(screen, 250, 25, 20, text_color, "Power")
        power.draw()
        height = Message(screen, 250, 75, 20, text_color, "Height")
        turn_counter = Message(screen, 800, 65, 30, (0, 0, 128), "Turn: " + str(turn))
        turn_counter.draw()
        height.draw()
        basket.draw()
        scoreboard.draw()
        player.draw()
        player.move()
        wind.draw()
        disc.move()
        disc.draw()
        tree.draw()
        tree.catch(disc)
        basket.catch(disc, scoreboard)
        if disc.is_caught_by_basket:
            good_putt = Message(screen, 400, 100, 50, (0, 255, 0 ), "Good Putt!")
            good_putt.draw()
            space_continue = Message(screen, 300, 200, 50, (0, 255, 0), "Press Space to Continue")
            space_continue.draw()
            scoreboard.update(100, chain_sound, applause_sound)
        if disc.is_caught_by_tree:
            too_bad = Message(screen, 400, 100, 50, (255, 0, 0), "Too Bad!")
            too_bad.draw()
            space_continue = Message(screen, 300, 200, 50, (255, 0, 0), "Press Space to Continue")
            space_continue.draw()
        if disc.y > 490 or disc.x > 1000:
            disc.hits_ground = True
            too_bad = Message(screen, 400, 100, 50, (255, 0, 0), "Too Bad!")
            too_bad.draw()
            space_continue = Message(screen, 300, 200, 50, (255, 0, 0), "Press Space to Continue")
            space_continue.draw()
        pygame.display.update()


def display_leaderboard(clock, screen, scoreboard, name):
    background = pygame.image.load("menu_screen.png")
    leaderboard = scores_file(name, scoreboard)
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            pressed_keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN and pressed_keys[pygame.K_SPACE]:
                return
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        draw_position = 125
        for k in range(len(leaderboard)):
            message = Message(screen, 25, draw_position, 25, (255, 255, 255), leaderboard[k][:-1])
            message.draw()
            draw_position = draw_position + 30
        your_score = Message(screen, 25, 25, 40, (255, 255, 255), "Your Score: " + str(scoreboard.score))
        your_score.draw()
        leaderboard_title = Message(screen, 25, 75, 40, (255, 255, 255), "Leaderboard:")
        leaderboard_title.draw()
        space_restart = Message(screen, 280, 400, 50, (255, 255, 0), "Press Space to Restart")
        space_restart.draw()
        pygame.display.update()


def scores_file(name, scoreboard):
    # got help from father
    file = open("HighScores.txt", "r")
    lines = file.readlines()
    file.close()
    did_insert = False
    for k in range(len(lines)):
        score = int(lines[k].split()[-1])
        title = lines[k].split()[:-1]
        if scoreboard.score >= score:
            lines.insert(k, name + " " + str(scoreboard.score) + "\n")
            did_insert = True
            break
    if not did_insert:
        lines.append(name + " " + str(scoreboard.score) + "\n")
    file = open("HighScores.txt", "w")
    if len(lines) >= 10:
        lines = lines[:10]
    for k in range(len(lines)):
        file.write(lines[k])
    file.close()
    return lines


def instruction_screen(clock, screen):
    background = pygame.image.load("menu_screen.png")
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            pressed_keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN and pressed_keys[pygame.K_SPACE]:
                return
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        welcome = Message(screen, 180, 30, 50, (255, 255, 0), "Welcome to Local Legends Disc Golf")
        welcome.draw()
        font = pygame.font.Font(None, 30)
        text = "The objective of this game is to land the disc inside the basket on each putt." \
               " You must enter the basket through the front. Discs coming from the top or back will not count." \
               " Each Putt is worth 100 points." \
               " To throw the disc, set the power and height bars and hit the red button." \
               " The wind will affect your power and height depending on which way it is blowing:" \
               " Headwinds (negative numbers) will lift the disc and take away power." \
               " Tailwinds (positive numbers) will drop your disc and add power." \
               " Watch out for trees as well as they will block your disc." \
               " But most importantly, have fun!"
        drawText(screen, text, (255, 255, 255), (100, 75, 800, 500), font)
        space_continue = Message(screen, 250, 400, 50, (255, 255, 0), "Press Space to Continue")
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
    pygame.mixer.music.load("The Greatest Showman Cast - The Other Side (Official Audio) (1).mp3")
    pygame.mixer.music.set_volume(.05)
    clock = pygame.time.Clock()
    pygame.display.set_caption("Local Legends Disc Golf")
    screen = pygame.display.set_mode((1000, 500))
    pygame.display.update()


    while True:
        scoreboard = Scoreboard(screen)
        pygame.mixer.music.play(1000)
        instruction_screen(clock, screen)
        name = choose_player(clock, screen)
        for k in range(3):
            turn = k + 1
            disc, power_slider, height_slider, basket, wind, tree, player = \
                display_game_screen(clock, screen, scoreboard, turn)
            animation(clock, screen, disc, power_slider, height_slider, basket, wind, tree, scoreboard, player, turn)
        display_leaderboard(clock, screen, scoreboard, name)


main()
