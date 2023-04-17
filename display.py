import pygame

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


def draw(maze, screen, cell_size, offset_x, offset_y, zoom):
    screen.fill((0, 0, 0))
    draw_maze(maze, screen, cell_size, offset_x, offset_y, zoom)
    pygame.display.flip()