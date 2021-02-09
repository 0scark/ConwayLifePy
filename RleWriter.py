import Constants

# see https://www.conwaylife.com/wiki/Run_Length_Encoded
class RleWriter:
    def __init__(self, filename, grid):
        self.f = open(filename, "w+")
        self.grid = grid
        self.num_live = 0
        self.num_death = 0
        self.buffer = []

    def flush(self):
        if len(''.join(self.buffer)) > 0:
            self.buffer.append("\n")
            self.f.write(''.join(self.buffer))

    def append(self, value):
        # do not allow lines > 70 chars, rle convention
        if (len(''.join(self.buffer)) + len(value)) >= Constants.MAX_RLE_LINE_SIZE:
            self.flush()
            self.buffer.clear()
        self.buffer.append(value)

    def write(self, num_live, num_death):
        if num_live > 0:
            if num_live > 1:
                self.append("{0}o".format(num_live))
            else:
                self.append("o")
        else:
            if num_death > 1:
                self.append("{0}b".format(num_death))
            else:
                self.append("b")

    def write_trailer(self, row):
        # end with '!'
        if row < (self.grid.num_rows - 1):
            self.append("$")
        else:
            self.append("!")

    def dump_row(self, row):
        output = []
        for col in range(self.grid.num_cols):
            if self.grid.matrix[row][col] == Constants.ALIVE:
                output.append('1')
            else:
                output.append('0')

    def header(self):
        self.f.write("#N name\n")
        self.f.write("#C comment\n")
        self.f.write("x = {0}, y = {1}\n".format(self.grid.num_cols, self.grid.num_rows))

    def reset_counters(self):
        self.num_live = 0
        self.num_death = 0

    def process_same_value(self, value):
        if value == Constants.ALIVE:            # update counters
            self.num_live += 1
        else:
            self.num_death += 1
        return False                            # indicate not written to file

    def process_new_value(self):
        self.write(self.num_live, self.num_death)       # write the previous values to file
        self.reset_counters()
        return True                                     # indicate written to file

    def save(self):
        self.header()
        for row in range(self.grid.num_rows):
            written = False
            self.reset_counters()
            cur_value = self.grid.matrix[row][0]
            for col in range(self.grid.num_cols):
                if cur_value == self.grid.matrix[row][col]:
                    written = self.process_same_value(cur_value)    # just update counters
                else:
                    written = self.process_new_value()              # write previous values to file
                    cur_value = self.grid.matrix[row][col]          # process new value
                    self.process_same_value(cur_value)
            if not written:
                self.process_new_value()  # new row, write to file what has not been written
            self.write_trailer(row)  # end row with eiter $ or !
        self.flush()    # ensure last data is written also
        self.f.close()  # close file

    @staticmethod
    def save_to_file(filename, grid):
        writer = RleWriter(filename, grid)
        writer.save()
