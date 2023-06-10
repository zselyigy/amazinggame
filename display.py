import pygame
import globals
import time

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
