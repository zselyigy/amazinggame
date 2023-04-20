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

def zoomlevel_diplay(screen,zoom_level):
    font = pygame.font.SysFont(None, 20)
    rect = pygame.Rect(690, 10, 100, 30)
    pygame.draw.rect(screen, (50, 50, 50), rect)
    text_surf = font.render('Zoom level: ' + str(zoom_level), True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)

def display_ingame_screen(maze, screen, offset_x, offset_y, zoom, rows, cols, buttons):
    display.draw(maze, screen, offset_x, offset_y, zoom, rows, cols)
    button_draw(screen, buttons)
    zoomlevel_diplay(screen,zoom)
    pygame.display.flip()

def main():
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
    startscreenpic = pygame.image.load(".\\retek.jpg")
    screen.blit(startscreenpic, (0, 0))
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
    seed_enabled = False
    seed = 1681844304
    offset_x, offset_y =0, 0
    zoom = 3
#Generate maze
    maze = generate.generate_maze_kruskal(rows, cols, seed, seed_enabled)
# setting up the start ingame screen
    buttons = []
    buttons.append(Button('Zoom In', 690, 50, 100, 30))
    buttons.append(Button('Zoom Out', 690, 90, 100, 30))
    buttons.append(Button('Quit', 690, 130, 100, 30))
#Draw maze on screen
    display_ingame_screen(maze, screen, offset_x, offset_y, zoom, rows, cols, buttons)
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
                    display_ingame_screen(maze, screen, offset_x, offset_y, zoom, rows, cols, buttons)
                elif event.key == pygame.K_RIGHT:
                    offset_x += 1
                    display_ingame_screen(maze, screen, offset_x, offset_y, zoom, rows, cols, buttons)
                elif event.key == pygame.K_UP:
                    offset_y -= 1
                    display_ingame_screen(maze, screen, offset_x, offset_y, zoom, rows, cols, buttons)
                elif event.key == pygame.K_DOWN:
                    offset_y += 1
                    display_ingame_screen(maze, screen, offset_x, offset_y, zoom, rows, cols, buttons)
                elif event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:
                    zoom += 1
                    display_ingame_screen(maze, screen, offset_x, offset_y, zoom, rows, cols, buttons)
                elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                    zoom = max(1, zoom - 1)
                    display_ingame_screen(maze, screen, offset_x, offset_y, zoom, rows, cols, buttons)
# screen button events                    
            for button in buttons:
                button.handle_event(event)

            if buttons[0].clicked:
                zoom += 1
                display_ingame_screen(maze, screen, offset_x, offset_y, zoom, rows, cols, buttons)

            if buttons[1].clicked:
                zoom = max(1, zoom - 1)
                display_ingame_screen(maze, screen, offset_x, offset_y, zoom, rows, cols, buttons)

            if buttons[2].clicked:
                running = False


    pygame.quit()


if __name__ == "__main__":
    main()