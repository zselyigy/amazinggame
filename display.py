import pygame
import globals

def textDisplay(text, fontsize, wtop, htop, width, heights, bgcolor, tcolor):
    font = pygame.font.SysFont(None, fontsize)
    rect = pygame.Rect(wtop, htop, width, heights)
    pygame.draw.rect(globals.screen, bgcolor, rect)
    text_surf = font.render(text, True, tcolor)
    text_rect = text_surf.get_rect(center=rect.center)
    globals.screen.blit(text_surf, text_rect)
    pygame.display.update(text_rect)

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