import pygame
import generate
import display
import random
import pygame
import numpy
import solve
import globals
import time

class Button:
    def __init__(self, text, x, y, width, height):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (50, 50, 50)
        self.hover_color = (25, 25, 25)
        self.font = pygame.font.SysFont(None, 20)
        self.clicked = False

    def draw(self, surface):
        color = self.hover_color if self.rect.collidepoint(pygame.mouse.get_pos()) else self.color
        pygame.draw.rect(surface, color, self.rect)
        text_surf = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.clicked = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.clicked = False

def button_draw(screen, buttons):
        for button in buttons:
            button.draw(screen)

def zoomlevel_diplay(screen,zoom_level):
    font = pygame.font.SysFont(None, 20)
    rect = pygame.Rect(pygame.display.Info().current_w-110, 10, 100, 30)
    pygame.draw.rect(screen, (50, 50, 50), rect)
    text_surf = font.render('Zoom level: ' + str(zoom_level), True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)

def solver_diplay(screen,solver_text):
    font = pygame.font.SysFont(None, 20)
    rect = pygame.Rect(pygame.display.Info().current_w-110, 50, 100, 30)
    pygame.draw.rect(screen, (50, 50, 50), rect)
    text_surf = font.render('Solver ' + str(solver_text), True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)

def display_ingame_screen(sqmaze, screen, offset_x, offset_y, zoom, rows, cols, buttons, update, solver_text):
    display.draw(sqmaze, screen, offset_x, offset_y, zoom, rows, cols)
    button_draw(screen, buttons)
    zoomlevel_diplay(screen,zoom)
    solver_diplay(screen,solver_text)
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
            ((i+offset_x) *  zoom, (j+offset_y) * zoom),
            ((i+offset_x) *  zoom, (j+offset_y+1) * zoom-1),
            zoom)
    update_rect = pygame.Rect((i+offset_x) *  zoom-(((zoom/3)+(zoom-1)/5)-1), (j+offset_y) * zoom, zoom+((zoom/3)+(zoom-1)/5), zoom)
    pygame.display.update(update_rect)

def endgame_display(screen):
    font = pygame.font.SysFont(None, 40)
    rect = pygame.Rect(pygame.display.Info().current_w//4, pygame.display.Info().current_h//4 , pygame.display.Info().current_w//2, pygame.display.Info().current_h//4)
    pygame.draw.rect(screen, (150, 00, 00), rect)
    text_surf = font.render('Congratulation! You won!', True, (10, 10, 10))
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)


