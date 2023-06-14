import pygame
import generate
import display
import random
import pygame
import numpy
import solve
import globals
import time
import math
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
            self.last_gamemode = globals.gamemode_solvethemaze

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
# Initialize pygame
    pygame.init()
    pygame.display.set_caption('The Wonder of Mazes')

    MyConfig = gameConfig()

# Define variables needed
    rows = MyConfig.last_rows
    cols = MyConfig.last_cols
    globals.gamemode_text = MyConfig.last_gamemode
    seed_enabled = False
    seed = 1683387020
    solver = 0
    solver_text = 'GBFS'
    globals.timer_r = 0
    MyPlayer = Player(MyConfig.last_player)
# Use this to set full screen
#     screen = pygame.display.set_mode((pygame.display.Info().current_w, pygame.display.Info().current_h))
#    window_width=800
#    window_height=800
    screen = pygame.display.set_mode((pygame.display.Info().current_w, pygame.display.Info().current_h))
    globals.screen = screen
# setting up the start screen
# arrays for the main components 
    startscreen_buttons = []    # buttons
    startscreen_inputs = []     # input fields
    display.start_screen(startscreen_buttons, startscreen_inputs, rows, cols, MyPlayer)

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
    globals.gamemode_text = startscreen_buttons[2].text

    MyConfig.last_player = MyPlayer.name
    MyConfig.last_rows = rows
    MyConfig.last_cols = cols
    MyConfig.last_gamemode = globals.gamemode_text
    MyConfig.save()


# display parameters
    zoom_y = pygame.display.Info().current_h // (2 * rows)
    zoom_x = pygame.display.Info().current_w // (2 * cols)
    zoom = min(zoom_x,zoom_y)
    zoom_init = zoom 

    globals.sc_x = pygame.display.Info().current_w // 2
    globals.sc_y = pygame.display.Info().current_h // 2

    temp = rows
    rows = cols
    cols = temp

    globals.mc_y = cols / 2
    globals.mc_x = rows / 2
    offset_y = -1 * cols // 2
    offset_x = -1 * rows // 2

# Generate maze
    sqmaze, pathmaze, startpos, endpos = generate_maze(rows, cols, seed, seed_enabled)
    for i in range(rows * 2 + 1):
        for j in range(cols * 2 + 1):
            if sqmaze[i][j] == 1:
                globals.path_nmbr = globals.path_nmbr + 1

# setting up the start ingame screen 
    buttons = []
# Setup and draw the ingame screen
    display.ingame_screen(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons, 0, solver_text)
#Handle pygame events
    running = True
    pygame.key.set_repeat(200, 50)
    while running:
        display.display_timer()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
