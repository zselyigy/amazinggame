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
try:
   import cPickle as pickle
except:
   import pickle

class gameConfig():
    def __init__(self):
        try:
            self.load()
        except:
            self.last_player = 'Player'
            self.last_rows = 10
            self.last_cols = 5

    def save(self):
        file = open('game.cfg','wb')
        file.write(pickle.dumps(self.__dict__))
        file.close()

    def load(self):
        file = open('game.cfg','rb')
        dataPickle = file.read()
        file.close()
        self.__dict__ = pickle.loads(dataPickle)

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
        self.fontsize = 20
        self.font = pygame.font.SysFont(None, self.fontsize)
        self.active = False
        self.digits = digits
        self.notmodified = True

    def draw(self):
        color = self.color_active if self.active else self.color_passive
        display.textDisplay(self.text, self.fontsize, self.rect, color, (255, 255, 255))

class InputBox_number(InputBox):
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.active = True
                self.draw()
            else:
                self.active = False
                self.draw()
        elif event.type == pygame.KEYDOWN and self.active:
            if len(event.unicode) != 1:
                a = -1
            else:
                a = unicodedata.decimal(event.unicode[0], -1)
            if event.key == pygame.K_BACKSPACE:  # Check for backspace
                # Get text input from 0 to -1, i.e., end.
                self.text = self.text[:-1]
                self.draw()
            elif len(self.text)<self.digits and a>=0 and a<10:
                # Append the unicode character to the text
                if self.notmodified:
                    self.notmodified = False
                    self.text = event.unicode
                else:
                    self.text += event.unicode
                self.draw()

class InputBox_string(InputBox):
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.active = True
                self.draw()
            else:
                self.active = False
                self.draw()
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:  # Check for backspace
                # Get text input from 0 to -1, i.e., end.
                self.text = self.text[:-1]
                if len(self.text)==0:
                    self.text = 'Player'
                    self.notmodified = True
                self.StartScreen_Refresh()
                self.draw()
            elif len(self.text)<self.digits:
                # Append the unicode character to the text
                if self.notmodified:
                    self.notmodified = False
                    self.text = event.unicode
                    self.StartScreen_Refresh()
                else:
                    self.text += event.unicode
                    self.StartScreen_Refresh()
                self.draw()

    def StartScreen_Refresh(self):
        pass

