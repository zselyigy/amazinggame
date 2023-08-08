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
import decimal
try:
    import cPickle as pickle
except:
    import pickle
import os
from datetime import datetime

class gameConfig():
    def __init__(self):
        try:
            self.load()
        except:
            self.last_player = 'Player'
            self.last_rows = 10
            self.last_cols = 5
            self.last_gamemode = globals.gamemode_solvethemaze
            self.last_seeddict = {}

    def save(self):
        file = open('game.cfg','wb')
        file.write(pickle.dumps(self.__dict__))
        file.close()

    def load(self):
        file = open('game.cfg','rb')
        dataPickle = file.read()
        file.close()
        self.__dict__ = pickle.loads(dataPickle)

class maze_record:
    def __init__(self, date, cols, rows, solvtime):
        self.date = date
        self.cols = cols
        self.rows = rows
        self.solvtime = solvtime

class Player:
    def __init__(self, name):
        self.name = name
        self.records = []
        if not os.path.isdir("player_data"):
            os.makedirs("player_data")
            self.save()
        try:
            self.load()
        except:
            self.save()

    def save(self):
        file = open('.\\player_data\\'+self.name+'.dat','wb')
        file.write(pickle.dumps(self.__dict__))
        file.close()

    def load(self):
        file = open('.\\player_data\\'+self.name+'.dat','rb')
        dataPickle = file.read()
        file.close()
        self.__dict__ = pickle.loads(dataPickle)

    def add_record(self, date, cols, rows, solvtime):
        self.records.append(maze_record(date, cols, rows, solvtime))

class BestRecords:
    def __init__(self):
        self.bestrecords_solve = []
        try:
            self.load()
        except:
            self.save()

    def save(self):
        file = open('bestrecords','wb')
        file.write(pickle.dumps(self.__dict__))
        file.close()

    def load(self):
        file = open('bestrecords','rb')
        dataPickle = file.read()
        file.close()
        self.__dict__ = pickle.loads(dataPickle)

    def add_record(self, gamemode, date, cols, rows, solvtime):
        match gamemode:
            case globals.gamemode_solvethemaze:
                self.bestrecords_solve.append(maze_record(date, cols, rows, solvtime))
            case globals.gamemode_timelimited:
                pass
            case globals.gamemode_speedrun:
                pass
#def reset(rows, cols, sqmaze, pathmaze, startpos):
def reset(rows, cols, sqmaze, startpos, mypath, accessed_tiles):
    for i in range(2*rows+1):
        for j in range(2*cols+1):
            if sqmaze[i][j] == 2:
                sqmaze[i][j] = 1
            if sqmaze[i][j] == 5:
                sqmaze[i][j] = 1
            if sqmaze[i][j] == 6:
                sqmaze[i][j] = 1
    mypath.clear()
    accessed_tiles.clear()
    mypath.append([1,startpos])
    accessed_tiles.append([1,startpos])

def generate_maze(rows, cols, seed, seed_enabled, mypath, accessed_tiles):
    maze, seed = generate.generate_maze_kruskal(rows, cols, seed, seed_enabled)
    sqmaze = generate.transform_display(rows, cols, maze, seed, seed_enabled)
    mypath.clear()
    accessed_tiles.clear()
    something = True
    while something:
        startpos = random.randint(1, 2 * cols)
        if  sqmaze[1][startpos] == 1:
            sqmaze[1][startpos] = 3
            mypath.append([1,startpos])
            accessed_tiles.append([1, startpos])
            something = False

    something = True
    while something:
        endpos = random.randint(1, 2 * cols)
        if  sqmaze[2 * rows - 1][endpos] == 1:
            sqmaze[2 * rows - 1][endpos] = 4
            something = False
    return sqmaze, startpos, endpos, seed

def starts_screen_loop(startscreen_buttons, startscreen_inputs, rows, cols, MyPlayer, seeddict, sc):
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
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    seeddict = {}
                    sc = 0
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

# quit if quit button clickedcols
    if startgame_quit:
        pygame.quit()


def main():
    globals.global_init()
# Initialize pygame
    pygame.init()
    pygame.display.set_caption('The Wonder of Mazes')

    MyConfig = gameConfig()

# Define variables needed
    rows = MyConfig.last_rows
    cols = MyConfig.last_cols
    seeddict = MyConfig.last_seeddict
    sc = 0
    globals.gamemode_text = MyConfig.last_gamemode
    seed_enabled = False
    seed = 1683387020
    solver = 0
    solver_text = 'GBFS'
    globals.timer_r = 0
    MyPlayer = Player(MyConfig.last_player)

