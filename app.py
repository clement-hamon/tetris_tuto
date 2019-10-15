import pygame

screen_width = 300
screen_height = 600
block_size = 30

screen = pygame.display.set_mode([screen_width, screen_height])
screen.fill([0, 0, 0])



def draw_grid(surface):
    # draw horizontal lines
    for i in range(screen_height // block_size):
        pygame.draw.line(surface, (125, 125, 125), (0, block_size * i),(screen_width, block_size * i))
    # draw vertical lines
    for j in range(screen_width // block_size):
        pygame.draw.line(surface, (125, 125, 125), (block_size * j, 0),(block_size * j, screen_height))

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    draw_grid(screen)
    pygame.display.update()