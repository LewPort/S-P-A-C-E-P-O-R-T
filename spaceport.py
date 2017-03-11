import pygame
import time
import random


pygame.init()

music = True
pygame.mixer.music.load('space_music_2.mp3')

aspect_ratio = 1.78
display_width = 1080
display_height = int(display_width // aspect_ratio)

black = (0, 0, 0)
white = (230, 230, 255)
red = (255,50,50)
green = (0, 255, 80)
blue = (0,135,255)


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
        self.is_player = is_player
        self.x = x_pos
        self.y = y_pos
        self.x_movement = x_mov
        self.y_movement = y_mov
        self.rotation_rate = rotation_rate
        self.rotation_amount = 0
        self.dimensions()

        self.mark_centre = False
        self.original_img = self.object_img

    def rot_centre(self, image, rect, angle):
        rot_image = pygame.transform.rotozoom(image, angle, 1)
        rot_rect = rot_image.get_rect(center=rect.center)
        return rot_image, rot_rect

    def object_update(self):
        if not self.is_player:
            self.old_rect = self.original_img.get_rect(center=self.object_centre_coords())
            self.rotation_amount += self.rotation_rate
            ship_img, new_rect = self.rot_centre(self.object_img, self.old_rect, self.rotation_amount)
            game_display.blit(ship_img, new_rect)

        self.positional_rules()
        self.display_speed()
        if self.mark_centre == True:
            self.draw_centre()
        self.x += self.x_movement
        self.y += self.y_movement
        #self.rotation_amount += self.rotation_rate



    def draw_object(self, x, y):
        if self.is_player:
            game_display.blit(self.object_img, (x, y))

    def draw_centre(self):
        horizontal = (self.object_centre_coords()[0] -20, self.object_centre_coords()[1])
        vertical = (self.object_centre_coords()[0], self.object_centre_coords()[1] - 20)
        pygame.draw.rect(game_display, red, (horizontal[0], horizontal[1], 40, 2))
        pygame.draw.rect(game_display, red, (vertical[0], vertical[1], 2, 40))

    def display_speed(self):
        #font = '/Library/Fonts/Andale Mono.ttf'

        if self.is_player:
            position = (10, 40)
        else:
            position = (self.x + 40, self.y - 20)


        monofont = pygame.font.Font(None, 34)
        monofont_colour = green
        speed_text = ('%.1f m/s' % self.calculated_speed())
        speed_display = monofont.render(speed_text, True, monofont_colour)
        game_display.blit(speed_display, position)

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

        rcs_sound_trigger()
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

        #return x_centre + self.x_movement, y_centre + self.y_movement

    def movement(self):
        return (round(self.x_movement, 1), round(self.y_movement, 1))

    def positional_rules(self):

        if self.player:
            if self.x > display_width:
                self.x -= display_width
                warpgate.x -= display_width
            if self.x < -self.dimensions()[0]:
                self.x += display_width
                warpgate.x += display_width
            if self.y > display_height:
                self.y -= display_height
                warpgate.y -= display_height
            if self.y < -self.dimensions()[1]:
                self.y += display_height
                warpgate.y += display_height

        #warpgate.draw_object(warpgate.x, warpgate.y)
        self.draw_object(self.x, self.y)

        self.off_screen_hint()


    def off_screen_hint(self):
        if not self.player:
            if self.x >= display_width:
                self.draw_off_screen_hint(display_width, self.object_centre_coords()[1])
            elif self.x <= -self.dimensions()[0]:
                self.draw_off_screen_hint(0, self.object_centre_coords()[1])
            elif self.y >= display_height:
                self.draw_off_screen_hint(self.object_centre_coords()[0], display_height)
            elif self.y <= -self.dimensions()[1]:
                self.draw_off_screen_hint(self.object_centre_coords()[0], 0)

    def draw_off_screen_hint(self, x, y):
        if x >= display_width:
            x = display_width
        if x <= 0:
            x = 0
        if y >= display_height:
            y = display_height
        if y <= 0:
            y = 0

        pygame.draw.circle(game_display, blue, (int(x), int(y)), 10, 0)



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

def intro_sequence():
    rcs_sound.stop()
    bwom_sound.set_volume(0.7)
    bwom_sound.play(0,0,2000)
    bwom_sound.fadeout(4000)
    big_message('S P A C E P O R T', blue)

def win_sequence():
    rcs_sound.stop()
    bwom_sound.play(0)
    bwom_sound.fadeout(4000)
    big_message('D O C K E D', (0, 255, 0))

def fail_sequence():
    rcs_sound.stop()
    bwom_sound.play(0)
    bwom_sound.fadeout(4000)
    big_message('T I M E  E X P I R E D', (255,0,0))
    

def big_message(text, colour):
    font = pygame.font.Font(None, 150)
    display = font.render(text, True, colour)

    text_x_centre = display.get_width() / 2
    text_y_centre = display.get_height() / 2
    
    little_timer = time.time() + 4
    while little_timer > time.time():
        game_display.blit(display, (display_width / 2 - text_x_centre, display_height / 2 - text_y_centre))
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


def rcs_sound_trigger():
    if pygame.mixer.get_busy() == False:
        rcs_sound.play(0, 0, 0)
        rcs_sound.set_volume(0.1)

def countdown_timer(deadline):
    now = time.time()
    remaining = deadline - now
    return remaining
    
def display_countdown_timer(seconds_to_display, colour):
    font = '/Library/Fonts/Andale Mono.ttf'
    remaining_time = time.strftime('%M:%S', time.gmtime(seconds_to_display))
    remaining_time = 'T: %s' % remaining_time
    #remaining_time = ' '.join(remaining_time)
    font = pygame.font.Font(None, 34)
    display = font.render(remaining_time, True, colour)
    game_display.blit(display, (10,10))

def levelgen():
    #def __init__(self, sprite, is_player, x_pos, y_pos, x_mov, y_mov, rotation_rate):
    global docked
    global spaceship
    global warpgate

    rnd_x_pos = int(display_width * (round(random.uniform(0.2, 0.8), 1)))
    rnd_y_pos = int(display_height * (round(random.uniform(0.4, 0.9), 1)))
    rnd_x_spd = round(random.uniform(-7, 7), 1)
    rnd_y_spd = round(random.uniform(-7, 7), 1)
    rnd_spin = round(random.uniform(-4, 4), 1)


    rnd_x_pos_var = rnd_x_pos * round(random.uniform(0.2, 1.8), 1)
    rnd_y_pos_var = rnd_y_pos * round(random.uniform(0.2, 1.8), 1)
    rnd_x_spd_var = rnd_x_spd * round(random.uniform(0.5, 1.5), 1)
    rnd_y_spd_var = rnd_y_spd * round(random.uniform(0.5, 1.5), 1)

    level_rnd_title = str(level) + ' (RND GEN)'
    title(level_rnd_title)
    docked = False
    spaceship = Object('spaceship.png', True, rnd_x_pos_var, rnd_y_pos_var, rnd_x_spd_var, rnd_y_spd_var, rnd_spin)
    warpgate = Object('warpgate.png', False, rnd_x_pos, rnd_y_pos, rnd_x_spd, rnd_y_spd, rnd_spin)
    game_loop()
    spaceship = None
    warpgate = None


    
    


def game_loop():
    global docked
    global playing
    global level
    global spaceship
    global warpgate

    deadline = time.time() + (60 * 2.5)

    
    while playing and not docked:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYUP:
                rcs_sound.fadeout(20)

        if time.time() >= deadline:
            fail_sequence()
            return None
                
        background()
        warpgate.object_update()
        spaceship.key_inputs()
        spaceship.object_update()
        
        display_countdown_timer(countdown_timer(deadline), red)
        pygame.display.update()
        win_conditions(5)
        clock.tick(70)
                
    win_sequence()
    return None

if __name__ == '__main__':

    if music == True:
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)

    level = 1
    spaceship_power = 0.01
    docked = False
    playing = True
    def title(level):
        level = str(level)
        pygame.display.set_caption('S P A C E P O R T - L V L %s' % level)

    time.sleep(0.1)
    intro_sequence()

    while playing:
        if level == 1:
            title(level)
            spaceship = Object('spaceship.png', True, int(display_width * 0.50), int(display_height * 0.9), 0.0, 0.0, 0)
            warpgate = Object('warpgate.png', False, 600, 300, -0.0, -0.0, 0.1)
            game_loop()
            spaceship = None
            warpgate = None

        elif level == 2:
            title(level)
            docked = False
            spaceship = Object('spaceship.png', True, int(display_width * 0.50), int(display_height * 0.9), -0.3, -1.0, 0)
            warpgate = Object('warpgate.png', False, 600, 300, -0.3, -1.0, 0.5)
            game_loop()
            spaceship = None
            warpgate = None

        elif level == 3:
            title(level)
            docked = False
            spaceship = Object('spaceship.png', True, int(display_width * 0.50), int(display_height * 0.9), -0.7, -1.5, 0)
            warpgate = Object('warpgate.png', False, 600, 300, -0.9, -0.1, 0.7)
            game_loop()
            spaceship = None
            warpgate = None

        elif level == 4:
            title(level)
            docked=False
            spaceship = Object('spaceship.png', True, int(display_width * 0.50), int(display_height * 0.9), 1.0, -1.5, 0)
            warpgate = Object('warpgate.png', False, 600, 300, -1.7, -2.1, 1)
            game_loop()
            spaceship = None
            warpgate = None

        elif level == 5:
            title(level)
            docked=False
            spaceship = Object('spaceship.png', True, int(display_width * 0.50), int(display_height * 0.9), 0.0, -2.0, 0)
            warpgate = Object('warpgate.png', False, 600, 300, 2.7, -3.0, 1.2)
            game_loop()
            spaceship = None
            warpgate = None

        elif level == 6:
            title(level)
            docked=False
            spaceship = Object('spaceship.png', True, int(display_width * 0.50), int(display_height * 0.9), -3, -7.0, 0)
            warpgate = Object('warpgate.png', False, 600, 300, -3, -10.0, 1.5)
            game_loop()
            spaceship = None
            warpgate = None

        elif level >= 7:
            levelgen()

        else:
            break

    pygame.quit()
    quit()


    
