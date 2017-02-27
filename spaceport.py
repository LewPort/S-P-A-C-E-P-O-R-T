import pygame
import time
import os


pygame.init()

music = True
aspect_ratio = 1.78
display_width = 1080
display_height = int(display_width // aspect_ratio)

black = (0, 0, 0)
white = (150, 150, 150)
green = (0, 255, 0)

game_display = pygame.display.set_mode((display_width, display_height))
clock = pygame.time.Clock()

pygame.mixer.init(frequency=44100)
bwom_sound = pygame.mixer.Sound('BWOM.ogg')
rcs_sound = pygame.mixer.Sound('rcs.ogg')

class Object:

    def __init__(self, sprite, is_player, x_pos, y_pos, x_mov, y_mov, rotation_rate):
        self.player = is_player
        self.sprite = sprite
        self.object_img = pygame.image.load(self.sprite)
        self.x = x_pos
        self.y = y_pos
        self.x_movement = x_mov
        self.y_movement = y_mov
        self.rotation_rate = rotation_rate
        self.dimensions()

    def object_update(self):
        self.positional_rules()
        self.display_speed()
        self.x += self.x_movement
        self.y += self.y_movement

    def draw_object(self, x, y):
        game_display.blit(self.object_img, (x, y))

    def display_speed(self):
        font = '/Library/Fonts/Andale Mono.ttf'
        monofont = pygame.font.Font(None, 14)
        monofont_colour = (0, 255, 80)
        speed_text = ('%.1f m/s' % self.calculated_speed())
        speed_display = monofont.render(speed_text, 1, monofont_colour)
        game_display.blit(speed_display, (self.x+40, self.y-20))

    def calculated_speed(self):
        if self.y_movement < 0:
            y_speed = self.y_movement - (self.y_movement * 2)
        else:
            y_speed = self.y_movement

        if self.x_movement < 0:
            x_speed = self.x_movement - (self.x_movement * 2)
        else:
            x_speed = self.x_movement

        speed = (y_speed + x_speed) * 10

        return speed

    def key_inputs(self):
        inc = spaceship_power
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.rcs('left')
            if self.x_movement < -20:
                self.x_movement += 0
            else:
                self.x_movement += -inc

        if keys[pygame.K_RIGHT]:
            self.rcs('right')
            if self.x_movement > 20:
                self.x_movement += 0
            else:
                self.x_movement += inc

        if keys[pygame.K_UP]:
            self.rcs('fwd')
            if self.y_movement < -20:
                self.y_movement += 0
            else:
                self.y_movement += -inc

        if keys[pygame.K_DOWN]:
            self.rcs('aft')
            if self.y_movement > 20:
                self.y_movement += 0
            else:
                self.y_movement += inc

        if keys[pygame.K_z]:
            self.rcs('ccw')
            if self.y_movement > 20:
                self.y_movement += 0
            else:
                self.y_movement += inc

    def rcs(self, thrust_dir):
        object_centre = self.object_centre_coords()
        behind = (object_centre[0], object_centre[1] + 15)
        infront = (object_centre[0], object_centre[1] - 25)
        left = (object_centre[0] - 20, object_centre[1])
        right = (object_centre[0] + 15, object_centre[1])

        rcs_trigger()
        if thrust_dir == 'fwd':
            pygame.draw.rect(game_display, white, (behind[0], behind[1], 2, 7))

        if thrust_dir == 'aft':
            pygame.draw.rect(game_display, white, (infront[0], infront[1], 2, 7))

        if thrust_dir == 'left':
            pygame.draw.rect(game_display, white, (right[0], right[1], 7, 2))

        if thrust_dir == 'right':
            pygame.draw.rect(game_display, white, (left[0], left[1], 7, 2))

        if thrust_dir == 'ccw':
            pygame.draw.rect(game_display, white, (behind[0], behind[1], 7, 2))
            pygame.draw.rect(game_display, white, (infront[0], infront[1], 7, 2))
            

    def dimensions(self):
        self.obj_width, self.obj_height = self.object_img.get_size()
        return self.object_img.get_size()

    def object_centre_coords(self):
        x_centre = (self.obj_width / 2) + self.x -1
        y_centre = (self.obj_height / 2) + self.y -1
        return x_centre, y_centre

    def movement(self):
        return (round(self.x_movement, 1), round(self.y_movement, 1))

    def positional_rules(self):

        if self.player:
            if self.x > display_width:
                self.x -= display_width
                warpgate.x -= display_width
            elif self.x < -self.dimensions()[0]:
                self.x += display_width
                warpgate.x += display_width
            elif self.y > display_height:
                self.y -= display_height
                warpgate.y -= display_height
            elif self.y < -self.dimensions()[1]:
                self.y += display_height
                warpgate.y += display_height

            warpgate.draw_object(warpgate.x, warpgate.y)
            self.draw_object(self.x, self.y)



    #
    # def gravity():
    #     global y_movement
    #
    #     if y > (display_height - 40) and y_movement > -2:
    #         y_movement = 0
    #     else:
    #         y_movement += 0.1

def background():
    space_bg = pygame.image.load('spacebg.jpg')
    space_bg = pygame.transform.scale(space_bg, (display_width, display_height))
    game_display.blit(space_bg, (0, 0))

def win_message():
    winfont = pygame.font.Font(None, 150)
    winfont_colour = (255, 0, 0)
    win_text = 'D O C K E D'
    win_display = winfont.render(win_text, 1, winfont_colour)
    rcs_sound.stop()
    bwom_sound.play(0, 5000)
    bwom_sound.fadeout(5000)
    text_x_centre = win_display.get_width() / 2
    text_y_centre = win_display.get_height() / 2
    little_timer = time.time() + 5
    while little_timer > time.time():
        game_display.blit(win_display, (display_width / 2 - text_x_centre, display_height / 2 - text_y_centre))
        pygame.display.update()

def win_conditions(accuracy_margin):
    global docked
    global level
    global spaceship
    global warpgate
    win_x_range, win_y_range = round(warpgate.object_centre_coords()[0]), round(warpgate.object_centre_coords()[1])
    win_x_range = range(win_x_range - accuracy_margin, win_x_range + accuracy_margin)
    win_y_range = range(win_y_range - accuracy_margin, win_y_range + accuracy_margin)

    ship_x_coord, ship_y_coord = spaceship.object_centre_coords()

    if round(ship_x_coord) in win_x_range and round(ship_y_coord) in win_y_range and spaceship.movement() == warpgate.movement():
        docked = True
        level += 1
        return


def rcs_trigger():
    if pygame.mixer.get_busy() == False:
        rcs_sound.play(0, 0, 0)
        rcs_sound.set_volume(0.1)

def rcs_sound_stop():
    for event in pygame.event.get():
        if event.type == pygame.KEYUP:
            rcs_sound.stop()

def game_loop():
    global docked
    global playing
    global level
    global spaceship
    global warpgate

    while playing and not docked:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                level = 0
                playing = False
                docked = True
                return

        background()
        warpgate.object_update()
        spaceship.object_update()
        spaceship.key_inputs()
        pygame.display.update()
        win_conditions(5)
        rcs_sound_stop()
        clock.tick(60)

    win_message()
    return

if music == True:
    pygame.mixer.music.load('space_music.mp3')
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)


