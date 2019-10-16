import pygame
import random
from pprint import pprint

screen_width = 300
screen_height = 600
block_size = 30
num_of_rows = screen_height // block_size
num_of_cols = screen_width // block_size
grid_color = (25, 25, 25)

screen = pygame.display.set_mode([screen_width, screen_height])

S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

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

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]

def draw_grid(surface):
    # draw horizontal lines
    for i in range(num_of_rows):
        pygame.draw.line(surface, grid_color, (0, block_size * i),(screen_width, block_size * i))
    # draw vertical lines
    for j in range(num_of_cols):
        pygame.draw.line(surface, grid_color, (block_size * j, 0),(block_size * j, screen_height))

class Piece(object):
    def __init__(self, shape, color, x, y):
        self.shape = shape
        self.color = color
        self.x = x
        self.y = y
        self.rotation = 0
        self.blocks_positions = self.convert_shape_format(shape[0])
    
    @staticmethod
    def create():
        return Piece(random.choice(shapes),random.choice(colors), 1, 1)

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

    def get_next_rotation_blocks_position(self):
        positions = []
        current_shape = self.shape[(self.rotation + 1) % len(self.shape)]
        next_blocks_positions = self.convert_shape_format(current_shape)
        for position in next_blocks_positions:
            positions.append((self.x + position[0], self.y  + position[1]))
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
    
    def rotate(self):
        self.rotation += 1
        current_shape = self.shape[(self.rotation) % len(self.shape)]
        self.blocks_positions = self.convert_shape_format(current_shape)

    def draw(self, surface):
        for position in self.blocks_positions:
            pygame.draw.rect(surface, self.color, ((self.x + position[0])* block_size, (self.y + position[1]) * block_size, block_size, block_size))


class BlocksManager(object):
    def __init__(self, limit_x, limit_y):
        self.blocks = {} # {(1, 2): (125, 125, 125), (1, 3) : (125, 125, 125), ...}
        self.limit_x = limit_x
        self.limit_y = limit_y
    
    def add_blocks(self, positions, color):
        for position in positions:
            self.blocks[position] = color

    def are_valid(self, positions):
        for position in positions:
            if (self.collide(position) or self.is_outside(position)):
                return False
        return True
    
    def collide(self, position):
        return (position in self.blocks.keys())

    def is_outside(self, position):
        return (position[0] < self.limit_x['min'] or self.limit_x['max'] < position[0] or self.limit_y['max'] < position[1])

    def remove_full_rows(self):
        block_counter = self.count_blocks_per_row()
        for row, count in block_counter.items():
            if count >= num_of_cols:
                positions_to_remove = [(x, row) for x in range(num_of_cols)]
                for position in positions_to_remove:
                    del self.blocks[position]
                for y in range(1, row + 1)[::-1]:
                    for x in range(num_of_cols):
                        if (x, y - 1) in self.blocks:
                            self.blocks[(x, y)] = self.blocks[(x, y - 1)]
                            del self.blocks[(x, y - 1)]

    def count_blocks_per_row(self):
        blocks_per_row = {}  # {12: 2, 13: 5,... }
        for block in self.blocks.keys():
            if not (block[1] in blocks_per_row):
                blocks_per_row[block[1]] = 1
            else:
                blocks_per_row[block[1]] += 1
        return dict(sorted(blocks_per_row.items()))

time_elapsed = pygame.time.get_ticks()
fall_event = pygame.USEREVENT + 1
pygame.time.set_timer(fall_event, 500)

current_piece = Piece.create()
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
            if event.key == pygame.K_DOWN:
                next_pos = current_piece.get_next_blocks_position((0, 1))
                if blocks_manager.are_valid(next_pos):
                    current_piece.falls()
            if event.key == pygame.K_UP:
                next_pos = current_piece.get_next_rotation_blocks_position()
                if blocks_manager.are_valid(next_pos):
                    current_piece.rotate()

        if event.type == fall_event:
            next_pos = current_piece.get_next_blocks_position((0, 1))
            if blocks_manager.are_valid(next_pos):
                current_piece.falls()
            else:
                blocks_manager.add_blocks(current_piece.get_blocks_position(), current_piece.color)
                current_piece = Piece.create()
                blocks_manager.remove_full_rows()


    screen.fill([0, 0, 0])
    current_piece.draw(screen)

    for position, color in blocks_manager.blocks.items():
        pygame.draw.rect(screen, color, ((position[0]) * block_size, (position[1]) * block_size, block_size, block_size))
    
    draw_grid(screen)

    pygame.display.update()