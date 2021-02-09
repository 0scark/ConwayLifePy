import Constants

# see https://www.conwaylife.com/wiki/Run_Length_Encoded
class RleReader:
    def __init__(self, filename, grid, offset_row, offset_col):
        self.filename = filename
        self.num_rows = 0
        self.num_cols = 0
        self.grid = grid
        self.comment_name = []
        self.comment_comment = []
        self.comment_other = []
        self.data = []
        self.OFFSET_ROW = offset_row
        self.OFFSET_COL = offset_col

    def process_comment(self, line):
        if line.startswith("#N"):
            self.comment_name.append(line[2:].strip())  # return everything after #N
        elif line.startswith("#C"):
            self.comment_comment.append(line[2:].strip())
        else:
            self.comment_other.append(line[2:].strip())

    def process_dimensions(self, line):
        lines = line.split(",")  # split "x = xx, y = xx , qq = xx" into entries
        for entry in lines:
            value = entry.replace(" ", "")  # strip spaces
            if value.startswith("x="):
                self.num_cols = int(value[2:])  # return everything after 'x=' eg 'x=48' -> 48 and convert to int
            elif value.startswith("y="):
                self.num_rows = int(value[2:])

    def process_data(self, line):
        # strip space, newline, carriage return
        value = line.replace(" ", "").replace("\n", "").replace("\r", "")
        self.data.append(value)

    def set_grid_values(self, row, col, number, value):
        if len(number) > 0:
            num = int("".join(number))  # make integer out of digit sequence
        else:
            num = 1  # 1 if no digits

        for x in range(num):
            self.grid.set_value(row, col + x, value)

        return col + num

    def generate_grid(self):

        value = "".join(self.data)      # convert data[] characters into 1 big string
        size = len(value)
        row = 0 + self.OFFSET_ROW
        col = 0 + self.OFFSET_COL
        number = []

        for index in range(size):
            char = value[index]
            if char in "1234567890":
                number.append(char)
            elif char == 'o':
                col = self.set_grid_values(row, col, number, Constants.ALIVE)
                number = []
            elif char == 'b':
                col = self.set_grid_values(row, col, number, Constants.DEATH)
                number = []
            elif char == '$':
                row += 1
                col = 0 + self.OFFSET_COL
                number = []
            elif char == '!':
                return
            else:
                return  # error

    def process_file(self):
        with open(self.filename, "r") as open_file:
            line = open_file.readline().strip()
            while line:
                if line[0] == '#':
                    self.process_comment(line)
                elif line[0] == 'x':
                    self.process_dimensions(line)
                else:
                    self.process_data(line)
                line = open_file.readline().strip()
        open_file.close()
        self.generate_grid()

    @staticmethod
    def read_from_file(grid, filename, offset_row, offset_col):
        reader = RleReader(filename, grid, offset_row, offset_col)
        reader.process_file()
