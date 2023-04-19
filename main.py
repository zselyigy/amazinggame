import pygame
import generate
import display

import pygame


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


def main():
#Initialize pygame
    pygame.init()
    pygame.display.set_caption('The Wonder of Mazes')
    screen = pygame.display.set_mode((800, 800))
    startscreen = pygame.image.load(".\\retek.jpg")
#Define variables needed
    rows = 10
    cols = 10
    seed_enabled = False
    seed = 1681844304
    cell_size = 1
    offset_x, offset_y =0, 0
    zoom = 3
    buttons = []
    buttons.append(Button('Zoom In', 690, 50, 100, 30))
    buttons.append(Button('Zoom Out', 690, 90, 100, 30))
#Generate maze
    maze = generate.generate_maze_kruskal(rows, cols, seed, seed_enabled)
#Draw maze on screen
    display.draw(maze, screen, cell_size, offset_x, offset_y, zoom, rows, cols)
    button_draw(screen, buttons)
    pygame.display.flip()
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
                    display.draw(maze, screen, cell_size, offset_x, offset_y, zoom, rows, cols)
                    button_draw(screen, buttons)
                elif event.key == pygame.K_RIGHT:
                    offset_x += 1
                    display.draw(maze, screen, cell_size, offset_x, offset_y, zoom, rows, cols)
                    button_draw(screen, buttons)
                elif event.key == pygame.K_UP:
                    offset_y -= 1
                    display.draw(maze, screen, cell_size, offset_x, offset_y, zoom, rows, cols)
                    button_draw(screen, buttons)
                elif event.key == pygame.K_DOWN:
                    offset_y += 1
                    display.draw(maze, screen, cell_size, offset_x, offset_y, zoom, rows, cols)
                    button_draw(screen, buttons)
                elif event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:
                    zoom += 1
                    display.draw(maze, screen, cell_size, offset_x, offset_y, zoom, rows, cols)
                    button_draw(screen, buttons)
                elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                    zoom = max(1, zoom - 2)
                    display.draw(maze, screen, cell_size, offset_x, offset_y, zoom, rows, cols)
                    button_draw(screen, buttons)
# screen button events                    
            for button in buttons:
                button.handle_event(event)

            if buttons[0].clicked:
                zoom += 1
                display.draw(maze, screen, cell_size, offset_x, offset_y, zoom, rows, cols)
                button_draw(screen, buttons)
                pygame.display.flip()

            if buttons[1].clicked:
                zoom = max(1, zoom - 2)
                display.draw(maze, screen, cell_size, offset_x, offset_y, zoom, rows, cols)
                button_draw(screen, buttons)
                pygame.display.flip()



    pygame.quit()


if __name__ == "__main__":
    main()