# Use this to set full screen
# full screen
    screen = pygame.display.set_mode((pygame.display.Info().current_w, pygame.display.Info().current_h))
# in window
#    screen = pygame.display.set_mode((800, 800))
    globals.screen = screen
# setting up the start screen
# arrays for the main components 
    startscreen_buttons = []    # buttons
    startscreen_inputs = []     # input fields

    starts_screen_loop(startscreen_buttons, startscreen_inputs, rows, cols, MyPlayer, seeddict, sc)

    rows=int(startscreen_inputs[0].text)
    cols=int(startscreen_inputs[1].text)
    seed_enabled = True
    if startscreen_inputs[2].text == '0' or startscreen_inputs[2].text == '':
        seed_enabled = False
        startscreen_inputs[2].text = '0'
    seed=int(startscreen_inputs[2].text)
    globals.gamemode_text = startscreen_buttons[2].text

    if MyConfig.last_player != MyPlayer.name:
        MyConfig.last_player = MyPlayer.name
        MyPlayer.save()

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
    mypath = []
    accessed_tiles = []
    sqmaze, startpos, endpos, seed = generate_maze(rows, cols, seed, seed_enabled, mypath, accessed_tiles)
    for i in range(rows * 2 + 1):
        for j in range(cols * 2 + 1):
            if sqmaze[i][j] == 1:
                globals.path_nmbr = globals.path_nmbr + 1
    try:
        keysList = list(seeddict[(str(rows)+"X"+str(cols))].keys())
        sc = len(keysList)
        seeddict.setdefault((str(rows)+"X"+str(cols)), {})[sc] = seed
    except KeyError:
            sc = 0
            seeddict.setdefault((str(rows)+"X"+str(cols)), {})[sc] = seed
    MyConfig.last_seeddict = seeddict
    MyConfig.save()
    print(seeddict)
# setting up the start ingame screen 
    buttons = []
# Setup and draw the ingame screen
    display.ingame_screen(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons, 0, accessed_tiles)
#Handle pygame events
    running = True
    pygame.key.set_repeat(200, 50)
    while running:
        display.display_timer()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                MyConfig.last_sc = sc
                MyConfig.last_seeddict = seeddict 
                MyConfig.save()
                running = False
