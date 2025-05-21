import pygame

class Keyboard:
    def __init__(self):
        self.up = False
        self.down = False
        self.left = False
        self.right = False

        self.w = False
        self.a = False
        self.s = False
        self.d = False


    """
    Precondition: event is KEYDOWN or KEYUP
    """
    def handle_events(self, event):
        handle = event.type == pygame.KEYDOWN
        if event.key == pygame.K_UP:
            self.up = handle
        elif event.key == pygame.K_DOWN:
            self.down = handle
        elif event.key == pygame.K_LEFT:
            self.left = handle
        elif event.key == pygame.K_RIGHT:
            self.right = handle
        elif event.key == pygame.K_w:
            self.w = handle
        elif event.key == pygame.K_a:
            self.a = handle
        elif event.key == pygame.K_s:
            self.s = handle
        elif event.key == pygame.K_d:
            self.d = handle
            
        