def endgame_display_solved(screen):
    font = pygame.font.SysFont(None, 40)
    rect = pygame.Rect(pygame.display.Info().current_w//4, pygame.display.Info().current_h//4 , pygame.display.Info().current_w//2, pygame.display.Info().current_h//4)
    pygame.draw.rect(screen, (150, 00, 00), rect)
    text_surf = font.render('Congratulation! The algorithm solved the maze!', True, (10, 10, 10))
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


def main():
    globals.global_init()
#Initialize pygame
    pygame.init()
    pygame.display.set_caption('The Wonder of Mazes')
# Use this to set full screen
#     screen = pygame.display.set_mode((pygame.display.Info().current_w, pygame.display.Info().current_h))
#    window_width=800
#    window_height=800
    window_width=pygame.display.Info().current_w
    window_height=pygame.display.Info().current_h
    screen = pygame.display.set_mode((window_width, window_height))
# setting up the start screen
    startscreen_buttons = []
    startscreen_buttons.append(Button('Start game', (window_width-100)/2, (window_height-30)/2, 100, 30))
    for button in startscreen_buttons:
        button.draw(screen)
    pygame.display.flip()
# event loop for the start screen
    running = True
    pygame.key.set_repeat(200, 10)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
# game starts by key s or clicking the start button
# keydown events
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    running = False
# screen button events                    
            for button in startscreen_buttons:
                button.handle_event(event)

            if startscreen_buttons[0].clicked:
                running = False

#Define variables needed
    rows = 10
    cols = 10
    seed_enabled = True
    seed = 1682355278
    offset_x, offset_y =0, 0
    zoom = 3
    solver = 0
    solver_text = 'GBFS'

#Generate maze
    sqmaze, pathmaze, startpos, endpos = generate_maze(rows, cols, seed, seed_enabled)
# setting up the start ingame screen
    buttons = []
    buttons.append(Button('Zoom In', pygame.display.Info().current_w-110,90, 100, 30))
    buttons.append(Button('Zoom Out',pygame.display.Info().current_w-110, 130, 100, 30))
    buttons.append(Button('Restart',pygame.display.Info().current_w-110, 170, 100, 30))
    buttons.append(Button('Change Solver',pygame.display.Info().current_w-110, 210, 100, 30))    
    buttons.append(Button('Solve',pygame.display.Info().current_w-110, 250, 100, 30))
    buttons.append(Button('Re-generate',pygame.display.Info().current_w-110, 290, 100, 30))
    buttons.append(Button('Quit',pygame.display.Info().current_w-110, 330, 100, 30))
#Draw maze on screen
    display_ingame_screen(sqmaze, screen, offset_x, offset_y, zoom, rows, cols, buttons, 0, solver_text)
#Handle pygame events
    running = True
    pygame.key.set_repeat(200, 10)
    while running:
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
                    display_ingame_screen(sqmaze, screen, offset_x, offset_y, zoom, rows, cols, buttons, 0, solver_text)
                elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                    zoom = max(1, zoom - 1)
                    display_ingame_screen(sqmaze, screen, offset_x, offset_y, zoom, rows, cols, buttons, 0, solver_text)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mazex = int((event.pos[0] + zoom / 2) // zoom - offset_x)
                mazey = int((event.pos[1]) // zoom - offset_y)
                if mazex > -1 and mazex < 2 * cols + 1 and mazey > -1 and mazey < 2 * rows + 1:
                    if sqmaze[mazex][mazey] == 1:
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
                            display_ingame_screen(sqmaze, screen, offset_x, offset_y, zoom, rows, cols, buttons, 1, solver_text)
# screen button events                    
            for button in buttons:
                button.handle_event(event)

            if buttons[0].clicked:
                zoom += 1
                display_ingame_screen(sqmaze, screen, offset_x, offset_y, zoom, rows, cols, buttons, 0, solver_text)
                pygame.event.clear

            if buttons[1].clicked:
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
                    solver_text = 'GBFS'
                    solver = 0
                    display_ingame_screen(sqmaze, screen, offset_x, offset_y, zoom, rows, cols, buttons, 1, solver_text)
                pygame.event.clear



            if buttons[4].clicked:
                reset(rows, cols, sqmaze, pathmaze, startpos)
                display_ingame_screen(sqmaze, screen, offset_x, offset_y, zoom, rows, cols, buttons, 1, solver_text)
                if solver == 0:
                    solution = solve.GBFS(sqmaze, screen, offset_x, offset_y, zoom, rows, cols, buttons)
                if solver == 1:
                    solution = solve.astar(sqmaze, screen, offset_x, offset_y, zoom, rows, cols, buttons)
                for so in solution:
                    sqmaze[so[0]][so[1]] = 5
                sqmaze[1][startpos] = 3
                sqmaze[2 * rows - 1][endpos] = 4
                display_ingame_screen(sqmaze, screen, offset_x, offset_y, zoom, rows, cols, buttons, 1, solver_text)
                endgame_display_solved(screen)
                pygame.display.flip()
                pygame.event.clear

            if buttons[5].clicked:
                sqmaze, pathmaze, startpos, endpos = generate_maze(rows, cols, seed, seed_enabled)
                display_ingame_screen(sqmaze, screen, offset_x, offset_y, zoom, rows, cols, buttons, 0, solver_text)
                pygame.event.clear


            if buttons[6].clicked:
                running = False


    pygame.quit()


if __name__ == "__main__":
    main()

