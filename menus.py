import pygame
class Menus:
    def __init__(self):
        self.running = True
        self.DOWN_KEY, self.START_KEY = False, False
        self.DISPLAY_W, self.DISPLAY_H = 500, 300
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode(((self.DISPLAY_W,self.DISPLAY_H)))
        self.font_name = "8-BIT WONDER.TTF"
        self.BLACK, self.WHITE = (0,0,0), (255,255,255)
    
    def get_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.K_RETURN:
                    self.running = False
                    
    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
    
    def draw_menu(self, text, x, y, size):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)

            
#menu class init
main_menu = Menus()
blinker = 0
main_menu.running = False
while main_menu.running:
    blinker += 1
    main_menu.display.fill(main_menu.BLACK)
    main_menu.get_input()
    main_menu.draw_menu("Welcome to Space Arena", 250, 105, 20)
    if blinker < 200:
        main_menu.draw_menu("Press enter to start", 250, 185, 15)
    if blinker > 400:
        blinker = 0
    main_menu.window.blit(main_menu.display, (0,0))
    pygame.display.update()