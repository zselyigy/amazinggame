import pygame
import globals
import time
import unicodedata

def textDisplay(text, fontsize, rect, bgcolor, tcolor):
    font = pygame.font.SysFont(None, fontsize)
    pygame.draw.rect(globals.screen, bgcolor, rect)
    text_surf = font.render(text, True, tcolor)
    text_rect = text_surf.get_rect(center=rect.center)
    globals.screen.blit(text_surf, text_rect)
    pygame.display.update(rect)

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
        textDisplay(self.text, self.fontsize, self.rect, color, (255, 255, 255))

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
        textDisplay('Welcome, '+self.Player.name+'!', globals.setup_screen_fontsize, pygame.Rect(pygame.display.Info().current_w//2-globals.setup_screen_fontsize*5, 20 , globals.setup_screen_fontsize*10, globals.setup_screen_fontsize+10), globals.setup_screen_bg_color, globals.setup_screen_font_color)

    def StartScreen_Refresh(self):
        self.Player.name = self.text
        self.startscreen_display()
        pygame.display.flip()


class baseButton:
    def __init__(self, text, x, y, width, height):
        self.counter = 0
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (50, 50, 50)
        self.hover_color = (25, 25, 25)
        self.fontsize = 20
        self.font = pygame.font.SysFont(None, self.fontsize)
        self.clicked = False

    def draw(self):
        color = self.hover_color if self.clicked else self.color
        textDisplay(self.text, self.fontsize, self.rect, color, (255, 255, 255))


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
                self.counter = 1

class SelfScrollButton(baseButton):
    def __init__(self, textarray, x, y, width, height):
        self.textarray = textarray
        self.counter = 0
        super().__init__(self.textarray[self.counter], x, y, width, height)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.clicked = True
                if self.counter==len(self.textarray)-1:
                    self.counter=0
                else:
                    self.counter = self.counter + 1
                self.text=self.textarray[self.counter]
                self.draw()
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.clicked = False
                self.draw()

class GameModeButton(baseButton):
    def __init__(self, textarray, x, y, width, height):
        self.textarray = textarray
        self.counter = self.textarray.index(globals.gamemode_text)
        self.text=globals.gamemode_text
        super().__init__(self.text, x, y, width, height)
#        self.allowed_gamemodes = ['Solve the maze']
        self.allowed_gamemodes = [globals.gamemode_solvethemaze,globals.gamemode_timelimited,globals.gamemode_speedrun]

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

def solved_display():
    font = pygame.font.SysFont(None, 20)
    rect = pygame.Rect(pygame.display.Info().current_w-180, 50, 170, 30)
    pygame.draw.rect(globals.screen, (50, 50, 50), rect)
    text = "Maze explored: {:.2f}%"
    text_surf = font.render(text.format(globals.percentage), True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=rect.center)
    globals.screen.blit(text_surf, text_rect)

def display_endgame():
    textDisplay('Congratulation! You won!', 40, pygame.Rect(pygame.display.Info().current_w//4, pygame.display.Info().current_h//4 , pygame.display.Info().current_w//2, pygame.display.Info().current_h//4), (150, 00, 00), (255, 255, 255))
    textDisplay('Time: ' + str(globals.time), 20, pygame.Rect(10, 10, 170, 30), (50, 50, 50), (255, 255, 255))

def display_endgame_solved():
    textDisplay('Congratulation! The algorithm solved the maze!', 40, pygame.Rect(pygame.display.Info().current_w//4, pygame.display.Info().current_h//4 , pygame.display.Info().current_w//2, pygame.display.Info().current_h//4), (150, 0, 0), (255, 255, 255))
    textDisplay('Time: ' + str(globals.time), 20, pygame.Rect(10, 10, 170, 30), (50, 50, 50), (255, 255, 255))

def timer():
    font = pygame.font.SysFont(None, 20)
    rect = pygame.Rect(pygame.display.Info().current_w-180, 90, 170, 30)
    pygame.draw.rect(globals.screen, (50, 50, 50), rect)
    text_surf = font.render('Time: ' + str(globals.time), True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=rect.center)
    globals.screen.blit(text_surf, text_rect)

def display_timer():
    if globals.timer_r == 1:
        globals.time = round(time.time()-globals.start_t, 3)
    update_rect = pygame.Rect(pygame.display.Info().current_w-180, 90, 170, 30)
    timer()
    pygame.display.update(update_rect) 

def start_screen(startscreen_buttons, startscreen_inputs, rows, cols, MyPlayer):
    # clear the screen
    globals.screen.fill((0,0,0))
    # startescreen buttons
    startscreen_buttons.append(Button('Start game', (pygame.display.Info().current_w-100)/2, (pygame.display.Info().current_h-30)/2, 100, 30))
    startscreen_buttons.append(Button('Quit', (pygame.display.Info().current_w-100)/2, (pygame.display.Info().current_h-30)/2 + 40, 100, 30))    
    startscreen_buttons.append(GameModeButton([globals.gamemode_solvethemaze,globals.gamemode_timelimited,globals.gamemode_speedrun], pygame.display.Info().current_w-globals.setup_screen_fontsize*5, 4*(globals.setup_screen_fontsize+20)+20 , globals.setup_screen_fontsize*5-20, globals.setup_screen_fontsize+10))
    for button in startscreen_buttons:
        button.draw()
    # plain texts
    textDisplay('Maze size', globals.setup_screen_fontsize, pygame.Rect(pygame.display.Info().current_w-globals.setup_screen_fontsize*5, 20 , globals.setup_screen_fontsize*5-20, globals.setup_screen_fontsize+10), globals.setup_screen_bg_color, globals.setup_screen_font_color)
    textDisplay('Rows:', 20, pygame.Rect(pygame.display.Info().current_w-globals.setup_screen_fontsize*5, 1*(globals.setup_screen_fontsize+20)+20 , globals.setup_screen_fontsize*3, globals.setup_screen_fontsize+10), globals.setup_screen_bg_color, globals.setup_screen_font_color)
    textDisplay('Cols:', 20, pygame.Rect(pygame.display.Info().current_w-globals.setup_screen_fontsize*5, 2*(globals.setup_screen_fontsize+20)+20 , globals.setup_screen_fontsize*3, globals.setup_screen_fontsize+10), globals.setup_screen_bg_color, globals.setup_screen_font_color)
    textDisplay('Game mode', globals.setup_screen_fontsize, pygame.Rect(pygame.display.Info().current_w-globals.setup_screen_fontsize*5, 3*(globals.setup_screen_fontsize+20)+20 , globals.setup_screen_fontsize*5-20, globals.setup_screen_fontsize+10), globals.setup_screen_bg_color, globals.setup_screen_font_color)
    textDisplay('Seed', globals.setup_screen_fontsize, pygame.Rect(pygame.display.Info().current_w-globals.setup_screen_fontsize*5, 5*(globals.setup_screen_fontsize+20)+20 , globals.setup_screen_fontsize*5-20, globals.setup_screen_fontsize+10), globals.setup_screen_bg_color, globals.setup_screen_font_color)
    textDisplay('Enter your name!', globals.setup_screen_fontsize, pygame.Rect(pygame.display.Info().current_w//2-globals.setup_screen_fontsize*3, 2*(globals.setup_screen_fontsize+20)+20 , globals.setup_screen_fontsize*6, globals.setup_screen_fontsize+10), globals.setup_screen_bg_color, globals.setup_screen_font_color)
    # input fields
    startscreen_inputs.append(InputBox_number(str(rows),pygame.display.Info().current_w-globals.setup_screen_fontsize*2, 1*(globals.setup_screen_fontsize+20)+20 , globals.setup_screen_fontsize*2-20, globals.setup_screen_fontsize+10,3))
    startscreen_inputs.append(InputBox_number(str(cols),pygame.display.Info().current_w-globals.setup_screen_fontsize*2, 2*(globals.setup_screen_fontsize+20)+20  , globals.setup_screen_fontsize*2-20, globals.setup_screen_fontsize+10,3))
    startscreen_inputs.append(InputBox_number('0',pygame.display.Info().current_w-globals.setup_screen_fontsize*5, 6*(globals.setup_screen_fontsize+20)+20  , globals.setup_screen_fontsize*5-20, globals.setup_screen_fontsize+10,12))
    startscreen_inputs.append(InputBox_Playername(MyPlayer.name,pygame.display.Info().current_w//2-globals.setup_screen_fontsize*3, 3*(globals.setup_screen_fontsize+20)+20  , globals.setup_screen_fontsize*6, globals.setup_screen_fontsize+10,20,MyPlayer))
    for inputbox in startscreen_inputs:
        inputbox.draw()
    # show the screen
    pygame.display.flip()

def draw_sqmaze(sqmaze, offset_x, offset_y, zoom, rows, cols, accessed_tiles):
    for i in range(2*rows+1):
        for j in range(2*cols+1):
            color = (0, 0, 0)
            if sqmaze[i][j] == 1:
                color = globals.alg_s
                try:
                    tileindex = accessed_tiles.index([j, i])
                except ValueError:
                    color = globals.path          
            elif sqmaze[i][j] == 2:
                color = globals.sel_path
            elif sqmaze[i][j] == 3:
                color = globals.start_c
            elif sqmaze[i][j] == 4:
                color = globals.end_c
            elif sqmaze[i][j] == 5:
                color = globals.fin_path
            elif sqmaze[i][j] == 6:
                color = globals.alg_s

            if color != (0, 0, 0):
                pygame.draw.line(globals.screen, color,
                    (globals.sc_x + zoom * (j - globals.mc_x + offset_x), globals.sc_y + zoom * (i - globals.mc_y + offset_y - 0.5)),
                    (globals.sc_x + zoom * (j - globals.mc_x + offset_x), globals.sc_y + zoom * (i - globals.mc_y + offset_y + 0.5)),
                    zoom)

def draw(sqmaze, offset_x, offset_y, zoom, rows, cols, accessed_tiles):
    globals.screen.fill((0, 0, 0))
    draw_sqmaze(sqmaze, offset_x, offset_y, zoom, rows, cols, accessed_tiles)


def ingame_screen(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons, update, accessed_tiles):
    ingame_button_height = 30
    buttons.append(Button('Zoom In', pygame.display.Info().current_w-180, 1*(ingame_button_height + 10) + 90, 170, ingame_button_height))
    buttons.append(Button('Zoom Out',pygame.display.Info().current_w-180, 2*(ingame_button_height + 10) + 90, 170, ingame_button_height))
    buttons.append(Button('Center maze',pygame.display.Info().current_w-180, 3*(ingame_button_height + 10) + 90, 170, ingame_button_height))
    buttons.append(Button('Restart',pygame.display.Info().current_w-180, 4*(ingame_button_height + 10) + 90, 170, ingame_button_height))
    buttons.append(SelfScrollButton(['Solver: GBFS','Solver: A*','Solver: DFS','Solver: BFS','Solver: Dijkstra'], pygame.display.Info().current_w-180, 5*(ingame_button_height + 10) + 90, 170, ingame_button_height))   
    buttons.append(Button('Solve',pygame.display.Info().current_w-180, 6*(ingame_button_height + 10) + 90, 170, ingame_button_height))
    buttons.append(Button('Re-generate',pygame.display.Info().current_w-180, 7*(ingame_button_height + 10) + 90, 170, ingame_button_height))
    buttons.append(SelfScrollButton(['Click and drag','Click direction','Arrows'], pygame.display.Info().current_w-180, 8*(ingame_button_height + 10) + 90, 170, ingame_button_height))   
    buttons.append(Button('Quit to main menu',pygame.display.Info().current_w-180, 9*(ingame_button_height + 10) + 90, 170, ingame_button_height))
    buttons.append(Button('Quit',pygame.display.Info().current_w-180, 10*(ingame_button_height + 10) + 90, 170, ingame_button_height))
    refresh_ingame_screen(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons, update, accessed_tiles)

def refresh_ingame_screen(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons, update, accessed_tiles):
    draw(sqmaze, offset_x, offset_y, zoom, rows, cols, accessed_tiles)
    for button in buttons:
        button.draw()
    textDisplay(globals.gamemode_text, 20, pygame.Rect(pygame.display.Info().current_w-180, 10, 170, 30), (0, 0, 0), (255, 255, 255))
    textDisplay('Zoom level: ' + str(zoom), 20, pygame.Rect(pygame.display.Info().current_w-180, pygame.display.Info().current_h-35, 170, 30), (0, 0, 0), (255, 255, 255))
    solved_display()
    timer()
    if update == 0:
        pygame.display.flip()
    elif update == 1:
        pygame.display.update()

def display_mazecell(offset_x, offset_y, zoom, i, j, sqmaze, accessed_tiles):
    color = (0, 0, 0)
    if sqmaze[i][j] == 1:
        color = globals.alg_s
        try:
            tileindex = accessed_tiles.index([j, i])
        except ValueError:
            color = globals.path          
    elif sqmaze[i][j] == 2:
        color = globals.sel_path
    elif sqmaze[i][j] == 3:
        color = globals.start_c
    elif sqmaze[i][j] == 4:
        color = globals.end_c
    elif sqmaze[i][j] == 5:
        color = globals.fin_path
    elif sqmaze[i][j] == 6:
        color = globals.alg_s

    if color != (0, 0, 0):
            pygame.draw.line(globals.screen, color,
                (globals.sc_x + zoom * (j - globals.mc_x + offset_x), globals.sc_y + zoom * (i - globals.mc_y + offset_y - 0.5)),
                (globals.sc_x + zoom * (j - globals.mc_x + offset_x), globals.sc_y + zoom * (i - globals.mc_y + offset_y + 0.5)),
                zoom)
#    update_rect = [pygame.Rect((i+offset_x + globals.centre_x) *  zoom-(((zoom/3)+(zoom-1)/5)-1), (j+offset_y + globals.centre_y) * zoom, zoom+((zoom/3)+(zoom-1)/5), zoom), pygame.Rect(pygame.display.Info().current_w-180, 50, 170, 30)]
    update_rect = [pygame.Rect(globals.sc_x + zoom * (j - globals.mc_x + offset_x - 0.5), globals.sc_y + zoom * (i - globals.mc_y + offset_y - 0.5), zoom + 1, zoom + 1), pygame.Rect(pygame.display.Info().current_w-180, 50, 170, 30)]
    solved_display()
    pygame.display.update(update_rect)  
