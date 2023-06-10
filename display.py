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

def draw_maze(maze, offset_x, offset_y, zoom, centre_x, centre_y):
    for edge in maze:
        x1, y1 = edge[0][1], edge[0][0]
        x2, y2 = edge[1][1], edge[1][0]

        # Add offsets to starting and ending points
        x1 += offset_x + centre_x
        y1 += offset_y + centre_y
        x2 += offset_x + centre_x
        y2 += offset_y + centre_y
        if not (x1 == 0 or y1 == 0 or x2 == 0 or y2 == 0 or x1 == len(maze)-1 or y1 == len(maze[0])-1 or x2 == len(maze)-1 or y2 == len(maze[0])-1):
            # Draw white path
            path_width = max(1, int(zoom//2))
            if x1<x2:
                pygame.draw.line(globals.screen, (255, 255, 255),
                                (int(x1  * zoom- int(path_width/2)), y1 * zoom),
                                (int(x2 * zoom+ int(path_width/2)), y2 * zoom),
                                path_width)

            else:
                pygame.draw.line(globals.screen, (255, 255, 255),
                                (x1 * zoom, int(y1 * zoom)- int(path_width/2)),
                                (x2  * zoom, int(y2 * zoom)+ int(path_width/2)),
                                path_width)

            pygame.display.flip()

def draw_sqmaze(sqmaze, offset_x, offset_y, zoom, rows, cols):
    path_width = zoom
    for i in range(2*rows+1):
        for j in range(2*cols+1):
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
                pygame.draw.line(globals.screen, color,
                    ((i+offset_x + globals.centre_x) *  zoom, (j+offset_y + globals.centre_y) * zoom),
                    ((i+offset_x + globals.centre_x) *  zoom, (j+offset_y+1 + globals.centre_y) * zoom-1),
                    path_width)

def draw(sqmaze, offset_x, offset_y, zoom, rows, cols):
    globals.screen.fill((0, 0, 0))
    draw_sqmaze(sqmaze, offset_x, offset_y, zoom, rows, cols)

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
        textDisplay(self.text, self.fontsize, self.rect, color, (255, 255, 255))

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

def zoomlevel_diplay(zoom_level):
    font = pygame.font.SysFont(None, 20)
    rect = pygame.Rect(pygame.display.Info().current_w-180, 10, 170, 30)
    pygame.draw.rect(globals.screen, (50, 50, 50), rect)
    text_surf = font.render('Zoom level: ' + str(zoom_level), True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=rect.center)
    globals.screen.blit(text_surf, text_rect)

def solver_diplay(searched_text):
    font = pygame.font.SysFont(None, 20)
    rect = pygame.Rect(pygame.display.Info().current_w-180, 90, 170, 30)
    pygame.draw.rect(globals.screen, (50, 50, 50), rect)
    text_surf = font.render('Solver: ' + str(searched_text), True, (255, 255, 255))
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

def timer():
    font = pygame.font.SysFont(None, 20)
    rect = pygame.Rect(10, 10, 170, 30)
    pygame.draw.rect(globals.screen, (50, 50, 50), rect)
    text_surf = font.render('Time: ' + str(globals.time), True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=rect.center)
    globals.screen.blit(text_surf, text_rect)

def display_timer():
    if globals.timer_r == 1:
        globals.time = round(time.time()-globals.start_t, 3)
    update_rect = pygame.Rect(10, 10, 170, 30)
    timer()
    pygame.display.update(update_rect) 

def start_screen(startscreen_buttons, startscreen_inputs, rows, cols, MyPlayer):
    # startescreen buttons
    startscreen_buttons.append(Button('Start game', (pygame.display.Info().current_w-100)/2, (pygame.display.Info().current_h-30)/2, 100, 30))
    startscreen_buttons.append(Button('Quit', (pygame.display.Info().current_w-100)/2, (pygame.display.Info().current_h-30)/2 + 40, 100, 30))    
    startscreen_buttons.append(GameModeButton(['Solve the maze','Time limited','Speed run'], pygame.display.Info().current_w-globals.setup_screen_fontsize*5, 4*(globals.setup_screen_fontsize+20)+20 , globals.setup_screen_fontsize*5-20, globals.setup_screen_fontsize+10))
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


def ingame_screen(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons, update, solver_text):
    ingame_button_height = 30
    buttons.append(Button('Zoom In', pygame.display.Info().current_w-180, 1*(ingame_button_height + 10) + 90, 170, ingame_button_height))
    buttons.append(Button('Zoom Out',pygame.display.Info().current_w-180, 2*(ingame_button_height + 10) + 90, 170, ingame_button_height))
    buttons.append(Button('Restart',pygame.display.Info().current_w-180, 3*(ingame_button_height + 10) + 90, 170, ingame_button_height))
    buttons.append(Button('Change Solver',pygame.display.Info().current_w-180, 4*(ingame_button_height + 10) + 90, 170, ingame_button_height))    
    buttons.append(Button('Solve',pygame.display.Info().current_w-180, 5*(ingame_button_height + 10) + 90, 170, ingame_button_height))
    buttons.append(Button('Re-generate',pygame.display.Info().current_w-180, 6*(ingame_button_height + 10) + 90, 170, ingame_button_height))
    buttons.append(Button('Quit',pygame.display.Info().current_w-180, 7*(ingame_button_height + 10) + 90, 170, ingame_button_height))
    refresh_ingame_screen(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons, update, solver_text)

def refresh_ingame_screen(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons, update, solver_text):
    draw(sqmaze, offset_x, offset_y, zoom, rows, cols)
    for button in buttons:
        button.draw()
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
