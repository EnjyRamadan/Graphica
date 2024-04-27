import pygame
from button import Button


class GUI:
    def __init__(self, screen, bg, width, height):
        self.screen = screen
        self.bg = bg
        self.width = width
        self.height = height
        self.close_rows = self.close_cols = False

    def __get_font(self, size):
        return pygame.font.Font("font.ttf", size)

    def __initialize_gui(self):
        self.input_rows = pygame.Rect(self.width / 4 - 185, 250, 350, 35)
        self.input_cols = pygame.Rect(self.width - self.width / 3 - 50, 250, 350, 35)

        self.rows_text = self.__get_font(50).render("Rows: ", True, "White")
        self.rows_rect = self.rows_text.get_rect(center=(self.width / 4, 175))

        self.cols_text = self.__get_font(50).render("Cols: ", True, "White")
        self.cols_rect = self.cols_text.get_rect(center=(self.width - (self.width / 4), 175))

        self.maze_text = self.__get_font(90).render("MAZE", True, "#03bafc")
        self.maze_rect = self.maze_text.get_rect(center=(self.width / 2, 80))

        self.bfs_button = Button(image=pygame.image.load("Play Rect.png"), pos=(self.width / 3, 375),
                                 text_input="BFS", font=self.__get_font(75), base_color="#d7fcd4", hovering_color="Green")

        self.dfs_button = Button(image=pygame.image.load("Play Rect.png"), pos=(self.width - 550, 375),
                                 text_input="DFS", font=self.__get_font(75), base_color="#d7fcd4", hovering_color="Green")

        self.astar_button = Button(image=pygame.image.load("Play Rect.png"), pos=(self.width / 3, 525),
                                   text_input="A*", font=self.__get_font(75), base_color="#d7fcd4", hovering_color="Green")

        self.greedy_button = Button(image=pygame.image.load("Play Rect.png"), pos=(self.width - 550, 525),
                                    text_input="Greedy", font=self.__get_font(50), base_color="#d7fcd4", hovering_color="Green")

        self.instructions_button = Button(image=pygame.image.load("Quit Rect.png"), pos=(self.width / 3, 675),
                                          text_input="Instructions", font=self.__get_font(30), base_color="#d7fcd4", hovering_color="Yellow")

        self.ucs_button = Button(image=pygame.image.load("Quit Rect.png"), pos=(self.width - 550, 675),
                                 text_input="UCS", font=self.__get_font(75), base_color="#d7fcd4", hovering_color="Green")

        self.quit_button = Button(image=pygame.image.load("Quit Rect.png"), pos=(self.width - 830, 800),
                                  text_input="QUIT", font=self.__get_font(75), base_color="#d7fcd4", hovering_color="Red")

        self.back_from_instructions_button = Button(image=pygame.image.load("Quit Rect.png"), pos=(self.width - 225, self.height//2),
                                                    text_input="Back", font=self.__get_font(75), base_color="#d7fcd4", hovering_color="#03bafc")

        self.maze_img = pygame.image.load('Play Rect.png')
        self.rows_img = pygame.image.load('Quit Rect.png')
        self.cols_img = pygame.image.load('Quit Rect.png')

    def __screen_blit(self):
        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(self.rows_img, (self.width / 4 - 200, 125))
        self.screen.blit(self.cols_img, (self.width - self.width / 3 - 50, 125))
        self.screen.blit(self.maze_img, (self.width / 3 + 75, 25))
        self.screen.blit(self.maze_text, self.maze_rect)
        self.screen.blit(self.rows_text, self.rows_rect)
        self.screen.blit(self.cols_text, self.cols_rect)

    def __show_instructions(self):
        while True:
            self.screen.blit(pygame.image.load("instructions.jpeg"), (0, 0))

            instructions_text = [
                "Maze App Implementing AI Search Techniques!",
                "",
                "1. Setting Up the Maze:",
                "   - Enter the number of rows and columns for the maze grid.",
                "   - Click on the grid cells to set the start point, goals, and obstacles.",
                "   - Press the SPACE key to begin the visualization.",
                "",
                "2. Drawing on the Grid:",
                "   - LEFT-CLICK: Set the start point and draw obstacles.",
                "   - MIDDLE-CLICK: Set goal points.",
                "   - RIGHT-CLICK: Erase.",
                "",
                "3. Playing Controls:",
                "   - Press SPACE to initiate the selected algorithm after setting up the maze.",
                "   - Enjoy watching the algorithm find the path from start to goals.",
                "",
                "Have fun exploring the world of maze-solving algorithms in this interactive app!"
            ]

            self.instructions_title_text = self.__get_font(32).render(instructions_text[0], True, "#de892f")
            self.instructions_title_rect = self.instructions_title_text.get_rect(center=(self.width / 4 + 320, 75))

            self.screen.blit(self.instructions_title_text, self.instructions_title_rect)

            font_heading = self.__get_font(25)
            font_body = self.__get_font(20)
            y_offset = 125

            for line in instructions_text[2:-1]:
                if line.startswith(("1.", "2.", "3.")):
                    color = "#03bafc"
                    font = font_heading
                else:
                    color = "White"
                    font = font_body

                text_surface = font.render(line, True, pygame.Color(color))
                text_rect = text_surface.get_rect(topleft=(20, y_offset))
                self.screen.blit(text_surface, text_rect)
                y_offset += 50

            last_text_surface = font_body.render(instructions_text[-1], True, pygame.Color("#de892f"))
            last_text_rect = last_text_surface.get_rect(topleft=(20, y_offset))
            self.screen.blit(last_text_surface, last_text_rect)

            self.back_from_instructions_button.change_color(pygame.mouse.get_pos())
            self.back_from_instructions_button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_from_instructions_button.check_for_input(pygame.mouse.get_pos()):
                        # self.main_menu()
                        return

            pygame.display.update()

    def main_menu(self):
        self.__initialize_gui()
        self.close_rows = self.close_cols = False
        buttons = [self.bfs_button, self.dfs_button, self.astar_button, self.greedy_button, self.ucs_button, self.instructions_button, self.quit_button]
        rows = cols = None
        color_inactive_rows = color_inactive_cols = pygame.Color('#03bafc')
        color_active_rows = color_active_cols = pygame.Color('Violet')
        color_rows = color_inactive_rows
        color_cols = color_inactive_cols
        active_rows = active_cols = False
        text_rows = text_cols = ''
        while True:

            mouse_pos = pygame.mouse.get_pos()
            self.__screen_blit()

            for button in buttons:
                button.change_color(mouse_pos)
                button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.input_rows.collidepoint(event.pos):
                        active_rows = True
                    else:
                        active_rows = False
                    color_rows = color_active_rows if active_rows else color_inactive_rows

                    if self.input_cols.collidepoint(event.pos):
                        active_cols = True
                    else:
                        active_cols = False
                    color_cols = color_active_cols if active_cols else color_inactive_cols

                if event.type == pygame.KEYDOWN:
                    if not self.close_rows:
                        if active_rows:
                            if event.key == pygame.K_RETURN:
                                try:
                                    rows = int(text_rows)
                                    text_rows = "Ready!"
                                    self.close_rows = True
                                except ValueError:
                                    text_rows = "Please enter a valid input!"
                            elif event.key == pygame.K_BACKSPACE:
                                text_rows = text_rows[:-1]
                                if len(text_rows) == 0:
                                    rows = None
                            else:
                                text_rows += event.unicode

                    if not self.close_cols:
                        if active_cols:
                            if event.key == pygame.K_RETURN:
                                try:
                                    cols = int(text_cols)
                                    text_cols = "Ready!"
                                    self.close_cols = True
                                except ValueError:
                                    text_cols = "Please enter a valid input!"
                            elif event.key == pygame.K_BACKSPACE:
                                text_cols = text_cols[:-1]
                                if len(text_cols) == 0:
                                    cols = None
                            else:
                                text_cols += event.unicode

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if rows is not None and cols is not None:
                        if self.bfs_button.check_for_input(mouse_pos):
                            return 'bfs', rows, cols
                        if self.dfs_button.check_for_input(mouse_pos):
                            return 'dfs', rows, cols
                        if self.greedy_button.check_for_input(mouse_pos):
                            return 'greedy', rows, cols
                        if self.astar_button.check_for_input(mouse_pos):
                            return 'astar', rows, cols
                        if self.ucs_button.check_for_input(mouse_pos):
                            return 'ucs', rows, cols
                    if self.instructions_button.check_for_input(mouse_pos):
                        self.__show_instructions()
                    if self.quit_button.check_for_input(mouse_pos):
                        exit()

            font = pygame.font.Font(None, 35)

            text_surface_rows = font.render(text_rows, True, pygame.Color('White'))
            pygame.draw.rect(self.screen, color_rows, self.input_rows, 2)
            self.screen.blit(text_surface_rows, (self.input_rows.x + 5, self.input_rows.y + 5))

            text_surface_cols = font.render(text_cols, True, pygame.Color('White'))
            pygame.draw.rect(self.screen, color_cols, self.input_cols, 2)
            self.screen.blit(text_surface_cols, (self.input_cols.x + 5, self.input_cols.y + 5))

            pygame.display.update()

    def show_new_back_button(self):
        self.back_from_algorithm_button = Button(image=pygame.image.load("Quit Rect.png"), pos=(self.width - 225, 200),
                                                 text_input="Back", font=self.__get_font(50), base_color="#d7fcd4",hovering_color="#03bafc")
        while True:

            self.back_from_algorithm_button.change_color(pygame.mouse.get_pos())
            self.back_from_algorithm_button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_from_algorithm_button.check_for_input(pygame.mouse.get_pos()):
                        return

            pygame.display.update()