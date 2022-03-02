import pygame
from Button import Button


class ServerGUI:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.WIDHT = 200
        self.HIGHT = 200
        self.screen = pygame.display.set_mode((self.WIDHT, self.HIGHT), depth=32)
        self.clock = pygame.time.Clock()
        self.Font = pygame.font.SysFont('ariel', 30)
        self.button_start = Button(pygame.Rect((65, 65), (70, 40)), "start", (255, 255, 128))

    def display(self):
        while True:
            for eve in pygame.event.get():
                if eve.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)
                if eve.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_start.rect.collidepoint(eve.pos):
                        self.button_start.pressed()

            pygame.draw.rect(self.screen, self.button_start.color, self.button_start.rect)
            if self.button_start.is_pressed:
                self.button_start.text = "stop"
            else:
                self.button_start.text = "start"
            button_start_text = self.Font.render(self.button_start.text, True, (0, 0, 0))
            self.screen.blit(button_start_text, (self.button_start.rect.x + 10, self.button_start.rect.y+5))
            pygame.display.update()
            self.screen.fill(pygame.Color(255, 250, 250))
            pygame.display.set_caption("Server")
            self.clock.tick(60)