class InputBox_Playername(InputBox_string):
    def __init__(self, text, x, y, width, height,digits, MyPlayer):
        super().__init__(text, x, y, width, height,digits)
        self.Player = MyPlayer
        self.startscreen_display()

    def startscreen_display(self):
        display.textDisplay('Welcome, '+self.Player.name+'!', globals.setup_screen_fontsize, pygame.Rect(pygame.display.Info().current_w//2-globals.setup_screen_fontsize*5, 20 , globals.setup_screen_fontsize*10, globals.setup_screen_fontsize+10), globals.setup_screen_bg_color, globals.setup_screen_font_color)

    def StartScreen_Refresh(self):
        self.Player.name = self.text
        self.startscreen_display()
        pygame.display.flip()

class baseButton:
    def __init__(self, text, x, y, width, height):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (50, 50, 50)
        self.hover_color = (25, 25, 25)
        self.fontsize = 20
        self.font = pygame.font.SysFont(None, self.fontsize)
        self.clicked = False

    def draw(self):
        color = self.hover_color if self.clicked else self.color
        display.textDisplay(self.text, self.fontsize, self.rect, color, (255, 255, 255))


class Button(baseButton):
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.clicked = True
                self.draw()
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.clicked = False
                self.draw()

class GameModeButton(baseButton):
    def __init__(self, textarray, x, y, width, height):
        self.textarray = textarray
        self.counter = 0
        self.text=self.textarray[self.counter]
        super().__init__(self.text, x, y, width, height)
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
                self.draw()
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.clicked = False
                self.draw()


def button_draw(buttons):
        for button in buttons:
            button.draw()

def zoomlevel_diplay(zoom_level):
    font = pygame.font.SysFont(None, 20)
    rect = pygame.Rect(pygame.display.Info().current_w-180, 10, 170, 30)
    pygame.draw.rect(globals.screen, (50, 50, 50), rect)
    text_surf = font.render('Zoom level: ' + str(zoom_level), True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=rect.center)
    globals.screen.blit(text_surf, text_rect)

def solved_display():
    font = pygame.font.SysFont(None, 20)
    rect = pygame.Rect(pygame.display.Info().current_w-180, 50, 170, 30)
    pygame.draw.rect(globals.screen, (50, 50, 50), rect)
    text = "Maze explored: {:.2f}%"
    text_surf = font.render(text.format(globals.percentage), True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=rect.center)
    globals.screen.blit(text_surf, text_rect)

def solver_diplay(searched_text):
    font = pygame.font.SysFont(None, 20)
    rect = pygame.Rect(pygame.display.Info().current_w-180, 90, 170, 30)
    pygame.draw.rect(globals.screen, (50, 50, 50), rect)
    text_surf = font.render('Solver: ' + str(searched_text), True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=rect.center)
    globals.screen.blit(text_surf, text_rect)

def display_ingame_screen(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons, update, solver_text):
    display.draw(sqmaze, offset_x, offset_y, zoom, rows, cols)
    button_draw(buttons)
    zoomlevel_diplay(zoom)
    solver_diplay(solver_text)
    solved_display()
    timer()
    if update == 0:
        pygame.display.flip()
    elif update == 1:
        pygame.display.update()

def display_mazecell(offset_x, offset_y, zoom, i, j, sqmaze):
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
        pygame.draw.line(globals.screen,color,
            ((i+offset_x + globals.centre_x) *  zoom, (j+offset_y + globals.centre_y) * zoom),
            ((i+offset_x + globals.centre_x) *  zoom, (j+offset_y+1 + globals.centre_y) * zoom-1),
            zoom)
    update_rect = [pygame.Rect((i+offset_x + globals.centre_x) *  zoom-(((zoom/3)+(zoom-1)/5)-1), (j+offset_y + globals.centre_y) * zoom, zoom+((zoom/3)+(zoom-1)/5), zoom), pygame.Rect(pygame.display.Info().current_w-180, 50, 170, 30)]
    solved_display()
    pygame.display.update(update_rect)  

def display_timer():
    if globals.timer_r == 1:
        globals.time = round(time.time()-globals.start_t, 3)
    update_rect = pygame.Rect(10, 10, 170, 30)
    timer()
    pygame.display.update(update_rect) 

def endgame_display():
    font = pygame.font.SysFont(None, 40)
    rect = pygame.Rect(pygame.display.Info().current_w//4, pygame.display.Info().current_h//4 , pygame.display.Info().current_w//2, pygame.display.Info().current_h//4)
    pygame.draw.rect(globals.screen, (150, 00, 00), rect)
    text_surf = font.render('Congratulation! You won!', True, (10, 10, 10))
    text_rect = text_surf.get_rect(center=rect.center)
    globals.screen.blit(text_surf, text_rect)
    font = pygame.font.SysFont(None, 20)
    rect = pygame.Rect(10, 10, 170, 30)
    pygame.draw.rect(globals.screen, (50, 50, 50), rect)
    text_surf = font.render('Time: ' + str(globals.time), True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=rect.center)
    globals.screen.blit(text_surf, text_rect)



def endgame_display_solved():
    font = pygame.font.SysFont(None, 40)
    rect = pygame.Rect(pygame.display.Info().current_w//4, pygame.display.Info().current_h//4 , pygame.display.Info().current_w//2, pygame.display.Info().current_h//4)
    pygame.draw.rect(globals.screen, (150, 00, 00), rect)
    text_surf = font.render('Congratulation! The algorithm solved the maze!', True, (10, 10, 10))
    text_rect = text_surf.get_rect(center=rect.center)
    globals.screen.blit(text_surf, text_rect)
    font = pygame.font.SysFont(None, 20)
    rect = pygame.Rect(10, 10, 170, 30)
    pygame.draw.rect(globals.screen, (50, 50, 50), rect)
    text_surf = font.render('Time: ' + str(globals.time), True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=rect.center)
    globals.screen.blit(text_surf, text_rect)


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

    MyConfig = gameConfig()

# Define variables needed
    rows = MyConfig.last_rows
    cols = MyConfig.last_cols
    seed_enabled = False
    seed = 1683387020
    offset_x, offset_y = 0, 0
    solver = 0
    solver_text = 'GBFS'
    globals.timer_r = 0
    MyPlayer = Player(MyConfig.last_player)
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
        button.draw()
# plain texts
    display.textDisplay('Maze size', globals.setup_screen_fontsize, pygame.Rect(pygame.display.Info().current_w-globals.setup_screen_fontsize*5, 20 , globals.setup_screen_fontsize*5-20, globals.setup_screen_fontsize+10), globals.setup_screen_bg_color, globals.setup_screen_font_color)
    display.textDisplay('Rows:', 20, pygame.Rect(pygame.display.Info().current_w-globals.setup_screen_fontsize*5, 1*(globals.setup_screen_fontsize+20)+20 , globals.setup_screen_fontsize*3, globals.setup_screen_fontsize+10), globals.setup_screen_bg_color, globals.setup_screen_font_color)
    display.textDisplay('Cols:', 20, pygame.Rect(pygame.display.Info().current_w-globals.setup_screen_fontsize*5, 2*(globals.setup_screen_fontsize+20)+20 , globals.setup_screen_fontsize*3, globals.setup_screen_fontsize+10), globals.setup_screen_bg_color, globals.setup_screen_font_color)
    display.textDisplay('Game mode', globals.setup_screen_fontsize, pygame.Rect(pygame.display.Info().current_w-globals.setup_screen_fontsize*5, 3*(globals.setup_screen_fontsize+20)+20 , globals.setup_screen_fontsize*5-20, globals.setup_screen_fontsize+10), globals.setup_screen_bg_color, globals.setup_screen_font_color)
    display.textDisplay('Seed', globals.setup_screen_fontsize, pygame.Rect(pygame.display.Info().current_w-globals.setup_screen_fontsize*5, 5*(globals.setup_screen_fontsize+20)+20 , globals.setup_screen_fontsize*5-20, globals.setup_screen_fontsize+10), globals.setup_screen_bg_color, globals.setup_screen_font_color)
    display.textDisplay('Enter your name!', globals.setup_screen_fontsize, pygame.Rect(pygame.display.Info().current_w//2-globals.setup_screen_fontsize*3, 2*(globals.setup_screen_fontsize+20)+20 , globals.setup_screen_fontsize*6, globals.setup_screen_fontsize+10), globals.setup_screen_bg_color, globals.setup_screen_font_color)

# input fields
    startscreen_inputs = []
    startscreen_inputs.append(InputBox_number(str(rows),pygame.display.Info().current_w-globals.setup_screen_fontsize*2, 1*(globals.setup_screen_fontsize+20)+20 , globals.setup_screen_fontsize*2-20, globals.setup_screen_fontsize+10,3))
    startscreen_inputs.append(InputBox_number(str(cols),pygame.display.Info().current_w-globals.setup_screen_fontsize*2, 2*(globals.setup_screen_fontsize+20)+20  , globals.setup_screen_fontsize*2-20, globals.setup_screen_fontsize+10,3))
    startscreen_inputs.append(InputBox_number('0',pygame.display.Info().current_w-globals.setup_screen_fontsize*5, 6*(globals.setup_screen_fontsize+20)+20  , globals.setup_screen_fontsize*5-20, globals.setup_screen_fontsize+10,12))
    startscreen_inputs.append(InputBox_Playername(MyPlayer.name,pygame.display.Info().current_w//2-globals.setup_screen_fontsize*3, 3*(globals.setup_screen_fontsize+20)+20  , globals.setup_screen_fontsize*6, globals.setup_screen_fontsize+10,20,MyPlayer))
    for inputbox in startscreen_inputs:
        inputbox.draw()

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

    rows=int(startscreen_inputs[0].text)
    cols=int(startscreen_inputs[1].text)
    seed_enabled = True
    if startscreen_inputs[2].text == '0' or startscreen_inputs[2].text == '':
        seed_enabled = False
        startscreen_inputs[2].text = '0'
    seed=int(startscreen_inputs[2].text)

    MyConfig.last_player = MyPlayer.name
    MyConfig.last_rows = rows
    MyConfig.last_cols = cols
    MyConfig.save()


# display parameters
    zoom_y = pygame.display.Info().current_h // (2 * rows)
    zoom_x = pygame.display.Info().current_w // (2 * cols)
    zoom = min(zoom_x,zoom_y)
    if zoom_y >= zoom_x:
        globals.centre_y = pygame.display.Info().current_h // zoom // 2 - rows
        globals.centre_x = 0
    else:
        globals.centre_y = 0
        globals.centre_x = pygame.display.Info().current_w // zoom // 2 - cols

    # globals.centre_y = ((pygame.display.Info().current_h // (pygame.display.Info().current_h // (2 * rows + 1)) // 2) - rows)
    # globals.centre_x = ((pygame.display.Info().current_w // (pygame.display.Info().current_w // (2 * cols + 1)) // 2) - cols)

    temp = rows
    rows = cols
    cols = temp

# Generate maze
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
    display_ingame_screen(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons, 0, solver_text)
#Handle pygame events
    running = True
    pygame.key.set_repeat(200, 50)
    while running:
        display_timer()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
# keydown events
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    offset_x -= 1
                    display_ingame_screen(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons, 0, solver_text)
                elif event.key == pygame.K_RIGHT:
                    offset_x += 1
                    display_ingame_screen(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons, 0, solver_text)
                elif event.key == pygame.K_UP:
                    offset_y -= 1
                    display_ingame_screen(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons, 0, solver_text)
                elif event.key == pygame.K_DOWN:
                    offset_y += 1
                    display_ingame_screen(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons, 0, solver_text)
                elif event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:
                    zoom += 1
                    globals.centre_y = ((pygame.display.Info().current_h / zoom / 2) - rows)
                    globals.centre_x = ((pygame.display.Info().current_w / zoom / 2) - cols)
                    display_ingame_screen(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons, 0, solver_text)
                elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                    zoom = max(1, zoom - 1)
                    globals.centre_y = ((pygame.display.Info().current_h / zoom / 2) - rows)
                    globals.centre_x = ((pygame.display.Info().current_w / zoom / 2) - cols)
                    display_ingame_screen(sqmaze,  offset_x, offset_y, zoom, rows, cols, buttons, 0, solver_text)
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
                            display_ingame_screen(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons, 1, solver_text)
                            if sqmaze[mazex - 1][mazey] == 4 or sqmaze[mazex + 1][mazey] == 4 or sqmaze[mazex][mazey - 1] == 4 or sqmaze[mazex][mazey + 1] == 4:
                                for i in range(2*rows+1):
                                    for j in range(2*cols+1):
                                        if sqmaze[i][j] == 2:
                                            sqmaze[i][j] = 5
                                display_ingame_screen(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons, 1, solver_text)
                                endgame_display()
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
                            display_ingame_screen(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons, 1, solver_text)
# screen button events                    
            for button in buttons:
                button.handle_event(event)

            if buttons[0].clicked:
                zoom += 1
                globals.centre_y = ((pygame.display.Info().current_h / zoom / 2) - rows)
                globals.centre_x = ((pygame.display.Info().current_w / zoom / 2) - cols)
                display_ingame_screen(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons, 0, solver_text)
                pygame.event.clear

            if buttons[1].clicked:
                globals.centre_y = ((pygame.display.Info().current_h / zoom / 2) - rows)
                globals.centre_x = ((pygame.display.Info().current_w / zoom / 2) - cols)
                zoom = max(1, zoom - 1)
                display_ingame_screen(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons, 0, solver_text)
                pygame.event.clear

            if buttons[2].clicked:
                reset(rows, cols, sqmaze, pathmaze, startpos)
                display_ingame_screen(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons, 1, solver_text)
                pygame.event.clear

            if buttons[3].clicked:
                if solver == 0:
                    solver_text = 'A*'
                    solver = 1
                elif solver == 1:
                    solver_text = 'DFS'
                    solver = 2
                elif solver == 2:
                    solver_text = 'BFS'
                    solver = 3
                elif solver == 3:
                    solver_text = 'Dijkstra'
                    solver = 4
                elif solver == 4:
                    solver_text = 'GBFS'
                    solver = 0
                display_ingame_screen(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons, 1, solver_text)
                pygame.event.clear



            if buttons[4].clicked:
                reset(rows, cols, sqmaze, pathmaze, startpos)
                globals.alg_sp = 0
                if globals.timer_r == 0:
                    globals.start_t = time.time()
                    globals.timer_r = 1
                display_ingame_screen(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons, 1, solver_text)
                if solver == 0:
                    solution = solve.GBFS(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons)
                if solver == 1:
                    solution = solve.astar(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons)
                if solver == 2:
                    solution = solve.dfs(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons)
                if solver == 3:
                    solution = solve.bfs(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons)
                if solver == 4:
                    solution = solve.dijkstra(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons)
                for so in solution:
                    sqmaze[so[0]][so[1]] = 5
                sqmaze[1][startpos] = 3
                sqmaze[2 * rows - 1][endpos] = 4
                display_ingame_screen(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons, 1, solver_text)
                globals.timer_r = 0
                endgame_display_solved()
                pygame.display.flip()
                pygame.event.clear(pygame.MOUSEBUTTONDOWN)

            if buttons[5].clicked:
                sqmaze, pathmaze, startpos, endpos = generate_maze(rows, cols, seed, seed_enabled)
                globals.path_nmbr = 0
                for i in range(rows * 2 + 1):
                    for j in range(cols * 2 + 1):
                        if sqmaze[i][j] == 1:
                            globals.path_nmbr = globals.path_nmbr + 1
                display_ingame_screen(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons, 0, solver_text)
                pygame.event.clear


            if buttons[6].clicked:
                running = False


pygame.quit()

if __name__ == "__main__":
    main()
