import pygame
import random
import tkinter as tk
import threading
from tkinter import messagebox
from collections import deque as queue
from cell import Cell
from colors import *


class MazeManager:
    def __init__(self, screen, rows, cols, width, height):
        self.screen = screen
        self.maze = []
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height

    def __show_messagebox(self):
        messagebox.showinfo("Note", "No Path Found")

    def __expand(self, cell: Cell):
        cell.neighbours = []

        if cell.row < cell.total_rows - 1 and not self.maze[cell.row + 1][cell.col].is_obstacle(): # down
            cell.neighbours.append(self.maze[cell.row + 1][cell.col])

        if cell.row > 0 and not self.maze[cell.row - 1][cell.col].is_obstacle(): # up
            cell.neighbours.append(self.maze[cell.row - 1][cell.col])

        if cell.col > 0 and not self.maze[cell.row][cell.col - 1].is_obstacle(): # left
            cell.neighbours.append(self.maze[cell.row][cell.col - 1])

        if cell.col < cell.total_cols - 1 and not self.maze[cell.row][cell.col + 1].is_obstacle(): # right
            cell.neighbours.append(self.maze[cell.row][cell.col + 1])

        return cell.neighbours

    def create_maze(self):
        gap_row = self.height // self.rows
        gap_col = self.width // self.cols
        for i in range(self.rows):
            self.maze.append([])
            for j in range(self.cols):
                cell = Cell(i, j, gap_row, gap_col, self.rows, self.cols)
                self.maze[i].append(cell)
        return self.maze

    def __draw_maze(self):
        gap_row = self.height // self.rows
        gap_col = self.width // self.cols
        for i in range(self.rows):
            pygame.draw.line(self.screen, GREY, (0, i * gap_row), (self.width, i * gap_row))
            for j in range(self.cols):
                pygame.draw.line(self.screen, GREY, (j * gap_col, 0), (j * gap_col, self.height))

    def __draw_scene(self):
        self.screen.fill(WHITE)
        for i in range(self.rows):
            for j in range(self.cols):
                self.maze[i][j].draw(self.screen)
        self.__draw_maze()
        pygame.display.update()

    def __get_clicked_pos(self, pos):
        gap_row = self.height // self.rows
        gap_col = self.width // self.cols
        x, y = pos
        row = x // gap_col
        col = y // gap_row
        return row, col

    def __bfs(self):
        fringe, visited, path = queue(), set(), []
        paths_dict = {self.start: None}
        fringe.append(self.start)
        while fringe:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            cell = fringe.popleft()
            if cell in self.goals:
                self.__visualize_path(cell, paths_dict)
                return

            if cell not in visited:
                visited.add(cell)
                cell.make_visited()
                neighbors = self.__expand(cell)
                for neighbor in neighbors:
                    if neighbor not in visited:
                        fringe.append(neighbor)
                        neighbor.make_explored()
                        paths_dict[neighbor] = cell
            self.__draw_scene()

    def __dfs(self):
        fringe, visited, path = [], set(), []
        paths_dict = {self.start: None}
        fringe.append([self.start])
        while fringe:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            if fringe[0] == [self.start]:
                cell = fringe.pop()[0]
            else:
                lst = fringe.pop(-1)
                cell = random.choice(lst)
                lst.remove(cell)
                if len(lst) != 0:
                    fringe.append(lst)

            if cell in self.goals:
                self.__visualize_path(cell, paths_dict)
                return

            if cell not in visited:
                visited.add(cell)
                cell.make_visited()
                neighbors = self.__expand(cell)
                final_neighbours = []
                for neighbor in neighbors:
                    if neighbor not in visited:
                        final_neighbours.append(neighbor)
                        neighbor.make_explored()
                        paths_dict[neighbor] = cell
                if len(final_neighbours) > 0:
                    fringe.append(final_neighbours)

            self.__draw_scene()

    def __get_cost(self, first, second):
        x1, y1 = first.row, first.col
        x2, y2 = second.row, second.col
        return abs(x1 - x2) + abs(y1 - y2)

    def __get_manhattan_distance(self, cell):
        min_distance = float('inf')
        for goal in self.goals:
            distance = abs(cell.row - goal.row) + abs(cell.col - goal.col)
            min_distance = min(min_distance, distance)
        return min_distance

    def __calc_heuristic(self):
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.maze[row][col]
                heuristic_curr_cell = self.__get_manhattan_distance(cell)
                self.maze[row][col].heuristic_val = heuristic_curr_cell

    def __greedy(self):
        self.__calc_heuristic()
        fringe, visited, path = [], set(), []
        paths_dict = {self.start: None}
        fringe.append((self.start.heuristic_val, self.start))
        while fringe:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            heuristic_val, cell = min(fringe, key=lambda x: x[0])
            fringe.remove((heuristic_val, cell))

            if cell in self.goals:
                self.__visualize_path(cell, paths_dict)
                return

            if cell not in visited:
                visited.add(cell)
                cell.make_visited()
                temp_lst = self.__expand(cell)
                neighbors = []
                for neighbor in temp_lst:
                    if neighbor not in visited:
                        neighbors.append((neighbor.heuristic_val, neighbor))
                        neighbor.make_explored()
                        paths_dict[neighbor] = cell
                neighbors.sort(key=lambda x: x[0])
                fringe.extend(neighbors)

            self.__draw_scene()

    def __astar(self):
        self.__calc_heuristic()
        fringe, visited, path = [], set(), []
        paths_dict = {self.start: None}
        fringe.append((self.start.heuristic_val + 0, self.start))
        while fringe:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            f_score, cell = min(fringe, key=lambda x: x[0])
            fringe.remove((f_score, cell))

            if cell in self.goals:
                self.__visualize_path(cell, paths_dict)
                return

            if cell not in visited:
                visited.add(cell)
                cell.make_visited()
                temp_lst = self.__expand(cell)
                neighbors = []
                for neighbor in temp_lst:
                    if neighbor not in visited:
                        f_score = neighbor.heuristic_val + self.__get_cost(self.start, neighbor)
                        neighbors.append((f_score, neighbor))
                        neighbor.make_explored()
                        paths_dict[neighbor] = cell
                fringe.extend(neighbors)
            self.__draw_scene()

    def __ucs(self):
        fringe, visited, path = [], set(), []
        paths_dict = {self.start: None}
        fringe.append((0, self.start))
        while fringe:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            cost, cell = min(fringe, key=lambda x: x[0])
            fringe.remove((cost, cell))

            if cell in self.goals:
                self.__visualize_path(cell, paths_dict)
                return

            if cell not in visited:
                visited.add(cell)
                cell.make_visited()
                temp_lst = self.__expand(cell)
                neighbors = []
                for neighbor in temp_lst:
                    if neighbor not in visited:
                        neighbors.append((cost + 1, neighbor))
                        neighbor.make_explored()
                        paths_dict[neighbor] = cell
                fringe.extend(neighbors)

            self.__draw_scene()

    def __visualize_path(self, goal, paths_dict):
        path, current_cell = [], goal
        while current_cell:
            path.append(current_cell)
            current_cell = paths_dict[current_cell]
        path = path[::-1]
        for cell in path:
            cell.make_path()
            self.__draw_scene()

    def play(self, algorithm):
        playing, self.start, self.goals = False, None, []
        running = True
        while running:
            self.screen.fill("Black")
            self.__draw_scene()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break

                if not playing:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            if self.start and len(self.goals) >= 0:
                                playing = True
                                match algorithm:
                                    case 'bfs':
                                        self.__bfs()
                                    case 'dfs':
                                        self.__dfs()
                                    case 'greedy':
                                        self.__greedy()
                                    case 'astar':
                                        self.__astar()
                                    case 'ucs':
                                        self.__ucs()
                                playing = False
                                return

                    if pygame.mouse.get_pressed()[0]:
                        pos = pygame.mouse.get_pos()
                        row, col = self.__get_clicked_pos(pos)
                        if row is not None and col is not None:
                            cell = self.maze[row][col]
                            if not self.start and cell not in self.goals:
                                self.start = cell
                                cell.make_start()
                            elif cell != self.start and cell not in self.goals:
                                cell.make_obstacle()
                    elif pygame.mouse.get_pressed()[1]:
                        pos = pygame.mouse.get_pos()
                        row, col = self.__get_clicked_pos(pos)
                        cell = self.maze[row][col]
                        if cell not in self.goals:
                            cell.make_goal()
                            self.goals.append(cell)
                    elif pygame.mouse.get_pressed()[2]:
                        pos = pygame.mouse.get_pos()
                        row, col = self.__get_clicked_pos(pos)
                        cell = self.maze[row][col]
                        cell.reset()
                        if cell == self.start:
                            self.start = None
                        if cell in self.goals:
                            self.goals.remove(cell)
            pygame.display.update()