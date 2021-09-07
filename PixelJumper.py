import pygame
from random import *
pygame.init()
pygame.mixer.init()

win = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
screen_width, screen_height = win.get_size()
pygame.display.set_caption("Pixel Jumper")

bg = pygame.image.load("images\\stonebrickbackground.png").convert()
bg_width, bg_height = bg.get_rect().size
bg_offset_x_count = (screen_width // bg_width) + 2
bg_offset_y_count = (screen_height // bg_height) + 2
platform_image = pygame.image.load("images\\copper.png").convert()
platform_image_width, platform_image_height = platform_image.get_rect().size
gem_image = pygame.image.load("images\\diamond.png")
splash_image = pygame.image.load("images\\splash.png")
splash_width, splash_height = splash_image.get_rect().size
pixel_jumper_image = pygame.image.load("images\\pixel_jumper.png")
pixel_jumper_width, pixel_jumper_height = pixel_jumper_image.get_rect().size
shop_image = pygame.image.load("images\\shop_unselected.png")
shop_image_width, shop_image_height = shop_image.get_rect().size
ui_font = pygame.font.SysFont('arial', 15)
menu_font = pygame.font.Font('font\\riffic-bold.ttf', 22)

sound_big_upgrade = pygame.mixer.Sound('sounds\\big_upgrade.wav')
sound_click_menu = pygame.mixer.Sound('sounds\\click_menu.wav')
sound_collect_gem = pygame.mixer.Sound('sounds\\collect_gem.wav')
sound_hit_head = pygame.mixer.Sound('sounds\\hit_head.wav')
sound_hover_menu = pygame.mixer.Sound('sounds\\hover_menu.wav')
sound_jump = pygame.mixer.Sound('sounds\\jump.wav')
sound_land = pygame.mixer.Sound('sounds\\land.wav')
sound_land_hard = pygame.mixer.Sound('sounds\\land_hard.wav')
sound_small_upgrade = pygame.mixer.Sound('sounds\\small_upgrade.wav')
sound_start_game = pygame.mixer.Sound('sounds\\start_game.wav')

clock = pygame.time.Clock()

PLAYER_WIDTH = 36
PLAYER_HEIGHT = 77
GRAVITY = 2
PLATFORM_HEIGHT = 32
GEM_WIDTH = 26
GEM_HEIGHT = 22
FRAMERATE = 25
STATE_SPLASH = 0
STATE_PLAY = 1
STATE_MAIN_MENU = 2
STATE_CREDITS = 3
STATE_PAUSE_MENU = 4
STATE_SHOP_MENU = 5 
STATE_HELP = 6

standing_image = pygame.image.load("images\\standing.png")
jumping_image = pygame.image.load("images\\Jumping.png")
jumping_left_image = pygame.image.load("images\\JumpingLeft.png")
jumping_right_image = pygame.image.load("images\\JumpingRight.png")

walk_left_images = [pygame.image.load('images\\walkingLeftFrame1.png'), pygame.image.load('images\\walkingLeftFrame2.png'), pygame.image.load('images\\walkingLeftFrame3.png'), pygame.image.load('images\\walkingLeftFrame4.png'), pygame.image.load('images\\walkingLeftFrame5.png'), pygame.image.load('images\\walkingLeftFrame6.png'), pygame.image.load('images\\walkingLeftFrame7.png'), pygame.image.load('images\\walkingLeftFrame8.png'), pygame.image.load('images\\walkingLeftFrame9.png'), pygame.image.load('images\\walkingLeftFrame10.png'), pygame.image.load('images\\walkingLeftFrame11.png'), pygame.image.load('images\\walkingLeftFrame12.png')]
walk_right_images = [pygame.image.load('images\\walkingrightframe1.png'), pygame.image.load('images\\walkingrightframe2.png'), pygame.image.load('images\\walkingrightframe3.png'), pygame.image.load('images\\walkingrightframe4.png'), pygame.image.load('images\\walkingrightframe5.png'), pygame.image.load('images\\walkingrightframe6.png'), pygame.image.load('images\\walkingrightframe7.png'), pygame.image.load('images\\walkingrightframe8.png'), pygame.image.load('images\\walkingrightframe9.png'), pygame.image.load('images\\walkingrightframe10.png'), pygame.image.load('images\\walkingrightframe11.png'), pygame.image.load('images\\walkingrightframe12.png')]

walk_frame_delay = 0
walk_frame_delay_max = 1
walk_frame_index = 0

scroll_x_limit_left = screen_width // 4
scroll_x_limit_right = scroll_x_limit_left * 3
scroll_y_limit = screen_height // 2

delta_x = 4
delta_y = 3

space_pressed = False

class player(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.speed = 5
        self.y_vel = 0
        self.jump_power = -30
        self.is_standing = True
        self.is_moving_left = False
        self.is_moving_right = False
        self.double_jumped = False

    def move(self):
        global level_reached
        global level_last, last_level_index
        global gem_count
        diff_x = 0
        diff_y = 0
        self.is_moving_left = False
        self.is_moving_right = False        
        landed = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            diff_x -= self.speed
            self.is_moving_left = True
        elif keys[pygame.K_d]:
            diff_x += self.speed
            self.is_moving_right = True

            
        diff_y += self.y_vel
        self.y_vel += GRAVITY

        if self.y + diff_y > screen_height - PLAYER_HEIGHT:
            diff_y = screen_height - PLAYER_HEIGHT - self.y
            self.is_standing = True
            self.y_vel = 0
            level_last = 0
            last_level_index = -1
            if diff_y > 60:
                sound_land_hard.play()
            elif diff_y > 10:
                sound_land.play()            
        for the_platform in platforms:
            collided_x = the_platform.rect.colliderect(pygame.Rect((self.x + diff_x, self.y), (PLAYER_WIDTH, PLAYER_HEIGHT)))
            collided_y = the_platform.rect.colliderect(pygame.Rect((self.x, self.y + diff_y), (PLAYER_WIDTH, PLAYER_HEIGHT)))

            if collided_x:
                if the_platform.vel == 0:
                    if diff_x  > 0:
                        diff_x = the_platform.x - PLAYER_WIDTH - self.x
                    elif diff_x  < 0:
                        diff_x = the_platform.x + the_platform.width - self.x
                else:
                    if (self.x < (the_platform.x + (the_platform.width // 2))):
                        diff_x = the_platform.x - PLAYER_WIDTH - self.x
                    else:
                        diff_x = the_platform.x + the_platform.width - self.x

            elif collided_y:
                if diff_y > 0:
                    if diff_y > 60:
                        sound_land_hard.play()
                    elif diff_y > 10:
                        sound_land.play()
                    diff_y = the_platform.y - PLAYER_HEIGHT - self.y
                    self.is_standing = True
                    self.y_vel = 0
                    level_last = the_platform.level
                    last_level_index = platforms.index(the_platform)
                    landed = True
                    if the_platform.level > level_reached:
                        level_reached = the_platform.level

                elif diff_y < 0:
                    diff_y = the_platform.y + the_platform.height - self.y
                    self.y_vel = 0
                    sound_hit_head.play()

        if (diff_y > 0) and not landed:
          self.is_standing = False
        
        if self.is_standing:
            self.double_jumped = False
            if space_pressed:
                self.y_vel = self.jump_power
                self.is_standing = False
                sound_jump.play()
        elif (space_pressed) and (not self.double_jumped) and (purchased_double_jump):
            self.y_vel = self.jump_power
            self.double_jumped = True
            sound_jump.play()

        if self.is_standing and (platforms[last_level_index].vel != 0) and purchased_sticky_boots:
            diff_x += platforms[last_level_index].last_vel

        if diff_y > 100:
            diff_y = 100

        self.x += diff_x
        self.y += diff_y

        for the_gem in gems:
            if the_gem.active:
                collided = the_gem.rect.colliderect(pygame.Rect((self.x, self.y), (PLAYER_WIDTH, PLAYER_HEIGHT)))
                if collided:
                    gem_count += 1
                    the_gem.reset()
                    sound_collect_gem.play()
            



class platform(object):
    def __init__(self,x,y,width,vel,min_x,max_x,level):
        self.x = x
        self.y = y
        self.width = int((width//platform_image_width) * platform_image_width)
        self.height = PLATFORM_HEIGHT
        self.vel = vel
        self.last_vel = vel
        self.min_x = min_x
        self.max_x = max_x
        self.level = level
        self.rect = pygame.Rect((x, y), (self.width, PLATFORM_HEIGHT))
    def draw(self, win):
        draw_y = self.y + world_offset_y
        if (draw_y + PLATFORM_HEIGHT >= 0) and (draw_y <= screen_height):
            for image_offset in range(self.width//platform_image_width):
                win.blit(platform_image, (self.x + world_offset_x + (image_offset * platform_image_width), draw_y))
    def move(self):
        self.last_vel = self.vel
        if self.vel != 0:
            self.x += self.vel
            self.rect = pygame.Rect((self.x, self.y), (self.width, self.height))
            if self.x >= self.max_x: 
                self.vel *= -1
            elif self.x <= self.min_x:
                self.vel *= -1

class gem(object):
    def __init__(self):
        self.reset()
    def draw(self, win):
        if self.active:
            win.blit(gem_image, (self.x + world_offset_x, self.y + world_offset_y)) 
    def update(self):
        if self.active:
            self.active_counter -= 1
            if self.active_counter < 1:
                self.reset()
        else:
            self.inactive_counter -= 1
            if self.inactive_counter < 1:
                self.active = True

    def reset(self):
        self.inactive_counter = randint(2, 6) * FRAMERATE
        self.active_counter = randint(5, 25) * FRAMERATE
        self.active = False
        random_index = randint(0, len(platforms)-1)
        while platforms[random_index].vel != 0:
            random_index = randint(0, len(platforms)-1)
        self.y = platforms[random_index].y - GEM_HEIGHT
        self.x = randint(platforms[random_index].x, platforms[random_index].x + platforms[random_index].width - GEM_WIDTH)        
        self.rect = pygame.Rect((self.x, self.y), (GEM_WIDTH, GEM_HEIGHT))

class button():
    def __init__(self,x,y,normal_image_file,hover_image_file):
        self.normal_image = pygame.image.load(normal_image_file)
        self.hover_image = pygame.image.load(hover_image_file)
        self.width, self.height = self.normal_image.get_rect().size
        self.x = x - (self.width // 2)
        self.y = y
        self.was_over = False

    def draw(self,win,mouse_x,mouse_y):
        if self.is_over((mouse_x, mouse_y)):
            win.blit(self.hover_image, (self.x, self.y))
        else:
            win.blit(self.normal_image, (self.x, self.y))

    def is_over(self,pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                if not self.was_over:
                    sound_hover_menu.play()
                self.was_over = True
                return True
        self.was_over = False
        return False



run = True

button_start_game = button(screen_width // 2, (screen_height // 2) - 100, "images\\Start_game_unselected.png", "images\\Start_game_selected.png") 
button_help = button(screen_width // 2, (screen_height // 2) - 0, "images\\Help_unselected.png", "images\\Help_selected.png") 
button_quit_game = button(screen_width // 2, (screen_height // 2) + 100, "images\\Quit_game_unselected.png", "images\\Quit_game_selected.png") 
button_help_back = button(screen_width // 2, (screen_height // 2) + 270, "images\\Back_unselected.png", "images\\Back_selected.png")
button_credits_exit = button(screen_width // 2, (screen_height // 2) + 270, "images\\ExitToMenu_unselected.png", "images\\ExitToMenu_selected.png")

button_resume_game = button(screen_width // 2, (screen_height // 2) - 100, "images\\Resumegame_unselected.png", "images\\Resumegame_selected.png")
button_shop = button(screen_width // 2, (screen_height // 2) - 0, "images\\Shop_unselected.png", "images\\Shop_selected.png")
button_restart_game = button(screen_width // 2, (screen_height // 2) + 100, "images\\RestartGame_unselected.png", "images\\RestartGame_selected.png")
button_exit_game = button(screen_width // 2, (screen_height // 2) + 200, "images\\ExitToMenu_unselected.png", "images\\ExitToMenu_selected.png")

button_buy_speed = button(screen_width // 2 + 80, (screen_height // 2) - 200, "images\\Buy_unselected.png", "images\\Buy_selected.png")
button_buy_jump_boost = button(screen_width // 2 + 80, (screen_height // 2) - 120, "images\\Buy_unselected.png", "images\\Buy_selected.png")
button_buy_double_jump = button(screen_width // 2 + 80, (screen_height // 2) - 40, "images\\Buy_unselected.png", "images\\Buy_selected.png")
button_buy_sticky_boots = button(screen_width // 2 + 80, (screen_height // 2) + 40, "images\\Buy_unselected.png", "images\\Buy_selected.png")
button_shop_back = button(screen_width // 2, (screen_height // 2) + 270, "images\\Back_unselected.png", "images\\Back_selected.png")



def reset_game():
    global bg_offset_x, bg_offset_y, world_offset_x, world_offset_y, level_reached, level_last
    global gem_count, pixelnate159, platforms, gems, start_x, start_y, purchased_double_jump
    global purchased_sticky_boots, last_level_index
    bg_offset_x = 0
    bg_offset_y = 0
    world_offset_x = 0
    world_offset_y = 0
    level_reached = 0
    level_last = 0
    last_level_index = 0
    gem_count = 0
    purchased_double_jump = False
    purchased_sticky_boots = False


    start_x = (screen_width // 2) - (PLAYER_WIDTH // 2)
    start_y = screen_height - PLAYER_HEIGHT
    pixelnate159 = player(start_x, start_y)

    zone_width = 400
    mid_zone_x = (screen_width // 2) - (zone_width // 2)
    left_zone_x = mid_zone_x - zone_width - PLAYER_WIDTH
    right_zone_x = mid_zone_x + zone_width + PLAYER_WIDTH
    level_height = 150
    level_y = screen_height - level_height


    platforms = []
    for level in range(200):
        if level <= 50:
            rand_min = 20
            rand_max = 50
        elif level <= 100:
            rand_min = 15
            rand_max = 40
        elif level <= 150:
            rand_min = 10
            rand_max = 30
        else:
            rand_min = 5
            rand_max = 20

        #Mid Zone
        width_percent = randint(rand_min, rand_max)
        platform_width = zone_width * (width_percent / 100)
        platform_width = int((platform_width//platform_image_width) * platform_image_width)
        platform_max_x = zone_width - platform_width
        platform_x = randint(mid_zone_x, mid_zone_x + platform_max_x)
        platform_vel = 0
        if randint(1, 10) == 1:
            platform_vel = randint(3, 8)
        if randint(1, 2) == 1:
            platform_vel * -1
        platforms.append(platform(platform_x, level_y, platform_width, platform_vel, mid_zone_x, mid_zone_x + platform_max_x, level + 1))

        #Left Zone
        width_percent = randint(rand_min, rand_max)
        platform_width = zone_width * (width_percent / 100)
        platform_width = int((platform_width//platform_image_width) * platform_image_width)
        platform_max_x = zone_width - platform_width
        platform_x = randint(left_zone_x, left_zone_x + platform_max_x)
        platform_vel = 0
        if randint(1, 10) == 1:
            platform_vel = randint(3, 8)
        if randint(1, 2) == 1:
            platform_vel * -1
        platforms.append(platform(platform_x, level_y, platform_width, platform_vel, left_zone_x, left_zone_x + platform_max_x, level + 1))

        #Right Zone
        width_percent = randint(rand_min, rand_max)
        platform_width = zone_width * (width_percent / 100)
        platform_width = int((platform_width//platform_image_width) * platform_image_width)
        platform_max_x = zone_width - platform_width
        platform_x = randint(right_zone_x, right_zone_x + platform_max_x)
        platform_vel = 0
        if randint(1, 10) == 1:
            platform_vel = randint(3, 8)
        if randint(1, 2) == 1:
            platform_vel * -1
        platforms.append(platform(platform_x, level_y, platform_width, platform_vel ,right_zone_x, right_zone_x + platform_max_x, level + 1))

        mid_zone_x -= delta_x
        left_zone_x -= delta_x * 3
        right_zone_x += delta_x * 3
        zone_width += delta_x * 2
        level_height += delta_y
        level_y -= level_height

    gems = []
    for level in range(100):
        gems.append(gem())






def draw_game():
    global walk_frame_index
    global walk_frame_delay
    win.fill((0,0,0))
    for bg_offset_x_loop in range(bg_offset_x_count):
        for bg_offset_y_loop in range(bg_offset_y_count):
            win.blit(bg, (bg_offset_x + (bg_offset_x_loop * bg_width),bg_offset_y + (bg_offset_y_loop * bg_height)))
    if pixelnate159.is_standing:
        walk_frame_delay = (walk_frame_delay + 1) % walk_frame_delay_max
        if walk_frame_delay == 0:
            walk_frame_index = (walk_frame_index + 1) % 12
        if pixelnate159.is_moving_right:
            win.blit(walk_right_images[walk_frame_index], (pixelnate159.x + world_offset_x - 8, pixelnate159.y + world_offset_y))
        elif pixelnate159.is_moving_left:
            win.blit(walk_left_images[walk_frame_index], (pixelnate159.x + world_offset_x - 8, pixelnate159.y + world_offset_y))
        else:
            win.blit(standing_image, (pixelnate159.x + world_offset_x - 8, pixelnate159.y + world_offset_y))
    else:
        if pixelnate159.is_moving_left:
            win.blit(jumping_left_image, (pixelnate159.x + world_offset_x - 8, pixelnate159.y + world_offset_y))
        elif pixelnate159.is_moving_right:
            win.blit(jumping_right_image, (pixelnate159.x + world_offset_x - 8, pixelnate159.y + world_offset_y))
        else:
            win.blit(jumping_image, (pixelnate159.x + world_offset_x - 8, pixelnate159.y + world_offset_y))
        
    
    for the_platform in platforms:
        the_platform.draw(win)
    
    for the_gem in gems:
        the_gem.draw(win)
    

    stats_left = screen_width - 120
    stats_height = 200
    surf = pygame.Surface((screen_width - stats_left, stats_height))
    surf.set_alpha(128)
    surf.fill((0,0,0))
    win.blit(surf, (stats_left - 10, 10))
    val_x = int(pixelnate159.x - start_x)
    val_y = int((pixelnate159.y - start_y) * -1)
    txt = ui_font.render(f"x: {val_x}", True, (255,255,255))
    win.blit(txt, (stats_left, 20))
    txt = ui_font.render(f"y: {val_y}", True, (255,255,255))
    win.blit(txt, (stats_left, 40))
    txt = ui_font.render(f"speed: {pixelnate159.speed}", True, (255,255,255))
    win.blit(txt, (stats_left, 60))
    txt = ui_font.render(f"jump power: {pixelnate159.jump_power * -1}", True, (255,255,255))
    win.blit(txt, (stats_left, 80))
    txt = ui_font.render(f"max level: {level_reached}", True, (255,255,255))
    win.blit(txt, (stats_left, 100))
    txt = ui_font.render(f"last level: {level_last}", True, (255,255,255))
    win.blit(txt, (stats_left, 120))
    txt = ui_font.render(f"gems: {gem_count}", True, (255,255,255))
    win.blit(txt, (stats_left, 140))
    if purchased_double_jump:
        txt = ui_font.render(f"double jump: Yes", True, (255,255,255))
    else:
        txt = ui_font.render(f"double jump: No", True, (255,255,255))
    win.blit(txt, (stats_left, 160))
    if purchased_sticky_boots:
        txt = ui_font.render(f"sticky boots: Yes", True, (255,255,255))
    else:
        txt = ui_font.render(f"sticky boots: No", True, (255,255,255))
    win.blit(txt, (stats_left, 180))
    
    

game_state = STATE_SPLASH


pygame.mixer.music.load("music\\Bensound_Creativemind_Intro.mp3")
pygame.mixer.music.play(-1)

while run:
    clock.tick(FRAMERATE)

    if game_state == STATE_SPLASH:
        #splash
        win.blit(splash_image, (screen_width // 2 - splash_width // 2, screen_height // 2 - splash_height // 2))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                game_state = STATE_MAIN_MENU
                sound_click_menu.play()

    elif game_state == STATE_MAIN_MENU:
        pos = pygame.mouse.get_pos()
        win.fill((0,0,0))
        button_start_game.draw(win,pos[0],pos[1])
        win.blit(pixel_jumper_image, ((screen_width // 2) - (pixel_jumper_width // 2), (screen_height // 2) - 350))        
        button_help.draw(win,pos[0],pos[1])
        button_quit_game.draw(win,pos[0],pos[1])
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_start_game.is_over(pos):
                    game_state = STATE_PLAY
                    reset_game()
                    pygame.mixer.music.load("music\\bensound-epic.mp3")
                    pygame.mixer.music.play(-1)
                    sound_start_game.play()
                elif button_quit_game.is_over(pos):
                    run = False
                    sound_click_menu.play()
                elif button_help.is_over(pos):
                    game_state = STATE_HELP
                    sound_click_menu.play()

    elif game_state == STATE_HELP:
        pos = pygame.mouse.get_pos()        
        win.fill((0,0,0))
        win.blit(pixel_jumper_image, ((screen_width // 2) - (pixel_jumper_width // 2), (screen_height // 2) - 350))
        txt = menu_font.render(f"Press 'a' to move left" , True, (255,255,255))
        win.blit(txt, ((screen_width // 2) - (txt.get_width() // 2), (screen_height // 2) - 150))
        txt = menu_font.render(f"Press 'd' to move right" , True, (255,255,255))
        win.blit(txt, ((screen_width // 2) - (txt.get_width() // 2), (screen_height // 2) - 100))
        txt = menu_font.render(f"Press 'spacebar' jump" , True, (255,255,255))
        win.blit(txt, ((screen_width // 2) - (txt.get_width() // 2), (screen_height // 2) - 50))
        txt = menu_font.render(f"Press 'esc' to open the menu" , True, (255,255,255))
        win.blit(txt, ((screen_width // 2) - (txt.get_width() // 2), (screen_height // 2) + 0))
        txt = menu_font.render(f"You can buy upgrades from the shop" , True, (255,255,255))
        win.blit(txt, ((screen_width // 2) - (txt.get_width() // 2), (screen_height // 2) + 50))
        txt = menu_font.render(f"To access the shop you need to open the pause menu" , True, (255,255,255))
        win.blit(txt, ((screen_width // 2) - (txt.get_width() // 2), (screen_height // 2) + 100))        
        txt = menu_font.render(f"The aim is to reach the 200th level" , True, (255,255,255))
        win.blit(txt, ((screen_width // 2) - (txt.get_width() // 2), (screen_height // 2) + 150))
        button_help_back.draw(win,pos[0],pos[1])
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_help_back.is_over(pos):
                    game_state = STATE_MAIN_MENU
                    sound_click_menu.play()
        

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            game_state = STATE_MAIN_MENU           

    elif game_state == STATE_CREDITS:
        pos = pygame.mouse.get_pos()        
        win.fill((0,0,0))
        win.blit(pixel_jumper_image, ((screen_width // 2) - (pixel_jumper_width // 2), (screen_height // 2) - 350))
        txt = menu_font.render(f"Congrats, you have completed" , True, (255,255,255))
        win.blit(txt, ((screen_width // 2) - (txt.get_width() // 2), (screen_height // 2) - 175))
        txt = menu_font.render(f"Pixel Jumper" , True, (255,255,255))
        win.blit(txt, ((screen_width // 2) - (txt.get_width() // 2), (screen_height // 2) - 125))
        txt = menu_font.render(f"#technosupport" , True, (255,255,255))
        win.blit(txt, ((screen_width // 2) - (txt.get_width() // 2), (screen_height // 2) - 75))
        txt = menu_font.render(f"This game was made by:" , True, (255,255,255))
        win.blit(txt, ((screen_width // 2) - (txt.get_width() // 2), (screen_height // 2) - 25))
        txt = menu_font.render(f"PixelNate159" , True, (255,255,255))
        win.blit(txt, ((screen_width // 2) - (txt.get_width() // 2), (screen_height // 2) + 25))
        txt = menu_font.render(f"and" , True, (255,255,255))
        win.blit(txt, ((screen_width // 2) - (txt.get_width() // 2), (screen_height // 2) + 75))        
        txt = menu_font.render(f"PixelMad147" , True, (255,255,255))
        win.blit(txt, ((screen_width // 2) - (txt.get_width() // 2), (screen_height // 2) + 125))
        txt = menu_font.render(f"Music by BenSound (bensound.com/royalty-free-music)" , True, (255,255,255))
        win.blit(txt, ((screen_width // 2) - (txt.get_width() // 2), (screen_height // 2) + 175))
        button_credits_exit.draw(win,pos[0],pos[1])
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_credits_exit.is_over(pos):
                    game_state = STATE_MAIN_MENU
                    pygame.mixer.music.load("music\\Bensound_Creativemind_Intro.mp3")
                    pygame.mixer.music.play(-1)
                    sound_click_menu.play()
        

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            game_state = STATE_MAIN_MENU    
            pygame.mixer.music.load("music\\Bensound_Creativemind_Intro.mp3")
            pygame.mixer.music.play(-1)       

    elif game_state == STATE_PAUSE_MENU:
        pos = pygame.mouse.get_pos()
        draw_game()
        surf = pygame.Surface((screen_width, screen_height))
        surf.set_alpha(100)
        surf.fill((0,0,0))
        win.blit(surf, (0, 0))        
        win.blit(pixel_jumper_image, ((screen_width // 2) - (pixel_jumper_width // 2), (screen_height // 2) - 350))
        button_resume_game.draw(win,pos[0],pos[1])
        button_shop.draw(win,pos[0],pos[1])
        button_restart_game.draw(win,pos[0],pos[1])
        button_exit_game.draw(win,pos[0],pos[1])
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                game_state = STATE_PLAY  
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_resume_game.is_over(pos):
                    game_state = STATE_PLAY
                    sound_click_menu.play()
                elif button_shop.is_over(pos):
                    game_state = STATE_SHOP_MENU
                    sound_click_menu.play()
                elif button_restart_game.is_over(pos):
                    game_state = STATE_PLAY
                    reset_game()
                    sound_click_menu.play()
                elif button_exit_game.is_over(pos):
                    game_state = STATE_MAIN_MENU
                    pygame.mixer.music.load("music\\Bensound_Creativemind_Intro.mp3")
                    pygame.mixer.music.play(-1)
                    sound_click_menu.play()

    elif game_state == STATE_SHOP_MENU:
        pos = pygame.mouse.get_pos()
        draw_game()
        surf = pygame.Surface((screen_width, screen_height))
        surf.set_alpha(100)
        surf.fill((0,0,0))
        win.blit(surf, (0, 0))        
        win.blit(shop_image, ((screen_width // 2) - (shop_image_width // 2), (screen_height // 2) - 350))
        button_shop_back.draw(win,pos[0],pos[1])

        button_buy_speed.draw(win,pos[0],pos[1])
        txt = menu_font.render(f"+1 speed   2x" , True, (255,255,255))
        win.blit(txt, ((screen_width // 2) - (txt.get_width()) - 20, (screen_height // 2) - 170))
        win.blit(gem_image, ((screen_width // 2) - 18, (screen_height // 2) - 166))
        button_buy_jump_boost.draw(win,pos[0],pos[1])
        txt = menu_font.render(f"+2 jump   3x" , True, (255,255,255))
        win.blit(txt, ((screen_width // 2) - (txt.get_width()) - 20, (screen_height // 2) - 90))
        win.blit(gem_image, ((screen_width // 2) - 18, (screen_height // 2) - 86))
        if not purchased_double_jump:
            button_buy_double_jump.draw(win,pos[0],pos[1])
            txt = menu_font.render(f"Double jump   20x" , True, (255,255,255))
            win.blit(txt, ((screen_width // 2) - (txt.get_width()) - 20, (screen_height // 2) - 10))
            win.blit(gem_image, ((screen_width // 2) - 18, (screen_height // 2) - 6))
        else:
            txt = menu_font.render(f"Double jump purchased" , True, (255,255,255))
            win.blit(txt, ((screen_width // 2) - (txt.get_width()) - 20, (screen_height // 2) - 10))

        if not purchased_sticky_boots:
            button_buy_sticky_boots.draw(win,pos[0],pos[1])
            txt = menu_font.render(f"Sticky boots   20x" , True, (255,255,255))
            win.blit(txt, ((screen_width // 2) - (txt.get_width()) - 20, (screen_height // 2) + 70))
            win.blit(gem_image, ((screen_width // 2) - 18, (screen_height // 2) + 76))
        else:
            txt = menu_font.render(f"Sticky Boots purchased" , True, (255,255,255))
            win.blit(txt, ((screen_width // 2) - (txt.get_width()) - 20, (screen_height // 2) + 70))
                   
        txt = menu_font.render(f"Balance: {gem_count}" , True, (255,255,255))
        win.blit(txt, ((screen_width // 2) - (txt.get_width()) - 20, (screen_height // 2) + 150))
        win.blit(gem_image, ((screen_width // 2) - 18, (screen_height // 2) + 156))
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                game_state = STATE_PAUSE_MENU  

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_shop_back.is_over(pos):
                    game_state = STATE_PAUSE_MENU
                    sound_click_menu.play()
                elif button_buy_speed.is_over(pos):
                    if gem_count >= 2:
                        pixelnate159.speed += 1
                        gem_count -= 2
                        sound_small_upgrade.play()
                elif button_buy_jump_boost.is_over(pos):
                    if gem_count >= 3:
                        pixelnate159.jump_power -= 2
                        gem_count -= 3
                        sound_small_upgrade.play()
                elif (not purchased_double_jump) and button_buy_double_jump.is_over(pos):
                    if gem_count >= 20:
                        purchased_double_jump = True
                        gem_count -= 20
                        sound_big_upgrade.play()
                elif (not purchased_sticky_boots) and button_buy_sticky_boots.is_over(pos):
                    if gem_count >= 20:
                        purchased_sticky_boots = True
                        gem_count -= 20
                        sound_big_upgrade.play()
   
    elif game_state == STATE_PLAY:
        space_pressed = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                game_state = STATE_PAUSE_MENU
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                space_pressed = True

        if pixelnate159.x < scroll_x_limit_left:
            world_offset_x = scroll_x_limit_left - pixelnate159.x
        elif pixelnate159.x + PLAYER_WIDTH > scroll_x_limit_right:
            world_offset_x = scroll_x_limit_right - (pixelnate159.x + PLAYER_WIDTH)
        else:
            world_offset_x = 0

        bg_offset_x = world_offset_x

        if bg_offset_x + bg_width < 0:
            while bg_offset_x + bg_width < 0:
                bg_offset_x += bg_width
        elif bg_offset_x > 0:
            while bg_offset_x > 0:
                bg_offset_x -= bg_width

        if pixelnate159.y < scroll_y_limit:
            world_offset_y = scroll_y_limit - pixelnate159.y
        else:
            world_offset_y = 0
        

        bg_offset_y = world_offset_y

        if bg_offset_y + bg_height < 0:
            while bg_offset_y + bg_height < 0:
                bg_offset_y += bg_height
        elif bg_offset_y > 0:
            while bg_offset_y > 0:
                bg_offset_y -= bg_height

        for the_platform in platforms:
            the_platform.move()
        pixelnate159.move()
        for the_gem in  gems:
            the_gem.update()

        draw_game()
        pygame.display.update()

        if level_last == 200:
            game_state = STATE_CREDITS
            pygame.mixer.music.load("music\\bensound-dubstep.mp3")
            pygame.mixer.music.play(-1)


pygame.quit()