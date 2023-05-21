import pygame
import generate
import display
import random
import pygame
import numpy
import solve
import globals
import time
import unicodedata

class Player:
    def __init__(self, name):
        self.name = name

class InputBox:
    def __init__(self, text, x, y, width, height,digits):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color_active = pygame.Color('lightskyblue3')
        self.color_passive = pygame.Color('chartreuse4')
        self.color = self.color_passive
        self.font = pygame.font.SysFont(None, 20)
        self.active = False
        self.digits = digits
        self.notmodified = True

    def draw(self, surface):
        color = self.color_active if self.active else self.color_passive
        pygame.draw.rect(surface, color, self.rect)
        text_surf = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        # set width of textfield so that text cannot get outside of user's text input
#        self.rect.w = max(100, text_surf.get_width()+10)
        pygame.display.flip()



class InputBox_number(InputBox):
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.active = True
                self.draw(globals.screen)
            else:
                self.active = False
                self.draw(globals.screen)
        elif event.type == pygame.KEYDOWN and self.active:
            if len(event.unicode) != 1:
                a = -1
            else:
                a = unicodedata.decimal(event.unicode[0], -1)
            if event.key == pygame.K_BACKSPACE:  # Check for backspace
                # Get text input from 0 to -1, i.e., end.
                self.text = self.text[:-1]
                self.draw(globals.screen)
            elif len(self.text)<self.digits and a>=0 and a<10:
                # Append the unicode character to the text
                if self.notmodified:
                    self.notmodified = False
                    self.text = event.unicode
                else:
                    self.text += event.unicode
                self.draw(globals.screen)

class InputBox_string(InputBox):
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.active = True
                self.draw(globals.screen)
            else:
                self.active = False
                self.draw(globals.screen)
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:  # Check for backspace
                # Get text input from 0 to -1, i.e., end.
                self.text = self.text[:-1]
                self.draw(globals.screen)
            elif len(self.text)<self.digits:
                # Append the unicode character to the text
                if self.notmodified:
                    self.notmodified = False
                    self.text = event.unicode
                else:
                    self.text += event.unicode
                self.draw(globals.screen)

