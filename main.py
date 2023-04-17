import pygame
import generate
import display

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    maze = generate.generate_maze_kruskal(10, 10)
    cell_size = 2
    offset_x, offset_y =5, 5
    zoom = 19
    display.draw(maze, screen, cell_size, offset_x, offset_y, zoom)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    offset_x += 1
                    display.draw(maze, screen, cell_size, offset_x, offset_y, zoom)
                elif event.key == pygame.K_RIGHT:
                    offset_x -= 1
                    display.draw(maze, screen, cell_size, offset_x, offset_y, zoom)
                elif event.key == pygame.K_UP:
                    offset_y += 1
                    display.draw(maze, screen, cell_size, offset_x, offset_y, zoom)
                elif event.key == pygame.K_DOWN:
                    offset_y -= 1
                    display.draw(maze, screen, cell_size, offset_x, offset_y, zoom)
                elif event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:
                    zoom += 2
                    display.draw(maze, screen, cell_size, offset_x, offset_y, zoom)
                elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                    zoom = max(1, zoom - 2)
                    display.draw(maze, screen, cell_size, offset_x, offset_y, zoom)
    pygame.quit()


if __name__ == "__main__":
    main()