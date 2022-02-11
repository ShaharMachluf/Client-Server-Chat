import pygame
import easygui
from Button import Button
from Client import Client


class ClientGUI:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.WIDHT = 500
        self.HIGHT = 500
        self.screen = pygame.display.set_mode((self.WIDHT, self.HIGHT), depth=32)
        self.clock = pygame.time.Clock()
        self.Font = pygame.font.SysFont('ariel', 20)
        self.button_login = Button(pygame.Rect((8, 8), (70, 40)), "Log in", (255, 255, 128))

    def display(self):
        while True:
            for eve in pygame.event.get():
                if eve.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)
                if eve.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_login.rect.collidepoint(eve.pos):
                        self.button_login.pressed()
            pygame.draw.rect(self.screen, self.button_login.color, self.button_login.rect)
            if self.button_login.is_pressed:
                name = easygui.enterbox('enter your user name:', 'Log in')
                server = easygui.enterbox('enter your server name:', 'Log in')
                client = Client(name, server)
                self.button_login.text = "Log out"
            else:
                self.button_login.text = "Log in"
            button_login_text = self.Font.render(self.button_login.text, True, (0, 0, 0))
            self.screen.blit(button_login_text, (self.button_login.rect.x + 10, self.button_login.rect.y+5))
            pygame.display.update()
            self.screen.fill(pygame.Color(255, 250, 250))
            pygame.display.set_caption("Client")
            self.clock.tick(60)
