import pygame
from pprint import pprint

screen_width = 150
screen_height = 300
block_size = 30
num_of_rows = screen_height // block_size
num_of_cols = screen_width // block_size

screen = pygame.display.set_mode([screen_width, screen_height])

def draw_grid(surface):
    # draw horizontal lines
    for i in range(num_of_rows):
        pygame.draw.line(surface, (125, 125, 125), (0, block_size * i),(screen_width, block_size * i))
    # draw vertical lines
    for j in range(num_of_cols):
        pygame.draw.line(surface, (125, 125, 125), (block_size * j, 0),(block_size * j, screen_height))

class Block(object):
    def __init__(self, x,y):
        self.x = x
        self.y = y
    
    def get_position(self):
        return (self.x, self.y)

    def get_next_position(self, position):
        return (self.x + position[0], self.y + position[1])

    def falls(self):
        self.y += 1
    
    def slides(self, coef):
        self.x += coef

    def draw(self, surface):
        pygame.draw.rect(surface, (125, 125, 125), (self.x * block_size, self.y * block_size, block_size, block_size))

def collide(position, other_positions):
    if position in other_positions:
        return True
    else:
        return False

def is_outside(position):
    if position[0] < 0 or num_of_cols - 1 < position[0]:
        return True
    else:
        return False

time_elapsed = pygame.time.get_ticks()
fall_event = pygame.USEREVENT + 1
pygame.time.set_timer(fall_event, 500)

current_block = Block(1, 2)
blocks = []

run = True
while run:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                next_pos = current_block.get_next_position((-1, 0))
                if not (collide(next_pos, blocks) or is_outside(next_pos)):
                    current_block.slides(-1)
            if event.key == pygame.K_RIGHT:
                next_pos = current_block.get_next_position((1, 0))
                if not (collide(next_pos, blocks) or is_outside(next_pos)):
                    current_block.slides(1)
        
        if event.type == fall_event:
            next_pos = current_block.get_next_position((0, 1))
            if next_pos[1] == num_of_rows or collide(current_block.get_next_position((0, 1)), blocks):
                blocks.append(current_block.get_position())
                current_block = Block(1, 2)
            else:
                current_block.falls()


    screen.fill([0, 0, 0])
    draw_grid(screen)
    current_block.draw(screen)

    for block in blocks:
        pygame.draw.rect(screen, (125, 125, 125), ((block[0]) * block_size, (block[1]) * block_size, block_size, block_size))

    pygame.display.update()