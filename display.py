import pygame
import generate

def draw_maze(maze, screen, cell_size, offset_x, offset_y, zoom):
    for edge in maze:
        x1, y1 = edge[0][1], edge[0][0]
        x2, y2 = edge[1][1], edge[1][0]

        # Add offsets to starting and ending points
        x1 += offset_x
        y1 += offset_y
        x2 += offset_x
        y2 += offset_y
        # Check if the edge is on the border of the maze
        if x1 == 0 or y1 == 0 or x2 == 0 or y2 == 0 or x1 == len(maze)-1 or y1 == len(maze[0])-1 or x2 == len(maze)-1 or y2 == len(maze[0])-1:
            # Draw black wall
            a=5 
#            pygame.draw.line(screen, (0, 0, 0),
#                            ((x1 * cell_size + cell_size//2) * zoom, (y1 * cell_size + cell_size//2) * zoom),
#                            ((x2 * cell_size + cell_size//2) * zoom, (y2 * cell_size + cell_size//2) * zoom),
#                            max(1, int(zoom//2)))
#            print("black")
        else:
            # Draw white path
            path_width = max(1, int(cell_size*zoom//2))
            if x1<x2:
                pygame.draw.line(screen, (255, 255, 255),
                                (int((x1) * cell_size) * zoom- int(path_width/2), (y1 * cell_size ) * zoom),
                                (int((x2 * cell_size ) * zoom+ int(path_width/2)), (y2 * cell_size ) * zoom),
                                path_width)

            else:
                pygame.draw.line(screen, (255, 255, 255),
                                ((x1 * cell_size ) * zoom, int(((y1) * cell_size) * zoom)- int(path_width/2)),
                                ((x2 * cell_size ) * zoom, int((y2 * cell_size ) * zoom)+ int(path_width/2)),
                                path_width)

            pygame.display.flip()

def draw_sqmaze(sqmaze, screen, cell_size, offset_x, offset_y, zoom, rows, cols):
#     path_width = max(1, int(cell_size*zoom//2))
    path_width = cell_size*zoom
    for i in range(2*rows+1):
        for j in range(2*cols+1):

        # Add offsets to starting and ending points

        # Check if the edge is on the border of the maze
#        if x1 == 0 or y1 == 0 or x2 == 0 or y2 == 0 or x1 == len(maze)-1 or y1 == len(maze[0])-1 or x2 == len(maze)-1 or y2 == len(maze[0])-1:
            if  sqmaze[i][j] == 1:
            # Draw white path
                pygame.draw.line(screen, (255, 255, 255),
                                ((i+offset_x) * cell_size * zoom, (j+offset_y) * cell_size  * zoom),
                                ((i+offset_x) * cell_size  * zoom, ((j+offset_y+1) * cell_size ) * zoom-1),
                                path_width)
                
            if sqmaze[i][j] == 2:
    # Draw red square
                pygame.draw.rect(screen, (255, 0, 0),
                        ((i+offset_x) * cell_size * zoom,
                        (j+offset_y) * cell_size * zoom,
                        cell_size * zoom,
                        cell_size * zoom))


def draw(maze, screen, cell_size, offset_x, offset_y, zoom, rows, cols):
    screen.fill((0, 0, 0))
    sqmaze = generate.transform_display(rows, cols, maze)
#    draw_maze(maze, screen, cell_size, offset_x, offset_y, zoom)
    draw_sqmaze(sqmaze, screen, cell_size, offset_x, offset_y, zoom, rows, cols)
    pygame.display.flip()