level = 1
spaceship_power = 0.01
docked = False
playing = True
def title(level):
    pygame.display.set_caption('S P A C E P O R T - L V L %d' % level)

while playing:
    if level == 1:
        title(level)
        spaceship = Object('spaceship.png', True, int(display_width * 0.50), int(display_height * 0.9), 0.0, 0.0, None)
        warpgate = Object('warpgate.png', False, 600, 300, -0.0, -0.0, None)
        game_loop()
        spaceship = None
        warpgate = None

    elif level == 2:
        title(level)
        docked = False
        spaceship = Object('spaceship.png', True, int(display_width * 0.50), int(display_height * 0.9), -0.3, -1.0, None)
        warpgate = Object('warpgate.png', False, 600, 300, -0.3, -1.0, None)
        game_loop()
        spaceship = None
        warpgate = None

    elif level == 3:
        title(level)
        docked = False
        spaceship = Object('spaceship.png', True, int(display_width * 0.50), int(display_height * 0.9), -0.7, -1.5, None)
        warpgate = Object('warpgate.png', False, 600, 300, -0.9, -0.1, None)
        game_loop()
        spaceship = None
        warpgate = None

    elif level == 4:
        title(level)
        docked=False
        spaceship = Object('spaceship.png', True, int(display_width * 0.50), int(display_height * 0.9), 1.0, -1.5, None)
        warpgate = Object('warpgate.png', False, 600, 300, -1.7, -2.1, None)
        game_loop()
        spaceship = None
        warpgate = None

    elif level == 5:
        title(level)
        docked=False
        spaceship = Object('spaceship.png', True, int(display_width * 0.50), int(display_height * 0.9), 0.0, -2.0, None)
        warpgate = Object('warpgate.png', False, 600, 300, 2.7, -3.0, None)
        game_loop()
        spaceship = None
        warpgate = None

    elif level == 6:
        title(level)
        docked=False
        spaceship = Object('spaceship.png', True, int(display_width * 0.50), int(display_height * 0.9), -3, -7.0, None)
        warpgate = Object('warpgate.png', False, 600, 300, -3, -10.0, None)
        game_loop()
        spaceship = None
        warpgate = None

    else:
        break





pygame.quit()
quit()


    
