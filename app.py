import pygame

screen_width = 300
screen_height = 600
block_size = 30

screen = pygame.display.set_mode([screen_width, screen_height])

def draw_grid(surface):
    # draw horizontal lines
    for i in range(screen_height // block_size):
        pygame.draw.line(surface, (125, 125, 125), (0, block_size * i),(screen_width, block_size * i))
    # draw vertical lines
    for j in range(screen_width // block_size):
        pygame.draw.line(surface, (125, 125, 125), (block_size * j, 0),(block_size * j, screen_height))

def draw_block(surface, x, y):
    pygame.draw.rect(surface, (125, 125, 125), (x * block_size, y * block_size, block_size, block_size))

x = 1
y = 2

run = True
while run:
    pygame.time.wait(500)
    
    y += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.fill([0, 0, 0])
    draw_grid(screen)
    draw_block(screen, x, y)

    pygame.display.update()