import pygame
from pprint import pprint

screen_width = 150
screen_height = 300
block_size = 30
num_of_rows = screen_height // block_size
num_of_cols = screen_width // block_size

screen = pygame.display.set_mode([screen_width, screen_height])

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

def draw_grid(surface):
    # draw horizontal lines
    for i in range(num_of_rows):
        pygame.draw.line(surface, (125, 125, 125), (0, block_size * i),(screen_width, block_size * i))
    # draw vertical lines
    for j in range(num_of_cols):
        pygame.draw.line(surface, (125, 125, 125), (block_size * j, 0),(block_size * j, screen_height))

class Piece(object):
    def __init__(self, shape, x, y):
        self.shape = shape
        self.x = x
        self.y = y
        self.rotation = 0
        self.blocks_positions = self.convert_shape_format(shape[0])
    
    def get_position(self):
        return (self.x, self.y)
    
    def get_blocks_position(self):
        positions = []
        for position in self.blocks_positions:
            positions.append((self.x + position[0], self.y  + position[1]))
        return positions
            
    def get_next_position(self, position):
        return (self.x + position[0], self.y + position[1])

    def get_next_blocks_position(self, next_position):
        positions = []
        for position in self.blocks_positions:
            positions.append((self.x + position[0] + next_position[0], self.y  + position[1] + next_position[1]))
        return positions
    
    def convert_shape_format(self, shape):
        positions = []
        for y, row in enumerate(shape):
            for x, col in enumerate(row):
                if shape[y][x] == "0":
                    positions.append((x, y))
        return positions

    def falls(self):
        self.y += 1
    
    def slides(self, coef):
        self.x += coef
    
    def draw(self, surface):
        for position in self.blocks_positions:
            pygame.draw.rect(surface, (125, 125, 125), ((self.x + position[0])* block_size, (self.y + position[1]) * block_size, block_size, block_size))


class BlocksManager(object):
    def __init__(self, limit_x, limit_y):
        self.blocks = []
        self.limit_x = limit_x
        self.limit_y = limit_y
    
    def add_block(self, position):
        self.blocks.append(position)
    
    def add_blocks(self, positions):
        for position in positions:
            self.blocks.append(position)

    def is_valid(self, position):
        return not (self.collide(position) or self.is_outside(position))

    def are_valid(self, positions):
        for position in positions:
            if (self.collide(position) or self.is_outside(position)):
                return False
        return True
    
    def collide(self, position):
        return (position in self.blocks)

    def is_outside(self, position):
        return (position[0] < self.limit_x['min'] or self.limit_x['max'] < position[0] or self.limit_y['max'] < position[1])

    def remove_full_rows(self):
        block_counter = self.count_blocks_per_row()
        for row, count in block_counter.items():
            if count >= num_of_cols:
                blocks_to_remove = [(x, row) for x in range(num_of_cols)]
                for block in blocks_to_remove:
                    self.blocks.pop(self.blocks.index(block))
                for y in range(1, row + 1)[::-1]:
                    for x in range(num_of_cols):
                        if (x, y - 1) in self.blocks:
                            self.blocks.append((x, y))
                            self.blocks.pop(self.blocks.index((x, y - 1)))

    def count_blocks_per_row(self):
        blocks_per_row = {}  # {12: 2, 13: 5,... }
        for block in self.blocks:
            if not (block[1] in blocks_per_row):
                blocks_per_row[block[1]] = 1
            else:
                blocks_per_row[block[1]] += 1
        return blocks_per_row

time_elapsed = pygame.time.get_ticks()
fall_event = pygame.USEREVENT + 1
pygame.time.set_timer(fall_event, 500)

current_piece = Piece(L, 1, 1)
blocks_manager = BlocksManager({"min": 0, "max": num_of_cols - 1}, {"min": 0, "max": num_of_rows - 1})

run = True
while run:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                next_pos = current_piece.get_next_blocks_position((-1, 0))
                if blocks_manager.are_valid(next_pos):
                    current_piece.slides(-1)
            if event.key == pygame.K_RIGHT:
                next_pos = current_piece.get_next_blocks_position((1, 0))
                if blocks_manager.are_valid(next_pos):
                    current_piece.slides(1)

        if event.type == fall_event:
            next_pos = current_piece.get_next_blocks_position((0, 1))
            if blocks_manager.are_valid(next_pos):
                current_piece.falls()
            else:
                blocks_manager.add_blocks(current_piece.get_blocks_position())
                current_piece = Piece(L, 1, 1)
                blocks_manager.remove_full_rows()


    screen.fill([0, 0, 0])
    draw_grid(screen)
    current_piece.draw(screen)

    for block in blocks_manager.blocks:
        pygame.draw.rect(screen, (125, 125, 125), ((block[0]) * block_size, (block[1]) * block_size, block_size, block_size))

    pygame.display.update()