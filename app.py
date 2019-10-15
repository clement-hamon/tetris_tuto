import pygame

screen_width = 300
screen_height = 600

screen = pygame.display.set_mode([screen_width, screen_height])
screen.fill([0, 0, 0])

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()