class Button:
    def __init__(self, text, x, y, width, height):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (50, 50, 50)
        self.hover_color = (25, 25, 25)
        self.font = pygame.font.SysFont(None, 20)
        self.clicked = False

    def draw(self, surface):
        color = self.hover_color if self.clicked else self.color
        pygame.draw.rect(surface, color, self.rect)
        text_surf = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        pygame.display.update(self.rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.clicked = True
                self.draw(globals.screen)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.clicked = False
                self.draw(globals.screen)

class GameModeButton(Button):
    def __init__(self, textarray, x, y, width, height):
        self.textarray = textarray
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (50, 50, 50)
        self.hover_color = (25, 25, 25)
        self.font = pygame.font.SysFont(None, 20)
        self.clicked = False
        self.counter = 0
        self.text=self.textarray[self.counter]
#        self.allowed_gamemodes = ['Solve the maze']
        self.allowed_gamemodes = ['Solve the maze','Time limited','Speed run']

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.clicked = True
                notfound = True
                while notfound:
                    if self.counter==len(self.textarray)-1:
                        self.counter=0
                    else:
                        self.counter = self.counter + 1
                    if self.textarray[self.counter] in self.allowed_gamemodes:
                        notfound = False
                self.text=self.textarray[self.counter]
                self.draw(globals.screen)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.clicked = False
                self.draw(globals.screen)


def button_draw(screen, buttons):
        for button in buttons:
            button.draw(screen)

def zoomlevel_diplay(screen,zoom_level):
    font = pygame.font.SysFont(None, 20)
    rect = pygame.Rect(pygame.display.Info().current_w-180, 10, 170, 30)
    pygame.draw.rect(screen, (50, 50, 50), rect)
    text_surf = font.render('Zoom level: ' + str(zoom_level), True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)

def solved_display(screen):
    font = pygame.font.SysFont(None, 20)
    rect = pygame.Rect(pygame.display.Info().current_w-180, 50, 170, 30)
    pygame.draw.rect(screen, (50, 50, 50), rect)
    text = "Maze explored: {:.2f}%"
    text_surf = font.render(text.format(globals.percentage), True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)

def solver_diplay(screen,searched_text):
    font = pygame.font.SysFont(None, 20)
    rect = pygame.Rect(pygame.display.Info().current_w-180, 90, 170, 30)
    pygame.draw.rect(screen, (50, 50, 50), rect)
    text_surf = font.render('Solver: ' + str(searched_text), True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)

def display_ingame_screen(sqmaze, screen, offset_x, offset_y, zoom, rows, cols, buttons, update, solver_text):
    display.draw(sqmaze, screen, offset_x, offset_y, zoom, rows, cols)
    button_draw(screen, buttons)
    zoomlevel_diplay(screen,zoom)
    solver_diplay(screen,solver_text)
    solved_display(screen)
    timer()
    if update == 0:
        pygame.display.flip()
    elif update == 1:
        pygame.display.update()

def display_mazecell(screen, offset_x, offset_y, zoom, i, j, sqmaze):
    color = (0, 0, 0)
    if sqmaze[i][j] == 1:
        color = globals.path          
    if sqmaze[i][j] == 2:
        color = globals.sel_path
    if sqmaze[i][j] == 3:
        color = globals.start_c
    if sqmaze[i][j] == 4:
        color = globals.end_c
    if sqmaze[i][j] == 5:
        color = globals.fin_path
    if sqmaze[i][j] == 6:
        color = globals.alg_s
    if color != (0, 0, 0):
        pygame.draw.line(screen, color,
            ((i+offset_x + globals.centre_x) *  zoom, (j+offset_y + globals.centre_y) * zoom),
            ((i+offset_x + globals.centre_x) *  zoom, (j+offset_y+1 + globals.centre_y) * zoom-1),
            zoom)
    update_rect = [pygame.Rect((i+offset_x + globals.centre_x) *  zoom-(((zoom/3)+(zoom-1)/5)-1), (j+offset_y + globals.centre_y) * zoom, zoom+((zoom/3)+(zoom-1)/5), zoom), pygame.Rect(pygame.display.Info().current_w-180, 50, 170, 30)]
    solved_display(screen)
    pygame.display.update(update_rect)  

def display_timer():
    if globals.timer_r == 1:
        globals.time = round(time.time()-globals.start_t, 3)
    update_rect = pygame.Rect(10, 10, 170, 30)
    timer()
    pygame.display.update(update_rect) 

def endgame_display(screen):
    font = pygame.font.SysFont(None, 40)
    rect = pygame.Rect(pygame.display.Info().current_w//4, pygame.display.Info().current_h//4 , pygame.display.Info().current_w//2, pygame.display.Info().current_h//4)
    pygame.draw.rect(screen, (150, 00, 00), rect)
    text_surf = font.render('Congratulation! You won!', True, (10, 10, 10))
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)
    font = pygame.font.SysFont(None, 20)
    rect = pygame.Rect(10, 10, 170, 30)
    pygame.draw.rect(screen, (50, 50, 50), rect)
    text_surf = font.render('Time: ' + str(globals.time), True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)



def endgame_display_solved(screen):
    font = pygame.font.SysFont(None, 40)
    rect = pygame.Rect(pygame.display.Info().current_w//4, pygame.display.Info().current_h//4 , pygame.display.Info().current_w//2, pygame.display.Info().current_h//4)
    pygame.draw.rect(screen, (150, 00, 00), rect)
    text_surf = font.render('Congratulation! The algorithm solved the maze!', True, (10, 10, 10))
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)
    font = pygame.font.SysFont(None, 20)
    rect = pygame.Rect(10, 10, 170, 30)
    pygame.draw.rect(screen, (50, 50, 50), rect)
    text_surf = font.render('Time: ' + str(globals.time), True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)


def reset(rows, cols, sqmaze, pathmaze, startpos):
    for i in range(2*rows+1):
        for j in range(2*cols+1):
            if sqmaze[i][j] == 2:
                sqmaze[i][j] = 1
            if sqmaze[i][j] == 5:
                sqmaze[i][j] = 1
            if sqmaze[i][j] == 6:
                sqmaze[i][j] = 1
            pathmaze[i][j] = 0
    pathmaze[1][startpos] = 1

def generate_maze(rows, cols, seed, seed_enabled):
    maze = generate.generate_maze_kruskal(rows, cols, seed, seed_enabled)
    sqmaze = generate.transform_display(rows, cols, maze, seed, seed_enabled)
    pathmaze = numpy.zeros((2*rows+1, 2*cols+1))
    something = True
    while something:
        startpos = random.randint(1, 2 * cols)
        if  sqmaze[1][startpos] == 1:
            sqmaze[1][startpos] = 3
            pathmaze[1][startpos] = 1
            something = False

    something = True
    while something:
        endpos = random.randint(1, 2 * cols)
        if  sqmaze[2 * rows - 1][endpos] == 1:
            sqmaze[2 * rows - 1][endpos] = 4
            something = False
    return sqmaze, pathmaze, startpos, endpos

def timer():
    font = pygame.font.SysFont(None, 20)
    rect = pygame.Rect(10, 10, 170, 30)
    pygame.draw.rect(globals.screen, (50, 50, 50), rect)
    text_surf = font.render('Time: ' + str(globals.time), True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=rect.center)
    globals.screen.blit(text_surf, text_rect)



def main():
    globals.global_init()
# Initialize pygame
    pygame.init()
    pygame.display.set_caption('The Wonder of Mazes')

# Define variables needed
    rows = 10
    cols = 5
    seed_enabled = False
    seed = 1683387020
    zoom = pygame.display.Info().current_h // (2 * rows + 1)
    globals.centre_y = ((pygame.display.Info().current_h // zoom // 2) - rows)
    globals.centre_x = ((pygame.display.Info().current_w // zoom // 2) - cols)
    offset_x, offset_y = 0, 0
    solver = 0
    solver_text = 'GBFS'
    globals.timer_r = 0
# Use this to set full screen
#     screen = pygame.display.set_mode((pygame.display.Info().current_w, pygame.display.Info().current_h))
#    window_width=800
#    window_height=800
    window_width=pygame.display.Info().current_w
    window_height=pygame.display.Info().current_h
    screen = pygame.display.set_mode((window_width, window_height))
    globals.screen = screen
# setting up the start screen
# main buttons
    startscreen_buttons = []
    startscreen_buttons.append(Button('Start game', (window_width-100)/2, (window_height-30)/2, 100, 30))
    startscreen_buttons.append(Button('Quit', (window_width-100)/2, (window_height-30)/2 + 40, 100, 30))    
    startscreen_buttons.append(GameModeButton(['Solve the maze','Time limited','Speed run'], pygame.display.Info().current_w-globals.setup_screen_fontsize*5, 4*(globals.setup_screen_fontsize+20)+20 , globals.setup_screen_fontsize*5-20, globals.setup_screen_fontsize+10))
    for button in startscreen_buttons:
        button.draw(screen)
# elements for basic configuration  -  might be moved to a setup screen later
    setup_screen_font_color = (220, 220, 220)
    setup_screen_bg_color = (0, 0, 0)
# plain texts
    font = pygame.font.SysFont(None, globals.setup_screen_fontsize)
    rect = pygame.Rect(pygame.display.Info().current_w-globals.setup_screen_fontsize*5, 20 , globals.setup_screen_fontsize*5-20, globals.setup_screen_fontsize+10)
    pygame.draw.rect(screen, setup_screen_bg_color, rect)
    text_surf = font.render('Maze size', True, setup_screen_font_color)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)

    font = pygame.font.SysFont(None, 20)
    rect = pygame.Rect(pygame.display.Info().current_w-globals.setup_screen_fontsize*5, 1*(globals.setup_screen_fontsize+20)+20 , globals.setup_screen_fontsize*3, globals.setup_screen_fontsize+10)
    pygame.draw.rect(screen, setup_screen_bg_color, rect)
    text_surf = font.render('Horizontal:', True, setup_screen_font_color)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)

    font = pygame.font.SysFont(None, 20)
    rect = pygame.Rect(pygame.display.Info().current_w-globals.setup_screen_fontsize*5, 2*(globals.setup_screen_fontsize+20)+20 , globals.setup_screen_fontsize*3, globals.setup_screen_fontsize+10)
    pygame.draw.rect(screen, setup_screen_bg_color, rect)
    text_surf = font.render('Vertical:', True, setup_screen_font_color)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)

    font = pygame.font.SysFont(None, globals.setup_screen_fontsize)
    rect = pygame.Rect(pygame.display.Info().current_w-globals.setup_screen_fontsize*5, 3*(globals.setup_screen_fontsize+20)+20 , globals.setup_screen_fontsize*5-20, globals.setup_screen_fontsize+10)
    pygame.draw.rect(screen, setup_screen_bg_color, rect)
    text_surf = font.render('Game mode', True, setup_screen_font_color)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)

    font = pygame.font.SysFont(None, globals.setup_screen_fontsize)
    rect = pygame.Rect(pygame.display.Info().current_w-globals.setup_screen_fontsize*5, 5*(globals.setup_screen_fontsize+20)+20 , globals.setup_screen_fontsize*5-20, globals.setup_screen_fontsize+10)
    pygame.draw.rect(screen, setup_screen_bg_color, rect)
    text_surf = font.render('Seed', True, setup_screen_font_color)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)

    font = pygame.font.SysFont(None, globals.setup_screen_fontsize)
    rect = pygame.Rect(pygame.display.Info().current_w//2-globals.setup_screen_fontsize*5, 20 , globals.setup_screen_fontsize*10, globals.setup_screen_fontsize+10)
    pygame.draw.rect(screen, setup_screen_bg_color, rect)
    text_surf = font.render('Welcome, Player!', True, setup_screen_font_color)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)

    font = pygame.font.SysFont(None, globals.setup_screen_fontsize)
    rect = pygame.Rect(pygame.display.Info().current_w//2-globals.setup_screen_fontsize*3, 1*(globals.setup_screen_fontsize+20)+20 , globals.setup_screen_fontsize*6, globals.setup_screen_fontsize+10)
    pygame.draw.rect(screen, setup_screen_bg_color, rect)
    text_surf = font.render('Enter your name!', True, setup_screen_font_color)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)

