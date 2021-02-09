import random

import Constants


class Grid:
    def __init__(self, rows, cols):
        self.num_rows = rows
        self.num_cols = cols
        self.matrix = []
        self.initialize_matrix()

    def initialize_matrix(self):
        # maak een matrix -> matrix[num_row][num_col]
        for row_num in range(self.num_rows):
            list_of_columns = [0] * self.num_cols
            self.matrix.append(list_of_columns)

    def get_value(self, row, col):
        return self.matrix[row][col]

    def set_value(self, row, col, value):
        try:
            self.matrix[row][col] = value
        except:
            print("exception row={0} col={1} val={3}".format(row, col, value))

    def clear(self):
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                self.matrix[row][col] = Constants.DEATH

    def randomize(self):
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                self.matrix[row][col] = random.randint(Constants.DEATH, Constants.ALIVE)
        return self

    def get_alive_neighbours(self, row, col):
        # using toroidal boundary conditions - x wrap around size
        def wrap_neg(x, size):
            return (x + size) % size

        def wrap_pos(x, size):
            return x % size

        # Get the number of alive cells surrounding current cell on a toroidal surface.
        count_alive_neighbours = 0
        count_alive_neighbours += self.matrix[wrap_neg(row - 1, self.num_rows)][wrap_neg(col - 1, self.num_cols)]
        count_alive_neighbours += self.matrix[wrap_neg(row - 1, self.num_rows)][col]
        count_alive_neighbours += self.matrix[wrap_neg(row - 1, self.num_rows)][wrap_pos(col + 1, self.num_cols)]
        count_alive_neighbours += self.matrix[row][wrap_neg(col - 1, self.num_cols)]
        count_alive_neighbours += self.matrix[row][wrap_pos(col + 1, self.num_cols)]
        count_alive_neighbours += self.matrix[wrap_pos(row + 1, self.num_rows)][wrap_neg(col - 1, self.num_cols)]
        count_alive_neighbours += self.matrix[wrap_pos(row + 1, self.num_rows)][col]
        count_alive_neighbours += self.matrix[wrap_pos(row + 1, self.num_rows)][wrap_pos(col + 1, self.num_cols)]
        return count_alive_neighbours

    def is_alive(self, row, col):
        return self.get_value(row, col) == Constants.ALIVE