# keydown events
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    offset_x -= 1
                    display.refresh_ingame_screen(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons, 0, accessed_tiles)
                elif event.key == pygame.K_x:
                    seeddict = {}
                    sc = 0
                elif event.key == pygame.K_d:
                    offset_x += 1
                    display.refresh_ingame_screen(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons, 0, accessed_tiles)
                elif event.key == pygame.K_w:
                    offset_y -= 1
                    display.refresh_ingame_screen(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons, 0, accessed_tiles)
                elif event.key == pygame.K_s:
                    offset_y += 1
                    display.refresh_ingame_screen(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons, 0, accessed_tiles)
                elif event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:
                    zoom += 1
                    display.refresh_ingame_screen(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons, 0, accessed_tiles)
                elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                    zoom = max(1, zoom - 1)
                    display.refresh_ingame_screen(sqmaze,  offset_x, offset_y, zoom, rows, cols, buttons, 0, accessed_tiles)
                elif (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN) and (globals.kbmaction_text == "Arrows"):
                    if event.key == pygame.K_LEFT:
                        xdir = -1
                        ydir = 0
                    if event.key == pygame.K_RIGHT:
                        xdir = +1
                        ydir = 0
                    if event.key == pygame.K_UP:
                        xdir = 0
                        ydir = -1
                    if event.key == pygame.K_DOWN:
                        xdir = 0
                        ydir = 1
                    mazex = mypath[-1][0] + xdir
                    mazey = mypath[-1][1] + ydir
                    if sqmaze[mazex][mazey] == 1: # the tile the arrow showed is empty
                        if globals.timer_r == 0:
                            globals.start_t = time.time()
                            globals.timer_r = 1
                        sqmaze[mazex][mazey] = 2
                        mypath.append([mazex,mazey])
                        try:
                            tileindex = accessed_tiles.index([mazex,mazey])
                        except ValueError:
                            accessed_tiles.append([mazex,mazey])
                            globals.solved_text = len(accessed_tiles) / globals.path_nmbr
                            globals.c = decimal.Decimal(globals.solved_text)
                            globals.percentage =(round(globals.c, 4) * 100)
                            display.solved_display()
                        
                        display.refresh_ingame_screen(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons, 1, accessed_tiles)
                        # check if the maze is solved
                        if sqmaze[mazex - 1][mazey] == 4 or sqmaze[mazex + 1][mazey] == 4 or sqmaze[mazex][mazey - 1] == 4 or sqmaze[mazex][mazey + 1] == 4:
                            for i in range(2*rows+1):
                                for j in range(2*cols+1):
                                    if sqmaze[i][j] == 2:
                                        sqmaze[i][j] = 5
                            display.refresh_ingame_screen(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons, 1, accessed_tiles)
                            display.display_endgame()

                            MyPlayer.add_record(datetime.now(), cols, rows, globals.time)
                            MyPlayer.save()
                            globals.timer_r = 0
                            pygame.display.flip()
                    elif sqmaze[mazex][mazey] == 2: # the tile the arrow showed in the selected path
                        sqmaze[mypath[-1][0]][mypath[-1][1]] = 1
                        display.display_mazecell(offset_x, offset_y, zoom, mypath[-1][0], mypath[-1][1], sqmaze, accessed_tiles)
                        del mypath[-1]
                        pygame.display.flip()

            elif pygame.mouse.get_pressed()[0] == True:
                pygame.event.clear(pygame.MOUSEBUTTONDOWN)
                mazex = math.floor((event.pos[0] - globals.sc_x) / zoom + globals.mc_x - offset_x + 0.5)
                mazey = math.floor((event.pos[1] - globals.sc_y) / zoom + globals.mc_y - offset_y + 0.5)
                display.textDisplay(str(math.floor((event.pos[0] - globals.sc_x) / zoom + globals.mc_x - offset_x + 0.5)), 20, pygame.Rect(pygame.display.Info().current_w-globals.setup_screen_fontsize*7, 12*(globals.setup_screen_fontsize+20)+20 , globals.setup_screen_fontsize*5-20, globals.setup_screen_fontsize+10), globals.setup_screen_bg_color, globals.setup_screen_font_color)
                display.textDisplay(str(math.floor((event.pos[1] - globals.sc_y) / zoom + globals.mc_y - offset_y + 0.5)), 20, pygame.Rect(pygame.display.Info().current_w-globals.setup_screen_fontsize*4, 12*(globals.setup_screen_fontsize+20)+20 , globals.setup_screen_fontsize*5-20, globals.setup_screen_fontsize+10), globals.setup_screen_bg_color, globals.setup_screen_font_color)
                if (globals.kbmaction_text == "Click and drag"):
                        if mazex > -1 and mazex < 2 * rows + 1 and mazey > -1 and mazey < 2 * cols + 1:
                            if sqmaze[mazex][mazey] == 1:    # the tile is empty. check if selectable or not
                                if (abs(mypath[-1][0] - mazex) + abs(mypath[-1][1] - mazey)) == 1:
                                    if globals.timer_r == 0:
                                        globals.start_t = time.time()
                                        globals.timer_r = 1
                                    sqmaze[mazex][mazey] = 2
                                    mypath.append([mazex,mazey])
                                    try:
                                        tileindex = accessed_tiles.index([mazex,mazey])
                                    except ValueError:
                                        accessed_tiles.append([mazex,mazey])
                                        globals.solved_text = len(accessed_tiles) / globals.path_nmbr
                                        globals.c = decimal.Decimal(globals.solved_text)
                                        globals.percentage =(round(globals.c, 4) * 100)
                                        display.solved_display()
                                    
                                    display.refresh_ingame_screen(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons, 1, accessed_tiles)
                                    # check if the maze is solved
                                    if sqmaze[mazex - 1][mazey] == 4 or sqmaze[mazex + 1][mazey] == 4 or sqmaze[mazex][mazey - 1] == 4 or sqmaze[mazex][mazey + 1] == 4:
                                        for i in range(2*rows+1):
                                            for j in range(2*cols+1):
                                                if sqmaze[i][j] == 2:
                                                    sqmaze[i][j] = 5
                                        display.refresh_ingame_screen(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons, 1, accessed_tiles)
                                        display.display_endgame()

                                        MyPlayer.add_record(datetime.now(), cols, rows, globals.time)
                                        MyPlayer.save()
                                        globals.timer_r = 0
                                        pygame.display.flip()
                elif (globals.kbmaction_text == "Click direction"):
                        if mazex > -1 and mazex < 2 * rows + 1 and mazey > -1 and mazey < 2 * cols + 1:
                                    if (mazex == mypath[-1][0] or mazey == mypath[-1][1]) and not (mazex == mypath[-1][0] and mazey == mypath[-1][1]):
                                        if mazex == mypath[-1][0]:   # the x coordinate is the same, check the y direction
                                            cds = numpy.sign(mazey - mypath[-1][1])   # determines the direction of click
                                            for j in range(mypath[-1][1] + cds, mazey + cds, cds):
                                                match sqmaze[mazex][j]:
                                                    case 0: # the next tile is wall, stop
                                                        break
                                                    case 1: # the tile is empty, we can move
                                                        if globals.timer_r == 0:
                                                            globals.start_t = time.time()
                                                            globals.timer_r = 1
                                                        sqmaze[mazex][j] = 2
                                                        mypath.append([mazex,j])
                                                        try:
                                                            tileindex = accessed_tiles.index([mazex,j])
                                                        except ValueError:
                                                            accessed_tiles.append([mazex,j])
                                                            globals.solved_text = len(accessed_tiles) / globals.path_nmbr
                                                            globals.c = decimal.Decimal(globals.solved_text)
                                                            globals.percentage =(round(globals.c, 4) * 100)
                                                            display.solved_display()
                                                        display.display_mazecell(offset_x, offset_y, zoom, mazex, j, sqmaze, accessed_tiles)
                                                        pygame.display.flip()
                                                        # display.refresh_ingame_screen(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons, 1, accessed_tiles)
                                                        # check if the maze is solved
                                                        masolved = False
                                                        if mazex > 0:
                                                            if sqmaze[mazex - 1][j] == 4:
                                                                masolved = True
                                                        if mazex < 2*rows + 1:
                                                            if sqmaze[mazex + 1][j] == 4:
                                                                masolved = True
                                                        if j > 0:
                                                            if sqmaze[mazex][j - 1] == 4:
                                                                masolved = True
                                                        if j < 2*cols + 1:
                                                            if sqmaze[mazex][j + 1] == 4:
                                                                masolved = True

                                                        if masolved:
                                                            for i in range(2*rows+1):
                                                                for j in range(2*cols+1):
                                                                    if sqmaze[i][j] == 2:
                                                                        sqmaze[i][j] = 5
                                                            display.refresh_ingame_screen(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons, 1, accessed_tiles)
                                                            display.display_endgame()

                                                            MyPlayer.add_record(datetime.now(), cols, rows, globals.time)
                                                            MyPlayer.save()
                                                            globals.timer_r = 0
                                                            pygame.display.flip()
                                                        # check if we reached a crossing
                                                        if mazex > 0:
                                                            if sqmaze[mazex-1][j] == 1:
                                                                break
                                                        if mazex < 2 * rows:
                                                            if sqmaze[mazex+1][j] == 1:
                                                                break
                                        else: # the y coordinate is the same, check the x direction
                                            cds = numpy.sign(mazex-mypath[-1][0])   # determines the direction of click
                                            for i in range(mypath[-1][0] + cds, mazex + cds, cds):
                                                match sqmaze[i][mazey]:
                                                    case 0: # the next tile is wall, stop
                                                        break
                                                    case 1: # the tile is empty, we can move
                                                        if globals.timer_r == 0:
                                                            globals.start_t = time.time()
                                                            globals.timer_r = 1
                                                        sqmaze[i][mazey] = 2
                                                        mypath.append([i,mazey])                                                        
                                                        try:
                                                            tileindex = accessed_tiles.index([i,mazey])
                                                        except ValueError:
                                                            accessed_tiles.append([i,mazey])
                                                            globals.solved_text = len(accessed_tiles) / globals.path_nmbr
                                                            globals.c = decimal.Decimal(globals.solved_text)
                                                            globals.percentage =(round(globals.c, 4) * 100)
                                                            display.solved_display()
                                                        display.display_mazecell(offset_x, offset_y, zoom, i, mazey, sqmaze, accessed_tiles)
                                                        pygame.display.flip()
                                                        # display.refresh_ingame_screen(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons, 1, accessed_tiles)
                                                        # check if the maze is solved
                                                        masolved = False
                                                        if i > 0:
                                                            if sqmaze[i - 1][mazey] == 4:
                                                                masolved = True
                                                        if i < 2*rows + 1:
                                                            if sqmaze[i + 1][mazey] == 4:
                                                                masolved = True
                                                        if mazey > 0:
                                                            if sqmaze[i][mazey - 1] == 4:
                                                                masolved = True
                                                        if mazey < 2*cols + 1:
                                                            if sqmaze[i][mazey + 1] == 4:
                                                                masolved = True

                                                        if masolved:
                                                            for i in range(2*rows+1):
                                                                for j in range(2*cols+1):
                                                                    if sqmaze[i][j] == 2:
                                                                        sqmaze[i][j] = 5
                                                            display.refresh_ingame_screen(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons, 1, accessed_tiles)
                                                            display.display_endgame()

                                                            MyPlayer.add_record(datetime.now(), cols, rows, globals.time)
                                                            MyPlayer.save()
                                                            globals.timer_r = 0
                                                            pygame.display.flip()
                                                        # check if we reached a crossing
                                                        if mazey > 0:
                                                            if sqmaze[i][mazey - 1] == 1:
                                                                break
                                                        if mazey < 2 * cols:
                                                            if sqmaze[i][mazey + 1] == 1:
                                                                break

            
            elif pygame.mouse.get_pressed()[2] == True:
                if globals.kbmaction_text == "Click and drag" or globals.kbmaction_text == "Click direction":
                    mazex = math.floor((event.pos[0] - globals.sc_x) / zoom + globals.mc_x - offset_x + 0.5)
                    mazey = math.floor((event.pos[1] - globals.sc_y) / zoom + globals.mc_y - offset_y + 0.5)
                    if mazex > -1 and mazex < 2 * rows + 1 and mazey > -1 and mazey < 2 * cols + 1:
                        if (mypath[-1][0] == mazex) and (mypath[-1][1] == mazey):    # is this the last selected tile?
                                sqmaze[mazex][mazey] = 1
                                del mypath[-1]
                                display.display_mazecell(offset_x, offset_y, zoom, mazex, mazey, sqmaze, accessed_tiles)
                                pygame.display.flip()

            if event.type == pygame.MOUSEMOTION:
                display.textDisplay(str(mypath[-1][0]), 20, pygame.Rect(pygame.display.Info().current_w-globals.setup_screen_fontsize*7, 10*(globals.setup_screen_fontsize+20)+20 , globals.setup_screen_fontsize*5-20, globals.setup_screen_fontsize+10), globals.setup_screen_bg_color, globals.setup_screen_font_color)
                display.textDisplay(str(mypath[-1][1]), 20, pygame.Rect(pygame.display.Info().current_w-globals.setup_screen_fontsize*4, 10*(globals.setup_screen_fontsize+20)+20 , globals.setup_screen_fontsize*5-20, globals.setup_screen_fontsize+10), globals.setup_screen_bg_color, globals.setup_screen_font_color)
                display.textDisplay(str(math.floor((event.pos[0] - globals.sc_x) / zoom + globals.mc_x - offset_x + 0.5)), 20, pygame.Rect(pygame.display.Info().current_w-globals.setup_screen_fontsize*7, 11*(globals.setup_screen_fontsize+20)+20 , globals.setup_screen_fontsize*5-20, globals.setup_screen_fontsize+10), globals.setup_screen_bg_color, globals.setup_screen_font_color)
                display.textDisplay(str(math.floor((event.pos[1] - globals.sc_y) / zoom + globals.mc_y - offset_y + 0.5)), 20, pygame.Rect(pygame.display.Info().current_w-globals.setup_screen_fontsize*4, 11*(globals.setup_screen_fontsize+20)+20 , globals.setup_screen_fontsize*5-20, globals.setup_screen_fontsize+10), globals.setup_screen_bg_color, globals.setup_screen_font_color)


