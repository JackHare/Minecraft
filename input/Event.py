import pygame

def poll_events(keyboard):
    for event in pygame.event.get():

        # Window Quit
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        # Keyboard events
        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            keyboard.handle_events(event)
