import pygame
from colors import *


class Cell:
    def __init__(self, row, col, width, height, total_rows, total_cols):
        self.row = row
        self.col = col
        self.height = width
        self.width = height
        self.total_rows = total_rows
        self.total_cols = total_cols
        self.x = row * self.width
        self.y = col * self.height
        self.color = WHITE
        self.neighbours = []
        self.heuristic_val = -1

    def get_pos(self):
        return self.row, self.col

    def is_obstacle(self):
        return self.color == BLACK

    def is_open(self):
        return self.color == WHITE

    def is_visited(self):
        return self.color == RED

    def is_start(self):
        return self.color == LABANY

    def is_goal(self):
        return self.color == GREEN

    def make_obstacle(self):
        self.color = BLACK

    def reset(self):
        self.color = WHITE

    def make_visited(self):
        self.color = RED

    def make_explored(self):
        self.color = YELLOW

    def make_start(self):
        self.color = LABANY

    def make_goal(self):
        self.color = GREEN

    def make_path(self):
        self.color = PURPLE

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def __lt__(self, other):
        return False
