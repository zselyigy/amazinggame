import pygame
import generate
import display

def main():
    pygame.init()
    pygame.display.set_caption('The Wonder of Mazes')
    rows = 10
    cols = 10
    seed_enabled = False
    seed = 1681844304
    screen = pygame.display.set_mode((800, 800))
    maze = generate.generate_maze_kruskal(rows, cols, seed, seed_enabled)
    cell_size = 1
    offset_x, offset_y =0, 0
    zoom = 3
    display.draw(maze, screen, cell_size, offset_x, offset_y, zoom, rows, cols)
    running = True
    pygame.key.set_repeat(200, 10)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    offset_x -= 1
                    display.draw(maze, screen, cell_size, offset_x, offset_y, zoom, rows, cols)
                elif event.key == pygame.K_RIGHT:
                    offset_x += 1
                    display.draw(maze, screen, cell_size, offset_x, offset_y, zoom, rows, cols)
                elif event.key == pygame.K_UP:
                    offset_y -= 1
                    display.draw(maze, screen, cell_size, offset_x, offset_y, zoom, rows, cols)
                elif event.key == pygame.K_DOWN:
                    offset_y += 1
                    display.draw(maze, screen, cell_size, offset_x, offset_y, zoom, rows, cols)
                elif event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:
                    zoom += 1
                    display.draw(maze, screen, cell_size, offset_x, offset_y, zoom, rows, cols)
                elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                    zoom = max(1, zoom - 2)
                    display.draw(maze, screen, cell_size, offset_x, offset_y, zoom, rows, cols)                  
    pygame.quit()


if __name__ == "__main__":
    main()