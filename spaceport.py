import pygame
import time
import os


pygame.init()

aspect_ratio = 1.78
display_width = 1080
display_height = int(display_width // aspect_ratio)

black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)

game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('S P A C E')
clock = pygame.time.Clock()

pygame.mixer.init(frequency=44100)
bwom_sound = pygame.mixer.Sound('BWOM.ogg')
#rumble_sound = pygame.mixer.Sound('rumble.wav')

rcs_sound = pygame.mixer.Sound('rcs.ogg')

#beep_sound = pygame.mixer.Sound('beep.mp3')



def background():
    space_bg = pygame.image.load('spacebg.jpg')
    space_bg = pygame.transform.scale(space_bg, (display_width, display_height))
    game_display.blit(space_bg, (0, 0))

def win_message():
    winfont = pygame.font.Font(None, 30)
    winfont_colour = (255, 0, 0)
    win_text = ('WINNER')
    win_display = winfont.render(win_text, 1, winfont_colour)
    game_display.blit(win_display, (display_width / 2, display_height / 2))
    pygame.mixer.music.stop()
    bwom_sound.play()
    time.sleep(1)




def win_conditions(accuracy_margin):
    global complete
    global level
    global spaceship
    global warpgate
    win_x_range, win_y_range = warpgate.object_centre_coords()
    win_x_range = range(win_x_range - accuracy_margin, win_x_range + accuracy_margin)
    win_y_range = range(win_y_range - accuracy_margin, win_y_range + accuracy_margin)

    ship_x_coord, ship_y_coord = spaceship.object_centre_coords()

    if ship_x_coord in win_x_range and ship_y_coord in win_y_range and spaceship.movement() == warpgate.movement():
        win_message()
        level += 1



class Object:

    def __init__(self, sprite, is_player, x_pos, y_pos, x_mov, y_mov):
        self.player = is_player
        self.sprite = sprite
        self.object_img = pygame.image.load(self.sprite)
        self.x = x_pos
        self.y = y_pos
        self.x_movement = x_mov
        self.y_movement = y_mov
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
        monofont = pygame.font.Font(None, 25)
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
        inc = 1.0
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:

            if self.x_movement < -20:
                self.x_movement += 0
            else:
                self.x_movement += -inc

        if keys[pygame.K_RIGHT]:

            if self.x_movement > 20:
                self.x_movement += 0
            else:
                self.x_movement += inc

        if keys[pygame.K_UP]:
            if self.y_movement < -20:
                self.y_movement += 0
            else:
                self.y_movement += -inc

        if keys[pygame.K_DOWN]:

            if self.y_movement > 20:
                self.y_movement += 0
            else:
                self.y_movement += inc

    def dimensions(self):
        self.obj_width, self.obj_height = self.object_img.get_size()
        return self.object_img.get_size()

    def object_centre_coords(self):
        x_centre = (self.obj_width / 2) + self.x
        y_centre = (self.obj_height / 2) + self.y
        return (round(x_centre), round(y_centre))

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




    def gravity():
        global y_movement

        if y > (display_height - 40) and y_movement > -2:
            y_movement = 0
        else:
            y_movement += 0.1

def rcs_trigger():
    for event in pygame.event.get():
        if event.type == pygame.K_DOWN:
            pass
    rcs_sound.play(100, 0, 500)
    rcs_sound.fadeout(500)





def game_loop():
    global complete
    global level
    global spaceship
    global warpgate


    while not complete:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                complete = True

        background()
        warpgate.object_update()
        spaceship.object_update()
        spaceship.key_inputs()
        pygame.display.update()
        clock.tick(60)
        win_conditions(5)


pygame.mixer.music.load('space_music.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)


level = 1
complete = False

while True:
    if level == 1:
        spaceship = Object('spaceship.png', True, int(display_width * 0.50), int(display_height * 0.9), 0.0, 0.0)
        warpgate = Object('warpgate.png', False, 600, 300, -0.0, -0.0)
        game_loop()
        spaceship = None
        warpgate = None
        level += 1



    elif level == 2:
        spaceship = Object('spaceship.png', True, int(display_width * 0.50), int(display_height * 0.9), -0.3, -1.0)
        warpgate = Object('warpgate.png', False, 600, 300, -0.3, -1.0)
        game_loop()
        spaceship = None
        warpgate = None
        level += 1

    elif level == 3:
        spaceship = Object('spaceship.png', True, int(display_width * 0.50), int(display_height * 0.9), -0.7, -1.5)
        warpgate = Object('warpgate.png', False, 600, 300, -0.5, -0.1)
        game_loop()

    elif level == 4:
        spaceship = Object('spaceship.png', True, int(display_width * 0.50), int(display_height * 0.9), 1.0, -1.5)
        warpgate = Object('warpgate.png', False, 600, 300, -0.7, -0.1)
        game_loop()





# pygame.quit()
# quit()


    
