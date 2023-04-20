import pygame
import generate

def draw_maze(maze, screen, offset_x, offset_y, zoom):
    for edge in maze:
        x1, y1 = edge[0][1], edge[0][0]
        x2, y2 = edge[1][1], edge[1][0]

        # Add offsets to starting and ending points
        x1 += offset_x
        y1 += offset_y
        x2 += offset_x
        y2 += offset_y
        if not (x1 == 0 or y1 == 0 or x2 == 0 or y2 == 0 or x1 == len(maze)-1 or y1 == len(maze[0])-1 or x2 == len(maze)-1 or y2 == len(maze[0])-1):
            # Draw white path
            path_width = max(1, int(zoom//2))
            if x1<x2:
                pygame.draw.line(screen, (255, 255, 255),
                                (int(x1  * zoom- int(path_width/2)), y1 * zoom),
                                (int(x2 * zoom+ int(path_width/2)), y2 * zoom),
                                path_width)

            else:
                pygame.draw.line(screen, (255, 255, 255),
                                (x1 * zoom, int(y1 * zoom)- int(path_width/2)),
                                (x2  * zoom, int(y2 * zoom)+ int(path_width/2)),
                                path_width)

            pygame.display.flip()

def draw_sqmaze(sqmaze, screen,  offset_x, offset_y, zoom, rows, cols):
    path_width = zoom
    for i in range(2*rows+1):
        for j in range(2*cols+1):
            if  sqmaze[i][j] == 1:
            # Draw white path
                pygame.draw.line(screen, (255, 255, 255),
                                ((i+offset_x) *  zoom, (j+offset_y) * zoom),
                                ((i+offset_x) *  zoom, (j+offset_y+1) * zoom-1),
                                path_width)
                
            if sqmaze[i][j] == 2:
    # Draw red square
                pygame.draw.rect(screen, (255, 0, 0),
                        ((i+offset_x) * zoom,
                        (j+offset_y) * zoom,
                        zoom,
                        zoom))


def draw(maze, screen,  offset_x, offset_y, zoom, rows, cols):
    screen.fill((0, 0, 0))
    sqmaze = generate.transform_display(rows, cols, maze)
    draw_sqmaze(sqmaze, screen,  offset_x, offset_y, zoom, rows, cols)
    pygame.display.flip()