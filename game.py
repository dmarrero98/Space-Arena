import pygame
from menus import *
from timeit import timeit
import random

class Asteroid:
    def __init__(self):
        self.asteroids = [(pygame.transform.scale(pygame.image.load(f"rock{i}.png"), (75, 85))) for i in range(0,4)]
        self.asteroid_y = -100
        self.dictionary = {}
        self.hitboxes = []

    
    def load_asteroids(self):
        obj_y = self.asteroid_y
        for i in range(0, 4):
            self.dictionary[i] = [random.randint(100, 700), obj_y]

    def draw(self, window, idx):
        x = self.dictionary[idx][0]
        y = self.dictionary[idx][1]
        hitbox = (x+11, y+7, 60, 65)
        self.dictionary[idx].append(pygame.draw.rect(window, (225,225,225), hitbox, 1))
        pygame.draw.rect(window, (225,225,225), hitbox, 1) 
        window.blit(self.asteroids[idx], (x, y))
        

class Player:
    def __init__(self):
        self.avatar = pygame.transform.scale(pygame.image.load("spaceship.png"), (55,55))
        self.avatar_x = 400
        self.avatar_y = 600 - self.avatar.get_width()
        self.hitbox = None
        self.avatar_limitx = self.avatar.get_width()*2, 800-self.avatar.get_width()*3
        self.avatar_limity = 600-self.avatar.get_height()-225, 650-self.avatar.get_height()
    
    def draw(self, screen):
        hitbox = (self.avatar_x+3, self.avatar_y, 50, 54)
        self.hitbox = pygame.draw.rect(screen, (225,225,225), hitbox, 1)
        self.hitbox
        screen.blit(self.avatar, (self.avatar_x, self.avatar_y))
    

    

class Spacearena():
    def __init__(self):
        pygame.init()
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.LEFT_KEY, self.RIGHT_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = 800, 650
        self.display = pygame.Surface((self.DISPLAY_W,self.DISPLAY_H))
        self.window = pygame.display.set_mode(((self.DISPLAY_W,self.DISPLAY_H)))
        self.window_icon = pygame.display.set_icon(pygame.image.load('spaceship.png'))
        self.background_img = "background.png"
        self.background_display = pygame.transform.scale(pygame.image.load("background.png"), (800, 600))
        self.set_window_caption = pygame.display.set_caption("Space arena")
        self.font_name = '8-BIT WONDER.TTF'
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.curr_menu = self.main_menu
        self.frames = pygame.time.Clock()
        self.current_time = 0 
        self.asteroids = Asteroid()
        self.player = Player()

        
    def game_loop(self):
        self.asteroids.load_asteroids()
        score = 0
        font = pygame.font.Font(self.font_name, 15)
        text_surface = font.render(f"Score {str(score)}", True, (225,225,225))
        text_rect = text_surface.get_rect()
        text_rect.center = (57, 635)
        while self.playing:
        
            self.check_events()
            self.window.fill((0, 0, 0))
            #player movement
            if self.RIGHT_KEY and self.player.avatar_x < self.player.avatar_limitx[1]:
                self.player.avatar_x += 5
            if self.LEFT_KEY and self.player.avatar_x > self.player.avatar_limitx[0]:
                self.player.avatar_x -= 5
            if self.UP_KEY and self.player.avatar_y > self.player.avatar_limity[0]:
                self.player.avatar_y -= 5
            if self.DOWN_KEY and self.player.avatar_y < self.player.avatar_limity[1]:
                self.player.avatar_y += 5
            #draw and blit game items
            text_surface = font.render(f"Score {str(score)}", True, (225,225,225))
            self.window.blit(text_surface, text_rect)
            self.window.blit(self.background_display, (0,0))
            self.player.draw(self.window)
            self.asteroids.draw(self.window, 0)
            #check player collision

            if self.asteroids.dictionary[0][1] < 675:
                self.asteroids.dictionary[0][1] += 6
            if self.asteroids.dictionary[0][1] >= 675:
                self.asteroids.dictionary[0][1] = -100
                self.asteroids.dictionary[0][0] = random.randint(100, 700)
                score += 1
            projectile1 = self.asteroids.asteroids[0].get_rect(center=(self.asteroids.dictionary[0][1], self.asteroids.dictionary[0][0]))
            if pygame.Rect.colliderect(self.player.hitbox, projectile1):
                break

            if self.current_time > 3000:
                self.asteroids.draw(self.window, 1)
                if self.asteroids.dictionary[1][1] < 675:
                    self.asteroids.dictionary[1][1] += 7
                if self.asteroids.dictionary[1][1] >= 675:
                    self.asteroids.dictionary[1][1] = -100
                    self.asteroids.dictionary[1][0] = random.randint(100, 700)
                    score += 1

            if self.current_time > 7000:
                self.asteroids.draw(self.window, 2)
                if self.asteroids.dictionary[2][1] < 675:
                    self.asteroids.dictionary[2][1] += 8
                if self.asteroids.dictionary[2][1] >= 675:
                    self.asteroids.dictionary[2][1] = -100
                    self.asteroids.dictionary[2][0] = random.randint(100, 700)
                    score += 1

            if self.current_time > 10000:
                self.asteroids.draw(self.window, 3)
                if self.asteroids.dictionary[3][1] < 675:
                    self.asteroids.dictionary[3][1] += 9
                if self.asteroids.dictionary[3][1] >= 675:
                    self.asteroids.dictionary[3][1] = -100
                    self.asteroids.dictionary[3][0] = random.randint(100, 700)
                    score += 1
            

            self.current_time = pygame.time.get_ticks()            
            pygame.display.flip()
            self.frames.tick(60)
            

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
                if event.key == pygame.K_LEFT:
                    self.LEFT_KEY = True
                if event.key == pygame.K_RIGHT:
                    self.RIGHT_KEY = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.LEFT_KEY = False
                if event.key == pygame.K_RIGHT:
                    self.RIGHT_KEY = False
                if event.key == pygame.K_UP:
                    self.UP_KEY = False
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = False
                if event.key == pygame.K_RETURN:
                    self.START_KEY = False
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = False

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

    def draw_text(self, text, size, x, y ):
        font = pygame.font.Font(self.font_name,size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface,text_rect)
    
g = Spacearena()

while g.running:
    g.curr_menu.display_menu()
    g.game_loop()