# keydown events
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    offset_x -= 1
                    display.refresh_ingame_screen(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons, 0, solver_text)
                elif event.key == pygame.K_d:
                    offset_x += 1
                    display.refresh_ingame_screen(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons, 0, solver_text)
                elif event.key == pygame.K_w:
                    offset_y -= 1
                    display.refresh_ingame_screen(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons, 0, solver_text)
                elif event.key == pygame.K_s:
                    offset_y += 1
                    display.refresh_ingame_screen(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons, 0, solver_text)
                elif event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:
                    zoom += 1
                    display.refresh_ingame_screen(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons, 0, solver_text)
                elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                    zoom = max(1, zoom - 1)
                    display.refresh_ingame_screen(sqmaze,  offset_x, offset_y, zoom, rows, cols, buttons, 0, solver_text)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mazex = math.floor((event.pos[0] - globals.sc_x) / zoom + globals.mc_x - offset_x + 0.5)
                mazey = math.floor((event.pos[1] - globals.sc_y) / zoom + globals.mc_y - offset_y + 0.5)
                if mazex > -1 and mazex < 2 * rows + 1 and mazey > -1 and mazey < 2 * cols + 1:
                    if sqmaze[mazex][mazey] == 1:    # the tile is empty. check if selectable or not
                        if (pathmaze[mazex - 1][mazey] + pathmaze[mazex + 1][mazey] + pathmaze[mazex][mazey - 1] + pathmaze[mazex][mazey + 1]) == 1:
                            if pathmaze[mazex - 1][mazey] > 0:
                                pathmaze[mazex - 1][mazey] = pathmaze[mazex - 1][mazey] + 1
                            if pathmaze[mazex + 1][mazey] > 0:
                                pathmaze[mazex + 1][mazey] = pathmaze[mazex + 1][mazey] + 1
                            if pathmaze[mazex][mazey - 1] > 0:
                                pathmaze[mazex][mazey - 1] = pathmaze[mazex][mazey - 1] + 1
                            if pathmaze[mazex][mazey + 1] > 0:
                                pathmaze[mazex][mazey + 1] = pathmaze[mazex][mazey + 1] + 1
                            if globals.timer_r == 0:
                                globals.start_t = time.time()
                                globals.timer_r = 1
                            pathmaze[mazex][mazey] = 1
                            sqmaze[mazex][mazey] = 2
                            display.refresh_ingame_screen(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons, 1, solver_text)
                            # check if the maze is solved
                            if sqmaze[mazex - 1][mazey] == 4 or sqmaze[mazex + 1][mazey] == 4 or sqmaze[mazex][mazey - 1] == 4 or sqmaze[mazex][mazey + 1] == 4:
                                for i in range(2*rows+1):
                                    for j in range(2*cols+1):
                                        if sqmaze[i][j] == 2:
                                            sqmaze[i][j] = 5
                                display.refresh_ingame_screen(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons, 1, solver_text)
                                display.display_endgame()
                                globals.timer_r = 0
                                pygame.display.flip()
                    elif sqmaze[mazex][mazey] == 2:    # the tile is selected. check if unselectable or not
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
                            display.refresh_ingame_screen(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons, 1, solver_text)
# screen button events                    
            for button in buttons:
                button.handle_event(event)
            # zoom in button
            if buttons[0].clicked:
                zoom += 1
                display.refresh_ingame_screen(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons, 0, solver_text)
                pygame.event.clear

            # zoom out button
            if buttons[1].clicked:
                zoom = max(1, zoom - 1)
                display.refresh_ingame_screen(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons, 0, solver_text)
                pygame.event.clear

            # center maze
            if buttons[2].clicked:
                zoom = zoom_init
                globals.mc_y = cols / 2
                globals.mc_x = rows / 2
                offset_y = -1 * cols // 2
                offset_x = -1 * rows // 2
                display.refresh_ingame_screen(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons, 0, solver_text)
                pygame.event.clear

            # restart maze solving
            if buttons[3].clicked:
                globals.timer_r = 0
                reset(rows, cols, sqmaze, pathmaze, startpos)
                display.refresh_ingame_screen(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons, 1, solver_text)
                pygame.event.clear

            # solver selection
            if buttons[4].clicked:
                solver = solver + 1
                if solver == 4:
                    solver = 0
                display.refresh_ingame_screen(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons, 1, solver_text)
                pygame.event.clear

            # solve the maze
            if buttons[5].clicked:
                reset(rows, cols, sqmaze, pathmaze, startpos)
                globals.alg_sp = 0
                if globals.timer_r == 0:
                    globals.start_t = time.time()
                    globals.timer_r = 1
                display.refresh_ingame_screen(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons, 1, solver_text)
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
                display.refresh_ingame_screen(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons, 1, solver_text)
                globals.timer_r = 0
                display.display_endgame_solved()
                pygame.display.flip()
                pygame.event.clear(pygame.MOUSEBUTTONDOWN)

            # re-generate maze
            if buttons[6].clicked:
                globals.timer_r = 0
                sqmaze, pathmaze, startpos, endpos = generate_maze(rows, cols, seed, seed_enabled)
                globals.path_nmbr = 0
                for i in range(rows * 2 + 1):
                    for j in range(cols * 2 + 1):
                        if sqmaze[i][j] == 1:
                            globals.path_nmbr = globals.path_nmbr + 1
                display.refresh_ingame_screen(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons, 0, solver_text)
                pygame.event.clear

            # quit
            if buttons[7].clicked:
                running = False


pygame.quit()

if __name__ == "__main__":
    main()
