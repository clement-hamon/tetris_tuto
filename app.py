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

class Block(object):
    def __init__(self, x,y):
        self.x = x
        self.y = y
    
    def falls(self):
        self.y += 1
    
    def slides(self, coef):
        self.x += coef

    def draw(self, surface):
        pygame.draw.rect(surface, (125, 125, 125), (self.x * block_size, self.y * block_size, block_size, block_size))

current_block = Block(1, 2)


time_elapsed = pygame.time.get_ticks()
fall_event = pygame.USEREVENT + 1
pygame.time.set_timer(fall_event, 500)

run = True
while run:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                current_block.slides(-1)
            if event.key == pygame.K_RIGHT:
                current_block.slides(1)
        
        if event.type == fall_event:
            current_block.falls()


    screen.fill([0, 0, 0])
    draw_grid(screen)
    current_block.draw(screen)

    pygame.display.update()