# input fields
    startscreen_inputs = []
    startscreen_inputs.append(InputBox_number(str(rows),pygame.display.Info().current_w-globals.setup_screen_fontsize*2, 1*(globals.setup_screen_fontsize+20)+20 , globals.setup_screen_fontsize*2-20, globals.setup_screen_fontsize+10,3))
    startscreen_inputs.append(InputBox_number(str(cols),pygame.display.Info().current_w-globals.setup_screen_fontsize*2, 2*(globals.setup_screen_fontsize+20)+20  , globals.setup_screen_fontsize*2-20, globals.setup_screen_fontsize+10,3))
    startscreen_inputs.append(InputBox_number('0',pygame.display.Info().current_w-globals.setup_screen_fontsize*5, 6*(globals.setup_screen_fontsize+20)+20  , globals.setup_screen_fontsize*5-20, globals.setup_screen_fontsize+10,12))
    startscreen_inputs.append(InputBox_string("Player",pygame.display.Info().current_w//2-globals.setup_screen_fontsize*3, 3*(globals.setup_screen_fontsize+20)+20  , globals.setup_screen_fontsize*6, globals.setup_screen_fontsize+10,20))
    for inputbox in startscreen_inputs:
        inputbox.draw(screen)

    pygame.display.flip()
    globals.timer_r = 0

# event loop for the start screen
    running = True
    startgame_quit = False
    pygame.key.set_repeat(200, 10)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
# game starts clicking the start button
# screen button events                    
            for button in startscreen_buttons:
                button.handle_event(event)

            if startscreen_buttons[0].clicked:
                running = False

            if startscreen_buttons[1].clicked:
                startgame_quit = True
                running = False

# screen inputbox events                    
            for inputbox in startscreen_inputs:
                inputbox.handle_event(event)

# quit if quit button clicked
    if startgame_quit:
        pygame.quit()

    rows=int(startscreen_inputs[1].text)
    cols=int(startscreen_inputs[0].text)
    seed_enabled = True
    if startscreen_inputs[2].text == '0' or startscreen_inputs[2].text == '':
        seed_enabled = False
        startscreen_inputs[2].text = '0'
    seed=int(startscreen_inputs[2].text)

#Generate maze
    sqmaze, pathmaze, startpos, endpos = generate_maze(rows, cols, seed, seed_enabled)
    for i in range(rows * 2 + 1):
        for j in range(cols * 2 + 1):
            if sqmaze[i][j] == 1:
                globals.path_nmbr = globals.path_nmbr + 1

# setting up the start ingame screen 
    ingame_button_height = 30
    buttons = []
    buttons.append(Button('Zoom In', pygame.display.Info().current_w-180, 1*(ingame_button_height + 10) + 90, 170, ingame_button_height))
    buttons.append(Button('Zoom Out',pygame.display.Info().current_w-180, 2*(ingame_button_height + 10) + 90, 170, ingame_button_height))
    buttons.append(Button('Restart',pygame.display.Info().current_w-180, 3*(ingame_button_height + 10) + 90, 170, ingame_button_height))
    buttons.append(Button('Change Solver',pygame.display.Info().current_w-180, 4*(ingame_button_height + 10) + 90, 170, ingame_button_height))    
    buttons.append(Button('Solve',pygame.display.Info().current_w-180, 5*(ingame_button_height + 10) + 90, 170, ingame_button_height))
    buttons.append(Button('Re-generate',pygame.display.Info().current_w-180, 6*(ingame_button_height + 10) + 90, 170, ingame_button_height))
    buttons.append(Button('Quit',pygame.display.Info().current_w-180, 7*(ingame_button_height + 10) + 90, 170, ingame_button_height))
#Draw maze on screen
    display_ingame_screen(sqmaze, screen, offset_x, offset_y, zoom, rows, cols, buttons, 0, solver_text)
#Handle pygame events
    running = True
    pygame.key.set_repeat(200, 10)
    while running:
        display_timer()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
# keydown events
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    offset_x -= 1
                    display_ingame_screen(sqmaze, screen, offset_x, offset_y, zoom, rows, cols, buttons, 0, solver_text)
                elif event.key == pygame.K_RIGHT:
                    offset_x += 1
                    display_ingame_screen(sqmaze, screen, offset_x, offset_y, zoom, rows, cols, buttons, 0, solver_text)
                elif event.key == pygame.K_UP:
                    offset_y -= 1
                    display_ingame_screen(sqmaze, screen, offset_x, offset_y, zoom, rows, cols, buttons, 0, solver_text)
                elif event.key == pygame.K_DOWN:
                    offset_y += 1
                    display_ingame_screen(sqmaze, screen, offset_x, offset_y, zoom, rows, cols, buttons, 0, solver_text)
                elif event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:
                    zoom += 1
                    globals.centre_y = ((pygame.display.Info().current_h / zoom / 2) - rows)
                    globals.centre_x = ((pygame.display.Info().current_w / zoom / 2) - cols)
                    display_ingame_screen(sqmaze, screen, offset_x, offset_y, zoom, rows, cols, buttons, 0, solver_text)
                elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                    zoom = max(1, zoom - 1)
                    globals.centre_y = ((pygame.display.Info().current_h / zoom / 2) - rows)
                    globals.centre_x = ((pygame.display.Info().current_w / zoom / 2) - cols)
                    display_ingame_screen(sqmaze, screen, offset_x, offset_y, zoom, rows, cols, buttons, 0, solver_text)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mazex = int((event.pos[0] + zoom / 2) // zoom - (offset_x+globals.centre_x))
                mazey = int((event.pos[1]) // zoom - (offset_y+globals.centre_y))
                if mazex > -1 and mazex < 2 * rows + 1 and mazey > -1 and mazey < 2 * cols + 1:
                    if sqmaze[mazex][mazey] == 1:
                        if globals.timer_r == 0:
                            globals.start_t = time.time()
                            globals.timer_r = 1
                        if (pathmaze[mazex - 1][mazey] + pathmaze[mazex + 1][mazey] + pathmaze[mazex][mazey - 1] + pathmaze[mazex][mazey + 1]) == 1:
                            if pathmaze[mazex - 1][mazey] > 0:
                                pathmaze[mazex - 1][mazey] = pathmaze[mazex - 1][mazey] + 1
                            if pathmaze[mazex + 1][mazey] > 0:
                                pathmaze[mazex + 1][mazey] = pathmaze[mazex + 1][mazey] + 1
                            if pathmaze[mazex][mazey - 1] > 0:
                                pathmaze[mazex][mazey - 1] = pathmaze[mazex][mazey - 1] + 1
                            if pathmaze[mazex][mazey + 1] > 0:
                                pathmaze[mazex][mazey + 1] = pathmaze[mazex][mazey + 1] + 1
                            pathmaze[mazex][mazey] = 1
                            sqmaze[mazex][mazey] = 2
                            display_ingame_screen(sqmaze, screen, offset_x, offset_y, zoom, rows, cols, buttons, 1, solver_text)
                            if sqmaze[mazex - 1][mazey] == 4 or sqmaze[mazex + 1][mazey] == 4 or sqmaze[mazex][mazey - 1] == 4 or sqmaze[mazex][mazey + 1] == 4:
                                for i in range(2*rows+1):
                                    for j in range(2*cols+1):
                                        if sqmaze[i][j] == 2:
                                            sqmaze[i][j] = 5
                                display_ingame_screen(sqmaze, screen, offset_x, offset_y, zoom, rows, cols, buttons, 1, solver_text)
                                endgame_display(screen)
                                globals.timer_r = 0
                                pygame.display.flip()
                    elif sqmaze[mazex][mazey] == 2:
                        if pathmaze[mazex][mazey] == 1:
                            if pathmaze[mazex - 1][mazey] > 0:
                                pathmaze[mazex - 1][mazey] = pathmaze[mazex - 1][mazey] - 1
                            if pathmaze[mazex + 1][mazey] > 0:
                                pathmaze[mazex + 1][mazey] = pathmaze[mazex + 1][mazey] - 1
                            if pathmaze[mazex][mazey - 1] > 0:
                                pathmaze[mazex][mazey - 1] = pathmaze[mazex][mazey - 1] - 1
                            if pathmaze[mazex][mazey + 1] > 0:
                                pathmaze[mazex][mazey + 1] = pathmaze[mazex][mazey + 1] - 1
                            pathmaze[mazex][mazey] = 0
                            sqmaze[mazex][mazey] = 1
                            globals.timer_r = 0
                            display_ingame_screen(sqmaze, screen, offset_x, offset_y, zoom, rows, cols, buttons, 1, solver_text)
# screen button events                    
            for button in buttons:
                button.handle_event(event)

            if buttons[0].clicked:
                zoom += 1
                globals.centre_y = ((pygame.display.Info().current_h / zoom / 2) - rows)
                globals.centre_x = ((pygame.display.Info().current_w / zoom / 2) - cols)
                display_ingame_screen(sqmaze, screen, offset_x, offset_y, zoom, rows, cols, buttons, 0, solver_text)
                pygame.event.clear

            if buttons[1].clicked:
                globals.centre_y = ((pygame.display.Info().current_h / zoom / 2) - rows)
                globals.centre_x = ((pygame.display.Info().current_w / zoom / 2) - cols)
                zoom = max(1, zoom - 1)
                display_ingame_screen(sqmaze, screen, offset_x, offset_y, zoom, rows, cols, buttons, 0, solver_text)
                pygame.event.clear

            if buttons[2].clicked:
                reset(rows, cols, sqmaze, pathmaze, startpos)
                display_ingame_screen(sqmaze, screen, offset_x, offset_y, zoom, rows, cols, buttons, 1, solver_text)
                pygame.event.clear

            if buttons[3].clicked:
                if solver == 0:
                    solver_text = 'A*'
                    solver = 1
                    display_ingame_screen(sqmaze, screen, offset_x, offset_y, zoom, rows, cols, buttons, 1, solver_text)
                elif solver == 1:
                    solver_text = 'DFS'
                    solver = 2
                    display_ingame_screen(sqmaze, screen, offset_x, offset_y, zoom, rows, cols, buttons, 1, solver_text)
                elif solver == 2:
                    solver_text = 'BFS'
                    solver = 3
                    display_ingame_screen(sqmaze, screen, offset_x, offset_y, zoom, rows, cols, buttons, 1, solver_text)
                elif solver == 3:
                    solver_text = 'Dijkstra'
                    solver = 4
                    display_ingame_screen(sqmaze, screen, offset_x, offset_y, zoom, rows, cols, buttons, 1, solver_text)
                elif solver == 4:
                    solver_text = 'GBFS'
                    solver = 0
                    display_ingame_screen(sqmaze, screen, offset_x, offset_y, zoom, rows, cols, buttons, 1, solver_text)
                pygame.event.clear



            if buttons[4].clicked:
                reset(rows, cols, sqmaze, pathmaze, startpos)
                globals.alg_sp = 0
                if globals.timer_r == 0:
                    globals.start_t = time.time()
                    globals.timer_r = 1
                display_ingame_screen(sqmaze, screen, offset_x, offset_y, zoom, rows, cols, buttons, 1, solver_text)
                if solver == 0:
                    solution = solve.GBFS(sqmaze, screen, offset_x, offset_y, zoom, rows, cols, buttons)
                if solver == 1:
                    solution = solve.astar(sqmaze, screen, offset_x, offset_y, zoom, rows, cols, buttons)
                if solver == 2:
                    solution = solve.dfs(sqmaze, screen, offset_x, offset_y, zoom, rows, cols, buttons)
                if solver == 3:
                    solution = solve.bfs(sqmaze, screen, offset_x, offset_y, zoom, rows, cols, buttons)
                if solver == 4:
                    solution = solve.dijkstra(sqmaze, screen, offset_x, offset_y, zoom, rows, cols, buttons)
                for so in solution:
                    sqmaze[so[0]][so[1]] = 5
                sqmaze[1][startpos] = 3
                sqmaze[2 * rows - 1][endpos] = 4
                display_ingame_screen(sqmaze, screen, offset_x, offset_y, zoom, rows, cols, buttons, 1, solver_text)
                globals.timer_r = 0
                endgame_display_solved(screen)
                pygame.display.flip()
                pygame.event.clear(pygame.MOUSEBUTTONDOWN)

            if buttons[5].clicked:
                sqmaze, pathmaze, startpos, endpos = generate_maze(rows, cols, seed, seed_enabled)
                globals.path_nmbr = 0
                for i in range(rows * 2 + 1):
                    for j in range(cols * 2 + 1):
                        if sqmaze[i][j] == 1:
                            globals.path_nmbr = globals.path_nmbr + 1
                display_ingame_screen(sqmaze, screen, offset_x, offset_y, zoom, rows, cols, buttons, 0, solver_text)
                pygame.event.clear


            if buttons[6].clicked:
                running = False


pygame.quit()

if __name__ == "__main__":
    main()
