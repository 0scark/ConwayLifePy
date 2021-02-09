import sys

import pygame
import Constants


class Game:

    def __init__(self):
        from Screen import Screen
        self.screen = Screen()
        self.grid = self.create_grid().randomize()
        self.PAUSE = False

    def create_grid(self):
        from Grid import Grid
        return Grid(self.screen.num_rows(), self.screen.num_cols())

    def draw_grid(self):
        self.screen.clear()
        self.screen.draw_grid(self.grid)

    def determine_new_cell_state(self, row, col):
        # gegeven een cel[row][col], bepaal de nieuwe state van de cel aan de hand van zijn buren
        num_alive_neighbours = self.grid.get_alive_neighbours(row, col)
        cell_value = self.grid.get_value(row, col)
        if cell_value == Constants.ALIVE:
            if num_alive_neighbours < 2:    # rule 1: underpopulation: levende cel gaat dood uit eenzaamheid
                return Constants.DEATH
            if num_alive_neighbours == 2 or num_alive_neighbours == 3:
                return Constants.ALIVE      # rule 2: stay alive: levende cel heeft voldoende levende buren
            if num_alive_neighbours > 3:    # rule 3: overpopulation: cel gaat dood indien meer dan 3 levende buren
                return Constants.DEATH
        elif cell_value == Constants.DEATH:
            if num_alive_neighbours == 3:   # rule 4: reproduction: dode cel komt tot leven met 3 levende buren
                return Constants.ALIVE
        return cell_value                   # geen wijziging

    def update_generation(self):
        # maak een nieuwe grid en pas de regels toe op basis van de oude generatie
        new_grid = self.create_grid()
        for row in range(self.grid.num_rows):
            for col in range(self.grid.num_cols):
                new_cell_state = self.determine_new_cell_state(row, col)
                new_grid.set_value(row, col, new_cell_state)
        self.grid = new_grid

    def load_file(self, filename, offset_row=Constants.OFFSET_ROW, offset_col=Constants.OFFSET_COL):
        # lees een rle file in en plaats deze in grid vanaf offset[row][col]
        from RleReader import RleReader
        self.screen.clear()
        self.grid = self.create_grid()
        RleReader.read_from_file(self.grid, filename, offset_row, offset_col)
        self.screen.draw_grid(self.grid)
        self.PAUSE = True

    def save_file(self, filename):
        from RleWriter import RleWriter
        RleWriter.save_to_file(filename, self.grid)

    def handle_events(self):
        def key_file(key):
            num = key - pygame.K_0
            name = "./data/file_{0}.rle".format(num)
            return name

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:     # quit
                    sys.exit()
                elif event.key == pygame.K_p:   # pause
                    self.PAUSE = not self.PAUSE
                elif event.key == pygame.K_s:   # save
                    self.save_file("./data/pipo.rle")
                elif event.key == pygame.K_l:   # load
                    self.load_file("./data/pipo.rle", 0, 0)
                elif event.key == pygame.K_r:   # randomize
                    self.grid = self.create_grid().randomize()
                elif event.key == pygame.K_c:   # clear
                    self.grid.clear()
                elif event.key == pygame.K_t:   # single step if pause
                    self.update_generation()
                    self.screen.draw_grid(self.grid)
                elif event.key in [pygame.K_0,  # load key 1-0 file
                                   pygame.K_1,
                                   pygame.K_2,
                                   pygame.K_3,
                                   pygame.K_4,
                                   pygame.K_5,
                                   pygame.K_6,
                                   pygame.K_7,
                                   pygame.K_8,
                                   pygame.K_9
                                   ]:
                    self.load_file(key_file(event.key))
            elif event.type == pygame.QUIT:
                sys.exit()

    def run(self):
        while True:
            self.handle_events()
            if not self.PAUSE:
                self.update_generation()
                self.screen.draw_grid(self.grid)
            self.screen.cap_frame_rate()


if __name__ == "__main__":
    game = Game()
    game.run()
