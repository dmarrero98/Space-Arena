import pygame
import random

#initialize pygame
pygame.init()

#create a screem
screen = pygame.display.set_mode((800, 600))

#load in background
scene = pygame.image.load("background.png")
scene = pygame.transform.scale(scene, (800, 600))


#Title and icon
pygame.display.set_caption("Space arena")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

#player movement
right = False
left = False
up = False
down = False

clock = pygame.time.Clock()

#player image load and scale
playerChar = pygame.image.load("spaceship.png")
playerChar = pygame.transform.scale(playerChar, (55,55))
playerx = 400
playery = 600-playerChar.get_width()

#obstacle image load and scale
obstacles = []
for i in range(0, 4):
    obstacles.append(pygame.transform.scale(pygame.image.load(f"rock{i}.png"), (75, 85)))

class Asteroid:
    def __init__(self, list: list, x, y):
        self.list = list
        self.x = x
        self.y = y
        self.asteroid_dict = {}
        self.hitbox = (self.x, self.y, 64, 64)

    def create_hitbox(self):
        i = 0
        for item in self.list:
            self.asteroid_dict[i] = item
            i += 1
        return self.asteroid_dict
    def draw(self, screen, idx, x, y):
        self.hitbox = (x+15, y+15, 45, 55)
        pygame.draw.rect(screen, (0,0,0), self.hitbox, 1)
        screen.blit(self.asteroid_dict[idx], (x, y))
        
    def get_hitbox(self, screen, x, y):
        self.hitbox = (x+15, y+15, 45, 55)
        return pygame.draw.rect(screen, (0,0,0), self.hitbox, 1)
    
class Player:
    def __init__(self, player_image, playerx, playery):
        self.player_image = player_image
        self.playerx = playerx
        self.playery = playery
        self.hitbox = (self.playerx, self.playery, 64, 64)
    
    def draw(self, screen, x, y):
        self.hitbox = (x+3, y, 50, 54)
        pygame.draw.rect(screen, (0,0,0), self.hitbox, 1)
        screen.blit(self.player_image, (x, y))
    
    def get_hitbox(self, screen, x, y):
        self.hitbox = (x+3, y, 50, 54)
        return pygame.draw.rect(screen, (0,0,0), self.hitbox, 1)

def background(file_name):
    scene = pygame.image.load(file_name)
    scene = pygame.transform.scale(scene, (800, 600))
    screen.blit(scene, (0,0))


#out of bounds limit for player
x_limit = 0, 800-playerChar.get_width()
y_limit = 0, 600-playerChar.get_height()-250

#x,y coordinates of obstacles
y = 0
y1 = -20
x = random.randint(0, 600)
x1 = random.randint(0, 600)
#initialize asteroid class
asteroids = Asteroid(obstacles, x, y)
#get object dict
callable_dict = asteroids.create_hitbox()
#index of obstacles list
z = 0
z1 = 1


#init player
player = Player(playerChar, playerx, playery)
#velocity of asteroids
velocity = 0
#game running loop
game_running = True
obj_counter = 0


while game_running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                left = True
            if event.key == pygame.K_RIGHT:
                right = True
            if event.key == pygame.K_UP:
                up = True
            if event.key == pygame.K_DOWN:
                down = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                left = False
            if event.key == pygame.K_RIGHT:
                right = False
            if event.key == pygame.K_UP:
                up = False
            if event.key == pygame.K_DOWN:
                down = False

        if event.type == pygame.QUIT:
            exit()

    if right and playerx < x_limit[1]:
        playerx += 6
    if left and playerx > x_limit[0]:
        playerx -= 6
    if up and playery > y_limit[1]:
        playery -= 6
    if down and playery < 600-playerChar.get_height():
        playery += 6


    screen.fill((0, 0, 0))
    if pygame.Rect.colliderect(player.get_hitbox(screen, playerx, playery), asteroids.get_hitbox(screen, x, y)):
        print("HIT")
        break
    if pygame.Rect.colliderect(player.get_hitbox(screen, playerx, playery), asteroids.get_hitbox(screen, x1, y1)):
        print("HIT")
        break
    
    screen.blit(scene, (0,0))
    asteroids.draw(screen, z1, x1, y1)
    asteroids.draw(screen, z, x, y)
    player.draw(screen, playerx, playery)
        
    if y > 600:
        y = -100
        if y == -100:
            x = random.randint(0, 600)
        if z <= len(obstacles)-1:
            z += 1
        if z > len(obstacles)-1:
            z = 0
    
    if y1 > 600:
        y1 = -100
        if y1 == -100:
            x1 = random.randint(0, 600)
        z1 = random.randint(0,3)

    y1 += 6
    y += 5
    pygame.display.flip()
    clock.tick(60)