#                                display.refresh_ingame_screen(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons, 1, accessed_tiles)
# screen button events                    
            for button in buttons:
                button.handle_event(event)
            # zoom in button
            if buttons[0].clicked:
                    zoom += 1
                    display.refresh_ingame_screen(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons, 0, accessed_tiles)
                    pygame.event.clear(pygame.MOUSEBUTTONDOWN)

            # zoom out button
            if buttons[1].clicked:
                    zoom = max(1, zoom - 1)
                    display.refresh_ingame_screen(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons, 0, accessed_tiles)
                    pygame.event.clear(pygame.MOUSEBUTTONDOWN)

            # center maze
            if buttons[2].clicked:
                if button.counter == 1:
                    zoom = zoom_init
                    globals.mc_y = cols / 2
                    globals.mc_x = rows / 2
                    offset_y = -1 * cols // 2
                    offset_x = -1 * rows // 2
                    display.refresh_ingame_screen(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons, 0, accessed_tiles)
                    pygame.event.clear(pygame.MOUSEBUTTONDOWN)
                    button.counter = 0

            # restart maze solving
            if buttons[3].clicked:
                if button.counter == 1:
                    globals.timer_r = 0
                    globals.time = 0.0
                    globals.percentage = 0
                    reset(rows, cols, sqmaze, startpos, mypath, accessed_tiles)
                    display.refresh_ingame_screen(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons, 1, accessed_tiles)
                    pygame.event.clear(pygame.MOUSEBUTTONDOWN)
                    button.counter = 0

            # solver selection
            if buttons[4].clicked:
                if button.counter == 1:
                    solver = solver + 1
                    if solver == 4:
                        solver = 0
                    display.refresh_ingame_screen(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons, 1, accessed_tiles)
                    pygame.event.clear(pygame.MOUSEBUTTONDOWN)
                    button.counter = 0

            # solve the maze
            if buttons[5].clicked:
                    if button.counter == 1:
                        reset(rows, cols, sqmaze, startpos, mypath, accessed_tiles)
                        globals.alg_sp = 0
                        if globals.timer_r == 0:
                            globals.start_t = time.time()
                            globals.timer_r = 1
                        display.refresh_ingame_screen(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons, 1, accessed_tiles)
                        if solver == 0:
                            solution = solve.GBFS(sqmaze, offset_x, offset_y, zoom, rows, cols, mypath[-1], (2 * rows - 1, endpos))
                        if solver == 1:
                            solution = solve.astar(sqmaze, offset_x, offset_y, zoom, rows, cols, mypath[-1], (2 * rows - 1, endpos))
                        if solver == 2:
                            solution = solve.dfs(sqmaze, offset_x, offset_y, zoom, rows, cols, mypath[-1], (2 * rows - 1, endpos))
                        if solver == 3:
                            solution = solve.bfs(sqmaze, offset_x, offset_y, zoom, rows, cols, mypath[-1], (2 * rows - 1, endpos))
                        if solver == 4:
                            solution = solve.dijkstra(sqmaze, offset_x, offset_y, zoom, rows, cols, mypath[-1], (2 * rows - 1, endpos))
                        for so in solution:
                            sqmaze[so[0]][so[1]] = 5
                        sqmaze[1][startpos] = 3
                        sqmaze[2 * rows - 1][endpos] = 4
                        display.refresh_ingame_screen(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons, 1, accessed_tiles)
                        globals.timer_r = 0
                        display.display_endgame_solved()
                        pygame.display.flip()
                        button.counter = 0

            # re-generate maze
            if buttons[6].clicked:
                if button.counter == 1:
                    globals.timer_r = 0
                    sqmaze, startpos, endpos, seed = generate_maze(rows, cols, seed, seed_enabled, mypath, accessed_tiles)
                    try:
                        keysList = list(seeddict[(str(rows)+"X"+str(cols))].keys())
                        sc = len(keysList)
                        seeddict.setdefault((str(rows)+"X"+str(cols)), {})[sc] = seed
                    except KeyError:
                        sc = 0
                        seeddict.setdefault((str(rows)+"X"+str(cols)), {})[sc] = seed
                    MyConfig.last_seeddict = seeddict
                    MyConfig.save()
                    print(seeddict)
                    mypath.append([1,startpos])
                    accessed_tiles.append([1,startpos])
                    globals.path_nmbr = 0
                    for i in range(rows * 2 + 1):
                        for j in range(cols * 2 + 1):
                            if sqmaze[i][j] == 1:
                                globals.path_nmbr = globals.path_nmbr + 1
                    display.refresh_ingame_screen(sqmaze, offset_x, offset_y, zoom, rows, cols, buttons, 0, accessed_tiles)
                    pygame.event.clear(pygame.MOUSEBUTTONDOWN)
                    button.counter = 0

            # keyboard and mouse action selection
            if buttons[7].clicked:
                globals.kbmaction_text = buttons[7].text

            # quit to main menu
            if buttons[8].clicked:
                temp = rows
                rows = cols
                cols = temp
                starts_screen_loop(startscreen_buttons, startscreen_inputs, rows, cols, MyPlayer, seeddict, sc)

            # quit
            if buttons[9].clicked:
                MyConfig.last_seeddict = seeddict 
                MyConfig.save()
                running = False

pygame.quit()

if __name__ == "__main__":
    main()
