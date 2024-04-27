import pygame
from mazemanager import MazeManager
from gui import GUI
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('sound.mp3')
pygame.mixer.music.play(-1)
SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption('Maze')
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)
WIDTH, HEIGHT = pygame.display.get_surface().get_size()
BG = pygame.image.load("BG.jpeg")
gui = GUI(SCREEN, BG, WIDTH, HEIGHT)
while True:
    algorithm, rows, cols = gui.main_menu()
    manager = MazeManager(SCREEN, rows, cols, WIDTH, HEIGHT)
    maze = manager.create_maze()
    manager.play(algorithm)
    gui.show_new_back_button()